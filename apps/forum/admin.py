from django.contrib import admin
from .models import Reply, Session, Topic, Forum


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    search_fields = 'id', 'forum_title', 'forum_user', 'forum_slug', 
    ordering = '-id', 
    fields = 'forum_title', 'forum_user', 'forum_description', 'forum_slug', 
    list_filter = 'forum_title', 'forum_user', 'forum_slug', 
    list_display = 'forum_title', 'forum_user', 'forum_slug', 'forum_timestamp_create', 'forum_timestamp_update', 
    list_display_links = 'forum_title', 
    prepopulated_fields = {'forum_slug': ('forum_title',)}
    list_per_page = 10


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    search_fields = 'id', 'session_user', 'session_title', 'session_slug', 
    ordering = '-id', 
    fields = 'session_forum', 'session_user', 'session_title', 'session_description', 'session_slug', 'staff_only', 
    list_filter = 'session_user', 'session_slug', 'staff_only', 
    list_display = 'id', 'session_user', 'session_forum', 'session_title', 'session_description', 'staff_only', 'session_timestamp_create', 'session_timestamp_update', 
    list_display_links = 'session_title', 
    prepopulated_fields = {'session_slug': ('session_title',)}
    list_per_page = 10


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = 'id', 'topic_user', 'topic_session', 'topic_title', 'topic_slug', 'views', 'fixed', 'tag', 
    ordering = '-id', 
    fields = 'topic_user', 'topic_session', 'topic_title', 'topic_content', 'topic_slug', 'views', 'fixed', 'block', 'likes', 'tag', 
    list_filter = 'topic_user', 'topic_session', 'topic_title', 'topic_slug', 'tag', 'fixed', 
    list_display = 'id', 'topic_session', 'topic_title', 'topic_user', 'fixed', 'block', 'topic_timestamp_create', 'topic_timestamp_update', 
    list_display_links = 'topic_title', 
    prepopulated_fields = {'topic_slug': ('topic_title',)}
    list_per_page = 10
    autocomplete_fields = 'tag', 


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    search_fields = 'id', 'reply_user', 'reply_topic', 
    ordering = '-id', 
    fields = 'reply_user', 'reply_topic', 'reply_content', 'likes', 
    list_filter = 'reply_user', 'reply_topic', 
    list_display = 'id', 'reply_topic', 'reply_user', 'reply_timestamp_create', 'reply_timestamp_update',
    list_display_links = 'reply_user', 'reply_topic', 
    list_per_page = 10