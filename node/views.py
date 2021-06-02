from django.http import HttpResponse
from django.http.response import HttpResponseNotAllowed, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from neomodel.exceptions import UniqueProperty
from neomodel.core import DoesNotExist

from .models import Node

@csrf_exempt
def create(req, name):
    if req.method not in  ['POST', 'OPTIONS']:
        return HttpResponseNotAllowed(permitted_methods=['POST', 'OPTIONS'])
    try:
        node = Node(name=name).save()
    except UniqueProperty:
        return HttpResponse(status=409, content='already exists')
    
    return JsonResponse({'name': node.name, 'id': node.id}, status=201)

@csrf_exempt
def connect(req, from_, to):
    if req.method not in  ['POST', 'OPTIONS']:
        return HttpResponseNotAllowed(permitted_methods=['POST', 'OPTIONS'])
    
    try:
        from_ = Node.nodes.get(name=from_)
    except DoesNotExist:
        return HttpResponseNotFound(from_)

    try:
        to = Node.nodes.get(name=to)
    except DoesNotExist:
        return HttpResponseNotFound(to)

    res = from_.connections.connect(to)
    return JsonResponse(res, safe=False)
    

def shortestpath(req, start, end):
    if req.method != 'GET':
        return HttpResponseNotAllowed(permitted_methods=['GET'])
    try:
        start = Node.nodes.get(name=start)
    except DoesNotExist:
        return HttpResponseNotFound(start)

    try:
        end = Node.nodes.get(name=end)
    except DoesNotExist:
        return HttpResponseNotFound(end)

    path = start.get_shortest_path(end.name)
    
    if not path:
        return HttpResponseNotFound()
    return JsonResponse({'Path': ','.join(node['name'].upper() for node in path.nodes)})