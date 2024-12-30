from django.urls import path
from . import views

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
    path('topic/<int:topic_id>/', views.thread_list, name='thread_list'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]
