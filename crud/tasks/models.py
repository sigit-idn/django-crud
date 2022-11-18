"""Task model"""

import typing
import datetime

from django.db                  import models
from django.contrib.auth.models import User

# pylint: disable=no-member
class Task(models.Model):
	"""Task is a model for the tasks table."""
	title       = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	due_date    = models.DateTimeField()
	started_at  = models.DateTimeField(blank=True, null=True)
	user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

	@property
	def progress(self: object) -> float:
		"""progress is a property that returns the progress of the task."""
		total_chunks = self.chunks.count()
		if total_chunks == 0:
			return 0

		finished_chunks = self.chunks.filter(finished_at__isnull=False).count()
		return finished_chunks / total_chunks * 100

	@property
	def estimated_seconds_left(self: object) -> int:
		"""estimated_seconds_left is a property that returns the estimated seconds left of the task."""
		if self.progress % 100 == 0:
			return 0

		estimated_time_left = (100 - self.progress) * (self.finished_at - self.started_at) / self.progress

		return int(estimated_time_left.total_seconds())

	@property
	def average_duration(self: object) -> int:
		"""average_duration is a property that returns the average duration of the task."""
		total_finished_chunks = self.chunks.filter(finished_at__isnull=False).count()
		if total_finished_chunks == 0:
			return 0

		total_duration = sum([
			chunk.duration.total_seconds() 
			for chunk in self.chunks.all()
			if chunk.duration is not None
		])

		return total_duration / total_finished_chunks / 3600 # in hours

	@property
	def finished_at(self: object) -> datetime.datetime:
		"""finished_at is a property that returns the finished at of the task."""
		return self.chunks.order_by('-finished_at').first().finished_at

	def __str__(self: object) -> str:
		return str(self.title)

	def to_json(self: object) -> dict:
		"""to_json is a method that returns a json representation of the task."""
		return {
			'id'         : self.id,
			'title'      : self.title,
			'description': self.description,
			'due_date'   : self.due_date,
			'started_at' : self.started_at,
			'user'       : self.user.id
		}