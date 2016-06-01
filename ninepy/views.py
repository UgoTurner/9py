from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Post

def index(request):
    latest_post_list = Post.objects.order_by('-publication_date')[:5]
    context = {'latest_post_list': latest_post_list}
    return render(request, 'ninepy/index.html', context)