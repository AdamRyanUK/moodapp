from django import forms
from .models import Thread, Post, Comment, Topic

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['thread', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'thread' in self.data:
            try:
                thread_id = int(self.data.get('thread'))
                # Filter the content to show only threads based on the topic
                self.fields['thread'].queryset = Thread.objects.filter(id=thread_id)
            except (ValueError, TypeError):
                pass


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
