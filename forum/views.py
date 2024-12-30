from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Thread, Post, Comment
from .forms import ThreadForm, PostForm, CommentForm

def topic_list(request):
    topics = Topic.objects.all()
    return render(request, 'forum/topic_list.html', {'topics': topics})

def thread_list(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    threads = topic.threads.all()
    return render(request, 'forum/thread_list.html', {'topic': topic, 'threads': threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.all()
    return render(request, 'forum/thread_detail.html', {'thread': thread, 'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    return render(request, 'forum/post_detail.html', {'post': post, 'comments': comments})
