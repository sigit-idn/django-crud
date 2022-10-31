from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task
import re


class Chunk(models.Model):
	title       = models.CharField(max_length=200)
	task        = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='chunks')
	finished_at = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return self.title

	def to_json(self):
		return {
			'id'         : self.id,
			'title'      : self.title,
			'task'       : self.task.id,
			'finished_at': self.finished_at
		}

	@property
	def duration(self):
		if self.finished_at is None:
			return

		chunk_sibling = self.task.chunks.filter(finished_at__lt=self.finished_at).order_by('-finished_at').first()
		started_at = chunk_sibling.finished_at if chunk_sibling is not None else self.task.started_at
		
		return self.finished_at - started_at