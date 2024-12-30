from .forms import PostForm
from django.contrib import admin
from .models import Topic, Thread, Post, Comment

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'created_by', 'created_at')
    list_filter = ('topic', 'created_by')
    search_fields = ('title', 'created_by__username')
    ordering = ('-created_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm  # Use the custom form with the thread field

    list_display = ('get_topic', 'get_thread', 'created_by', 'created_at', 'content_preview')
    list_filter = ('topic', 'thread', 'created_by')  # Filter by topic, thread, and created_by
    search_fields = ('content', 'created_by__username', 'thread__title', 'topic__name')
    ordering = ('-created_at',)

    # Display the topic name in the admin list view
    def get_topic(self, obj):
        return obj.topic.name if obj.topic else None
    get_topic.admin_order_field = 'topic'  # Allow sorting by topic
    get_topic.short_description = 'Topic'

    # Display the thread title in the admin list view
    def get_thread(self, obj):
        return obj.thread.title if obj.thread else None
    get_thread.admin_order_field = 'thread'  # Allow sorting by thread
    get_thread.short_description = 'Thread'

    # Content preview in the admin list view
    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Content Preview'

    def save_model(self, request, obj, form, change):
        # Automatically set the topic based on the selected thread
        if obj.thread:
            obj.topic = obj.thread.topic
        # Automatically set the created_by field to the current user if not already set
        if not getattr(obj, 'created_by', None):
            obj.created_by = request.user
        obj.save()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created_by', 'created_at', 'content_preview')
    list_filter = ('post', 'created_by')
    search_fields = ('content', 'created_by__username')
    ordering = ('-created_at',)

    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
