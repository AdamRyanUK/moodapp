from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Thread(models.Model):
    topic = models.ForeignKey(Topic, related_name='threads', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='threads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    thread = models.ForeignKey(Thread, related_name='posts', on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE, null=True)  
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.created_by.username} in '{self.thread.title}' - {self.content[:30]}..."

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_by.username} - Comment"
