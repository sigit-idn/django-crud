import json

from django.shortcuts               import render
from django.http                    import HttpResponse, JsonResponse
from django.contrib.auth.models     import User
from django.views                   import generic
from tasks.models                   import Task
from chunks.models                  import Chunk


class TasksView(generic.View):
	def post(self, request, *args, **kwargs):
		request_body = json.loads(request.body)

		task = Task.objects.create(
			title       = request_body['title'],
			description = request_body['description'],
			due_date    = request_body['due_date'],
			user				= request.user
		)

		task.save()

		return JsonResponse(task.to_json())

class TaskView(generic.View):
	def get(self, request, *args, **kwargs):
		task = Task.objects.get(id=self.kwargs['id'])
		return JsonResponse(task.to_json())

	def put(self, request, *args, **kwargs):
		task = Task.objects.get(id=self.kwargs['id'])
		request_body = json.loads(request.body)
		task.title       = request_body['title']
		task.description = request_body['description']
		task.due_date    = request_body['due_date']
		task.started_at	 = request_body['started_at']
		task.save()
		return JsonResponse(task.to_json())

	def patch(self, request, *args, **kwargs):
		task = Task.objects.get(id=self.kwargs['id'])
		request_body = json.loads(request.body)
		task.title       = request_body['title'] if 'title' in request_body else task.title
		task.description = request_body['description'] if 'description' in request_body else task.description
		task.due_date    = request_body['due_date'] if 'due_date' in request_body else task.due_date
		task.started_at	 = request_body['started_at'] if 'started_at' in request_body else task.started_at
		task.save()
		return JsonResponse(task.to_json())

	def delete(self, request, *args, **kwargs):
		task = Task.objects.get(id=self.kwargs['id'])
		task.delete()
		return JsonResponse(task.to_json())

class ChunksView(generic.View):
	def get(self, request, *args, **kwargs):
		chunks = Chunk.objects.filter(task_id=self.kwargs['id'])
		return JsonResponse([chunk.to_json() for chunk in chunks], safe=False)

	def post(self, request, *args, **kwargs):
		request_body = json.loads(request.body)

		titles = request_body['title'].splitlines()

		for title in titles:
			if title:
				chunk = Chunk.objects.create(
					title = title,
					task_id = self.kwargs['task_id']
				)
				chunk.save()

		return JsonResponse([chunk.to_json() for chunk in chunks], safe=False)

class ChunkView(generic.View):
	def get(self, request, *args, **kwargs):
		chunk = Chunk.objects.get(id=self.kwargs['id'])
		return JsonResponse(chunk.to_json())

	def put(self, request, *args, **kwargs):
		chunk = Chunk.objects.get(id=self.kwargs['id'])
		request_body = json.loads(request.body)
		chunk.title   = request_body['title']
		if request_body['finishedAt']:
			chunk.finished_at = request_body['finishedAt']

		chunk.save()
		return JsonResponse(chunk.to_json())

	def delete(self, request, *args, **kwargs):
		chunk = Chunk.objects.get(id=self.kwargs['id'])
		chunk.delete()
		return JsonResponse(chunk.to_json())