import json

from django.shortcuts import render
from django.http      import HttpResponse, JsonResponse
from django.views     import generic
from chunks.models    import Chunk

class ChunkView(generic.View):
	pass