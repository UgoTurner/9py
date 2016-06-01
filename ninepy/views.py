from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from .models import Post

def index(request):
    latest_post_list = Post.objects.order_by('-publication_date')[:5]
    context = {'latest_post_list': latest_post_list}
    return render(request, 'ninepy/index.html', context)


def post_details(request, post_id):
    try:
        post_details = Post.objects.get(pk=post_id)
        context = {'post_details': post_details}
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, 'ninepy/post_details.html', context)
	