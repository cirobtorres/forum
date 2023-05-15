from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    path(route='', view=views.home, name='home'),
    path(route='session/<int:session_id>/', view=views.session, name='session'),
    path(route='session/<int:session_id>/topic/<int:topic_id>/', view=views.topic, name='topic'),
    path(route='reply-to/<int:session_id>/topic/<int:topic_id>/', view=views.reply, name='reply'),
    path(route='topic-creation/<int:session_id>/', view=views.topic_creation, name='topic_creation'),
    path(route='topic-create/<int:session_id>/', view=views.topic_confirm, name='topic_confirm'),
    path(route='delete-topic/<int:session_id>/topic/<int:topic_id>/', view=views.topic_delete, name='topic_delete'),
    path(route='delete-reply/<int:session_id>/topic/<int:topic_id>/<int:reply_id>/', view=views.reply_delete, name='reply_delete'),
    path(route='search-tag/<str:tag_name>/<int:tag_id>/', view=views.search_by_tag, name='tag'),
    path(route='search/', view=views.search_list_view, name='query'),
    path(route='like/<int:session_id>/<int:topic_id>/', view=views.like_topic, name='like_topic'),
    path(route='like/<int:session_id>/<int:topic_id>/<int:reply_id>/', view=views.like_reply, name='like_reply'),
]