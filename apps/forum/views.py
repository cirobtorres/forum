import os

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import Http404, HttpRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from utils.pagination import pagination_func

from .forms import ReplyForm, CreateTopicForm
from .models import Forum, Reply, Session, Topic

PER_PAGE_SESSION = int(os.environ.get('PER_PAGE_SESSION', 10))
PER_PAGE_TOPIC = int(os.environ.get('PER_PAGE_TOPIC', 9))
PER_PAGE_SEARCH = int(os.environ.get('PER_PAGE_SEARCH', 10))
PER_PAGE_SEARCH_BY_TAG = int(os.environ.get('PER_PAGE_SEARCH_BY_TAG', 10))

def home(request: HttpRequest) -> HttpResponse:
    template_name = 'global/content/home.html'
    dict_data = {}
    for forum in Forum.objects.all().values('id', 'forum_title', 'forum_description'):
        sessions = Session.objects \
            .filter(session_forum_id=forum.get('id', None)) \
                .values('id', 'session_title', 'session_description') \
                    .annotate(total_topics=Count('topic', distinct=True)) \
                        .annotate(total_replies=Count('topic__reply'))
        sessions_dict = {}
        for session in sessions:
            topics = Topic.objects \
                .filter(topic_session_id=session.get('id', None), fixed=True,) \
                    .annotate(
                last_reply_id=Reply.objects.subquery('id'), # latest
                last_reply_user_id=Reply.objects.subquery('reply_user_id'), # latest
                last_reply_username=Reply.objects.subquery('reply_user__username'), # latest
                last_reply_timestamp=Reply.objects.subquery('reply_timestamp_create'), # latest
                total_replies=Count('reply__reply_content'),
                )
            topic_list = []
            for topic in topics:
                try:
                    reply = Reply.objects.filter(reply_topic_id=topic.id)
                    paginator = pagination_func(request, reply, PER_PAGE_TOPIC)
                    topic_list.append((topic, paginator,))
                except ObjectDoesNotExist:
                    pass
            sessions_dict.update({session.get('session_title', None): (session, topic_list,),})
        dict_data.update({forum.get('forum_title', None): (forum, sessions_dict),})
    topics = Topic.objects.aggregate(topics=Count('id'))
    replies = Reply.objects.aggregate(replies=Count('id'))
    users = User.objects.aggregate(users=Count('id'))
    total = topics, replies, users,
    topic_feed = Topic.objects.order_by('-topic_timestamp_create')[:50]
    context = {'dict_data': dict_data, 'total': total, 'topic_feed': topic_feed,}
    return render(request=request, template_name=template_name, context=context,)


def session(request: HttpRequest, session_id: int) -> HttpResponse:
    template_name = 'global/content/session.html'
    session = Session.objects.get(id=session_id)
    topics = Topic.objects.filter(topic_session_id=session_id).annotate(
        reply_count=Count('reply'),
        last_reply_id=Reply.objects.subquery('reply_user_id'),
        last_reply_username=Reply.objects.subquery('reply_user__username'),
        last_reply_timestamp=Reply.objects.subquery('reply_timestamp_create')).order_by('-fixed', 'last_reply_timestamp' or 'topic_timestamp_create',)
    pagination = pagination_func(request, topics, PER_PAGE_SESSION)
    breadcrumb = session, 
    context = {'session': session, 'pagination': pagination, 'staff_only': session.staff_only, 'breadcrumb': breadcrumb,}
    return render(request=request,template_name=template_name,context=context,)

def topic(request: HttpRequest, session_id: int, topic_id: int) -> HttpResponse:
    template_name = 'global/content/topic.html'
    reply_form = ReplyForm()
    session = Session.objects.get(id=session_id)
    topic = Topic.objects.filter(id=topic_id).first()
    replies = Reply.objects.filter(reply_topic_id=topic.id)
    pagination = pagination_func(request, replies, PER_PAGE_TOPIC)
    topic_likes = User.objects.filter(id__in=Topic.objects.filter(id=topic_id).values('likes'))
    total_likes = get_object_or_404(Topic, id=topic_id).total_likes()
    likes = topic_likes, total_likes,
    tags = Topic.objects.filter(id=topic_id).values('tag', 'tag__name')
    breadcrumb = session, topic, 
    if request.session.get('topic_id', False) != topic.id:
        request.session['topic_id'] = topic.id
        topic.views += 1
        topic.save(update_fields=['views'])
    context = {
        'topic': topic, 'num_pages': pagination[1], 'pagination': pagination, 
        'reply_form': reply_form, 'likes': likes, 'tags': tags, 'breadcrumb': breadcrumb, 
        }
    return render(request=request, template_name=template_name, context=context,)


def search_list_view(request: HttpRequest,) -> HttpResponse:
    template_name = 'global/content/search-list.html'
    query = request.GET.get('q', '')
    topic_query = Topic.objects.filter(
        Q(topic_user__username__icontains=query) | 
        Q(topic_title__icontains=query)
    ).order_by('-topic_timestamp_create')
    total = topic_query.count()
    pagination = pagination_func(request, topic_query, PER_PAGE_SEARCH)
    context = {'query_title': query, 'query': query, 'total': total, 'num_pages': pagination[1], 'pagination': pagination,}
    return render(request=request, template_name=template_name, context=context,)


def topic_creation(request: HttpRequest, session_id: int) -> HttpResponse:
    template_name = 'global/content/topic-creation.html'
    form = CreateTopicForm(request.POST or None)
    session = Session.objects.get(id=session_id)
    breadcrumb = session, 
    context = {'form': form,'session_id': session_id, 'session': session, 'breadcrumb': breadcrumb, 
               'form_confirmation': reverse(viewname='forum:topic_confirm', kwargs={'session_id': session_id})}
    return render(request=request, template_name=template_name, context=context,)


def topic_confirm(request: HttpRequest, session_id: int) -> HttpResponse:
    if not request.POST:
        return Http404()
    form = CreateTopicForm(request.POST or None)
    if form.is_valid():
        new_topic = form.save(commit=False)
        new_topic.topic_user = request.user
        new_topic.topic_session = Session.objects.get(id=session_id)
        new_topic.save()
        new_topic.tag.add(*(tag for tag in form.cleaned_data.get('tag', '')))
        messages.success(request=request, message='Tópico criaco com sucesso!')
        return redirect(to=reverse(viewname='forum:topic', kwargs={'session_id': session_id, 'topic_id': new_topic.id,}))
    messages.error(request=request, message='ERRO! Tópico não criado')
    return redirect(to=reverse(viewname='forum:topic_creation', kwargs={'session_id': session_id,}))


def topic_delete(request: HttpRequest, session_id: int, topic_id: int) -> HttpResponse:
    if not request.POST:
        return Http404()
    topic = Topic.objects.get(id=topic_id)
    topic.delete()
    messages.success(request=request, message='Tópico apagado com sucesso')
    return redirect(to=reverse(viewname='forum:session', kwargs={'session_id': session_id,},))


def reply(request: HttpRequest, session_id: int, topic_id: int) -> HttpResponse:
    if not request.POST:
        return Http404()
    form = ReplyForm(request.POST or None)
    topic = Topic.objects.filter(id=topic_id).first()

    # When someone's comment starts a new page, "last_page" must update to "next_page"
    num_elem_on_page = int(request.POST.get('num_elem_on_page'))
    last_page = int(request.POST.get('url_dispatcher'))
    next_page = last_page + 1 if num_elem_on_page % PER_PAGE_TOPIC == 0 else last_page
    next_page = str(next_page)
    
    if form.is_valid():
        new_reply = form.save(commit=False)
        new_reply.reply_user = request.user
        if topic.block and not new_reply.reply_user.is_staff:
            messages.error(
                request=request, 
                message='Você previsa de privilégios de administrador para comentar' + \
                    ' aqui porque este tópico foi bloqueado por um moderador!'
                    )
            return redirect(to=request.META.get('HTTP_REFERER'))
        new_reply.reply_topic = topic
        new_reply.reply_content = form.cleaned_data.get('reply_content', '')
        form.save()
        messages.success(request=request, message='Comentário enviado com sucesso!')
        # return redirect(to=request.META.get('HTTP_REFERER'))
        return redirect(to=f'/session-{session_id}/topic-{topic_id}/?page={next_page}')
    messages.error(request=request, message='Comentário inválido')
    return redirect(to=f'/session-{session_id}/topic-{topic_id}/?page={last_page}')


def reply_delete(request: HttpRequest, session_id: int, topic_id: int, reply_id: int) -> HttpResponse:
    if not request.POST:
        return Http404()
    reply = Reply.objects.get(id=reply_id)
    reply.delete()
    messages.success(request=request, message='Seu comentário foi apagado')
    return redirect(to=reverse(viewname='forum:topic', kwargs={'session_id': session_id, 'topic_id': topic_id}))


def search_by_tag(request: HttpRequest, tag_name: str, tag_id: int) -> HttpResponse:
    template_name = 'global/content/search-by-tag.html'
    topics = Topic.objects.filter(tag=tag_id).order_by('-topic_timestamp_create')
    pagination = pagination_func(request, topics, PER_PAGE_SEARCH_BY_TAG)
    context = {'pagination': pagination, 'tag': [tag_id, tag_name,],}
    return render(request=request, template_name=template_name, context=context,)


def like_topic(request: HttpRequest, session_id: int, topic_id: int) -> HttpResponse:
    topic = get_object_or_404(Topic, id=request.POST.get('topic_id'))  # topic_id é o nome do button em like_topic_thumbs_up.html
    if topic.likes.filter(id=request.user.id).exists():
        topic.likes.remove(request.user)
    else:
        topic.likes.add(request.user)
    return redirect(to=reverse(viewname='forum:topic', kwargs={'session_id': session_id, 'topic_id': topic_id,}))


def like_reply(request: HttpRequest, session_id: int, topic_id: int, reply_id: int) -> HttpResponse:
    reply = get_object_or_404(Reply, id=request.POST.get('reply_id'))  # reply_id é o nome do button em like_reply_thumbs_up.html
    if reply.likes.filter(id=request.user.id).exists():
        reply.likes.remove(request.user)
    else:
        reply.likes.add(request.user)
    return redirect(to=reverse(viewname='forum:topic', kwargs={'session_id': session_id, 'topic_id': topic_id,}))
