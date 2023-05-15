import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models.aggregates import Count

from ..forum.models import Reply, Topic
from .models import User
from .forms import (
    LoginForm, 
    UpdateUserForm, 
    UpdateAccountForm, 
    RegisterUserForm, 
    RegisterAccountForm, 
    )

from utils.pagination import pagination_func

PER_PAGE_DASHBOARD_VIEW_REPLIES = int(os.environ.get('PER_PAGE_DASHBOARD_VIEW_REPLIES', 10))

def register_access(request):
    template_name = 'global/content/register.html'
    keep_session_data = request.session.get('keep_session_data', None)
    if not request.session.get('get_previously_url', False):
        request.session['get_previously_url'] = request.META.get('HTTP_REFERER', '/')
    user_form = RegisterUserForm(keep_session_data)
    account_form = RegisterAccountForm(keep_session_data)
    context = {
        'user_form': user_form, 
        'account_form': account_form, 
        'form_confirmation': reverse(viewname='account:register_confirm'), 
    }
    return render(request=request, template_name=template_name, context=context,)


def register_confirm(request: HttpRequest) -> HttpResponse:
    if not request.POST:
        return Http404()
    request.session['keep_session_data'] = request.POST
    get_previously_url = request.session.get('get_previously_url', reverse(viewname='forum:home'))
    user_form = RegisterUserForm(data=request.POST or None,)
    account_form = RegisterAccountForm(data=request.POST or None, files=request.FILES or None,)
    if user_form.is_valid() and account_form.is_valid():
        user = user_form.save()
        user.refresh_from_db()
        user.account.birth_date = account_form.cleaned_data.get('birth_date', '')
        user.account.gender = account_form.cleaned_data.get('gender', '')
        user.account.city = account_form.cleaned_data.get('city', '')
        user.account.state = account_form.cleaned_data.get('state', '')
        user.account.img = account_form.cleaned_data.get('img', None)
        username = user_form.cleaned_data.get('username', '')
        password = user_form.cleaned_data.get('password', '')
        user.set_password(password)
        user.save()
        autentication = authenticate(
            username=username,
            password=password,
            )
        if autentication is not None:
            messages.success(request=request, message=f'Bem vindo {autentication.username}!')
            login(request=request, user=autentication)
        del request.session['keep_session_data']
        return redirect(to=get_previously_url)
    return redirect(to=reverse(viewname='account:register_access'))


def login_access(request: HttpRequest) -> HttpResponse:
    # if request.user.is_anonymous:
    if 'next' in request.GET:
        messages.error(request=request, message='Você precisa estar cadastrado para poder visualizar o perfil de outros usuários')
        return redirect(to=reverse(viewname='account:login_access'))
    login_session_data = request.session.get('login_session_data', None)
    if not request.session.get('get_previously_url', False):
        request.session['get_previously_url'] = request.META.get('HTTP_REFERER', False)
    form = LoginForm(login_session_data or None)
    context = {'form': form, 'form_confirmation': reverse(viewname='account:login_confirm'),}
    return render(request=request, template_name='global/content/login.html',context=context,)


def login_confirm(request: HttpRequest) -> HttpResponse:
    if not request.POST:
        raise Http404()
    request.session['login_session_data'] = request.POST
    get_previously_url = request.session.get('get_previously_url', reverse('forum:home'))
    form = LoginForm(request.session['login_session_data'] or None)
    if form.is_valid():
        autentication = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
            )
        if autentication is not None:
            messages.success(request=request, message=f'Bem vindo de volta, {autentication.username}!')
            login(request=request, user=autentication)
            del request.session['login_session_data']
            return redirect(to=get_previously_url)
        messages.error(request=request, message='Usuário ou senha inválidos')
        return redirect(to=reverse(viewname='account:login_access'))
    messages.error(request=request, message='Formulário inválido')
    return redirect(to=reverse(viewname='account:login_access'))


@login_required(login_url='account:login_access', redirect_field_name='next')
def logout_view(request: HttpRequest) -> HttpResponse:
    if not request.POST:
        messages.error(request=request, message='Requisição de log out inválida')
        return redirect(to=reverse(viewname='account:login_access'))
    elif request.POST.get('username') != request.user.username:
        messages.error(request=request, message='Usuário de log out inválido')
        return redirect(to=reverse(viewname='forum:home'))
    else:
        logout(request)
        messages.success(request=request, message='Log out com sucesso!')
        return redirect(to=reverse(viewname='forum:home'))


@login_required(login_url='account:login_access', redirect_field_name='next')
def dashboard(request: HttpRequest, name: str, id: int) -> HttpResponse:
    template_name = 'global/content/dashboard.html'
    user_form = UpdateUserForm(instance=request.user)
    account_form = UpdateAccountForm(instance=request.user.account)
    user_topics_overview = Topic.objects.filter(topic_user__id=id).order_by('-topic_timestamp_create')
    user_replies = Reply.objects.filter(reply_user_id=id).order_by('-reply_timestamp_create')
    context = {
        'user_form': user_form, 
        'account_form': account_form,
        'user_topics_overview': user_topics_overview, 
        'user_replies': user_replies, 
    }
    return render(request=request, template_name=template_name, context=context,)


@login_required(login_url='account:login_access', redirect_field_name='next')
def update_confirm(request: HttpRequest, name: str, id: int) -> HttpResponse:
    if not request.POST:
        return Http404()
    user_form = UpdateUserForm(data=request.POST, instance=request.user)
    account_form = UpdateAccountForm(data=request.POST, files=request.FILES, instance=request.user.account)
    if user_form.is_valid() and account_form.is_valid():
        user = user_form.save()
        user.account.birth_date = account_form.cleaned_data.get('birth_date', '')
        user.account.gender = account_form.cleaned_data.get('gender', '')
        user.account.city = account_form.cleaned_data.get('city', '')
        user.account.state = account_form.cleaned_data.get('state', '')
        user.account.img = account_form.cleaned_data.get('img', '')
        user.save()
        messages.success(request=request, message='Seus dados foram atualizados com sucesso!')
        return redirect(to=reverse(viewname='account:dashboard', kwargs={'name': name, 'id': id,}))
    messages.error(request=request, message='Seus dados não são válidos')
    return redirect(to=reverse(viewname='account:dashboard', kwargs={'name': name, 'id': id,}))


@login_required(login_url='account:login_access', redirect_field_name='next')
def dashboard_view(request: HttpRequest, name: str, id: int) -> HttpResponse:
    template_name = 'global/content/dashboard-view.html'
    member_user = User.objects.filter(id=id).first()
    member_topics = Topic.objects.filter(topic_user__id=member_user.id).order_by('-topic_timestamp_create')
    member_replies = Reply.objects.filter(reply_user__id=member_user.id).order_by('-reply_timestamp_create')
    member_replies.annotate(current_page='')  # Incompleto!
    # Precisa haver um "annotate" de "current_page" de cada "reply" em "member_replies"
    pagination = pagination_func(request=request, object_parse=member_replies, per_page=PER_PAGE_DASHBOARD_VIEW_REPLIES)
    total_likes = member_topics.aggregate(total_topics=Count('likes')).get('total_topics') + \
        member_replies.aggregate(total_replies=Count('likes')).get('total_replies')
    context = {'member_user': member_user, 'member_topics': member_topics, 'pagination': pagination, 'total_likes': total_likes,}
    return render(request=request, template_name=template_name, context=context,)


# ---------------------------------------- INCOMPLETO ----------------------------------------
@login_required(login_url='account:login_access', redirect_field_name='next')
def dashboard_view_home(request: HttpRequest) -> HttpResponse:
    return HttpResponse(True)


@login_required(login_url='account:login_access', redirect_field_name='next')
def dashboard_view_data(request: HttpRequest) -> HttpResponse:
    return HttpResponse(True)


@login_required(login_url='account:login_access', redirect_field_name='next')
def dashboard_view_activities(request: HttpRequest) -> HttpResponse:
    return HttpResponse(True)
# --------------------------------------------------------------------------------------------


def members_all(request: HttpRequest) -> HttpResponse:
    template_name = 'global\content\members.html'
    members = User.objects.get_user_info('username')
    context = {'members': members,}
    return render(request=request, template_name=template_name, context=context,)


def members_staffs(request: HttpRequest) -> HttpResponse:
    template_name = 'global\content\members.html'
    members = User.objects.get_user_info('username').filter(is_staff=True)
    context = {'members': members,}
    return render(request=request, template_name=template_name, context=context,)


def members_topics(request: HttpRequest) -> HttpResponse:
    template_name = 'global\content\members.html'
    members = User.objects.get_user_info('-total_topics')
    main = [i.total_topics for i in members]  # ME APAGUE
    context = {'members': members, 'main': main,}
    return render(request=request, template_name=template_name, context=context,)


def members_replies(request: HttpRequest) -> HttpResponse:
    template_name = 'global\content\members.html'
    members = User.objects.get_user_info('-total_replies')
    context = {'members': members,}
    return render(request=request, template_name=template_name, context=context,)


def members_likes(request: HttpRequest) -> HttpResponse:
    template_name = 'global\content\members.html'
    members = User.objects.get_user_info('-total_likes')
    context = {'members': members,}
    return render(request=request, template_name=template_name, context=context,)