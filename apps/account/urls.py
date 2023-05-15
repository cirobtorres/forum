from django.urls import path

from . import views

app_name = 'account'


urlpatterns = [
    path(route='login/', view=views.login_access, name='login_access'),
    path(route='login/confirm/', view=views.login_confirm, name='login_confirm'),
    path(route='register/', view=views.register_access, name='register_access'),
    path(route='register/confirm/', view=views.register_confirm, name='register_confirm'),
    path(route='update/<str:name>/<int:id>/', view=views.update_confirm, name='update_confirm'),
    path(route='logout/', view=views.logout_view, name='logout_view'), 
    path(route='dashboard/<str:name>/<int:id>/', view=views.dashboard, name='dashboard'),
    path(route='dashboard-view/<str:name>/<int:id>/', view=views.dashboard_view, name='dashboard_view'), 
    path(route='members/', view=views.members_all, name='members_all'), 
    path(route='members/staffs/', view=views.members_staffs, name='members_staffs'), 
    path(route='members/topics/', view=views.members_topics, name='members_topics'), 
    path(route='members/replies/', view=views.members_replies, name='members_replies'), 
    path(route='members/likes/', view=views.members_likes, name='members_likes'), 
]