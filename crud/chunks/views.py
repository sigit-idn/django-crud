import json

from django.shortcuts               import render
from django.http                    import HttpResponse, JsonResponse
from django.views                   import generic
from chunks.models                  import Chunk

class ChunkView(generic.View):
	def put(self, request, *args, **kwargs):
		chunk = Chunk.objects.get(id=self.kwargs['id'])
		request_body = json.loads(request.body)
		chunk.title = request_body['title']
		chunk.save()
		return JsonResponse(chunk.to_json())

	def delete(self, request, *args, **kwargs):
		chunk = Chunk.objects.get(id=self.kwargs['id'])
		chunk.delete()
		return JsonResponse(chunk.to_json())