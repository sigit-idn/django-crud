import typing
import os

from datetime     import datetime, timedelta, timezone
from django.db    import models
from tasks.models import Task


# pylint: disable=no-member
class Chunk(models.Model):
	"""Chunk is a model for the chunks table."""
	title       = models.CharField(max_length=200)
	task        = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='chunks')
	finished_at = models.DateTimeField(blank=True, null=True)

	_WORK_START  = os.environ.get('WORK_START'  , '09:00')
	_WORK_END    = os.environ.get('WORK_END'    , '18:00')
	_BREAK_START = os.environ.get('BREAK_START' , '12:00')
	_BREAK_END   = os.environ.get('BREAK_END'   , '13:00')
	_WEEKENDS    = os.environ.get('WEEKENDS'    , '5,6')

	@property
	def duration(self: object) -> timedelta:
		"""duration is a property that returns the duration of the chunk."""
		if self.finished_at is None:
			return

		duration: timedelta = self.finished_at - self.started_at

		duration -= self.lunch_break

		duration -= self.out_of_work

		duration -= self.weekend

		return duration

	@property
	def started_at(self: object) -> datetime:
		"""started_at is a property that returns the started at of the chunk."""
		chunk_before: Chunk = self.task.chunks.filter(finished_at__lt=self.finished_at).order_by('-finished_at').first()
		return chunk_before.finished_at if chunk_before is not None else self.task.started_at

	def __str__(self) -> str:
		return str(self.title)

	def to_json(self) -> dict:
		"""to_json is a method that returns a json representation of the chunk."""
		return {
			'id'         : self.id,
			'title'      : self.title,
			'task'       : self.task.id,
			'finished_at': self.finished_at
		}

	def generate_time(self: object, time: str) -> datetime:
		"""generate_time is a method that returns a datetime object from a string."""
		return datetime.strptime(time, '%H:%M').replace(tzinfo=timezone.utc)

	@property
	def work_start(self: object) -> datetime:
		"""work_start is a property that returns the work start of the chunk."""
		return self.generate_time(self._WORK_START)

	@property
	def work_end(self: object) -> datetime:
		"""work_end is a property that returns the work end of the chunk."""
		return self.generate_time(self._WORK_END)

	@property
	def break_start(self: object) -> datetime:
		"""break_start is a property that returns the break start of the chunk."""
		return self.generate_time(self._BREAK_START)

	@property
	def break_end(self: object) -> datetime:
		"""break_end is a property that returns the break end of the chunk."""
		return self.generate_time(self._BREAK_END)

	@property
	def lunch_break(self: object) -> timedelta:
		"""lunch_break is a property that returns the lunch break of the chunk."""
		if self.finished_at is None:
			return timedelta()


		if self.started_at > self.break_end:
			return timedelta()

		if self.finished_at < self.break_start:
			return timedelta()

		if self.started_at < self.break_start:
			return self.break_start - self.started_at

		if self.finished_at > self.break_end:
			return self.finished_at - self.break_end

		return self.finished_at - self.started_at


	@property
	def out_of_work(self: object) -> timedelta:
		"""out_of_work is a property that returns the out of work of the chunk."""
		if self.finished_at is None:
			return timedelta()

		if self.started_at > self.work_end:
			return timedelta()

		if self.finished_at < self.work_start:
			return timedelta()

		if self.started_at < self.work_start:
			return self.work_start - self.started_at

		if self.finished_at > self.work_end:
			return self.finished_at - self.work_end

		return self.finished_at - self.started_at

	@property
	def weekend(self: object) -> timedelta:
		"""weekend is a property that returns the weekend of the chunk."""
		if self.finished_at is None:
			return timedelta()

		weekends: typing.List[int] = [int(weekend) for weekend in self._WEEKENDS.split(',')]

		if self.finished_at.weekday() in weekends:
			return timedelta()

		if self.started_at.weekday() in weekends:
			return timedelta()

		return timedelta()

		