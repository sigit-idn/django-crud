import datetime
from django.db                  import models
from tasks.models               import Task


# pylint: disable=no-member
class Chunk(models.Model):
	"""Chunk is a model for the chunks table."""
	title       = models.CharField(max_length=200)
	task        = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='chunks')
	finished_at = models.DateTimeField(blank=True, null=True)

	@property
	def duration(self):
		"""duration is a property that returns the duration of the chunk."""
		if self.finished_at is None:
			return

		chunk_before = self.task.chunks.filter(finished_at__lt=self.finished_at).order_by('-finished_at').first()
		started_at = chunk_before.finished_at if chunk_before is not None else self.task.started_at

		days = (self.finished_at.date() - started_at.date()).days

		if days > 0:
			started_at += datetime.timedelta(hours=15) # over the time

		if days > 1:
			started_at += datetime.timedelta(days=2, hours=15) # over weekend

		return self.finished_at - started_at


	def __str__(self):
		return str(self.title)

	def to_json(self):
		"""to_json is a method that returns a json representation of the chunk."""
		return {
			'id'         : self.id,
			'title'      : self.title,
			'task'       : self.task.id,
			'finished_at': self.finished_at
		}