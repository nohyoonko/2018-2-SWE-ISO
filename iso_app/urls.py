"""sow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #join
    path('join/', views.join),
    path('check_id/', views.check_id),
    path('join/register_userinfo_db/',views.register_userinfo_db),

    #login
    path('',views.login),
    path('login/', views.login),
    path('logout/', views.logout),
    path('check_login/', views.check_login),
    path('login_admin/', views.login_admin),
    path('mypage/', views.mypage),
    path('edit_mypage/', views.edit_mypage),
    path('edit_mypage_success/', views.edit_mypage_success),

    #notice 
    url(r'^.+/notice/$', views.notice_list),
    url(r'^.+/notice/(?P<pk>\d+)$', views.notice_detail),
    url(r'^.+/notice/new$', views.notice_new),
    url(r'^.+/notice/(?P<pk>\d+)/edit$', views.notice_edit),
    url(r'^.+/notice/(?P<pk>\d+)/delete$', views.notice_delete),

    #post
    url(r'^.+/post/$',views.post_new),
    url(r'^.+/post/(?P<pk>\d+)/edit$', views.post_edit),
    url(r'^.+/post/(?P<pk>\d+)/delete$', views.post_delete),

    #reference room
    url(r'^.+reference/upload', views.upload_file),
    url(r'^.+reference/delete/.+', views.delete_file),
    url(r'^.+reference/$', views.reference),
    url(r'^.+media/$', views.download),

    #calendar
    url(r'^.+/calendar/$', views.calendar),
    url(r'^.+/calendar/add_cal/$', views.add_cal),
     
    #class room
    path('create_room/', views.create_room), 
    path('create_room/register_class_db', views.register_class_db),
    url(r'^.+/main_teamroom$',views.main_teamroom),
    url(r'^.+/today/$',views.today),

    #participate
    url(r'^.+/participate/$',views.participate),
    #url(r'^.+/participate/delete$',views.par_delete),

    #setting
    url(r'^.+/setting/$',views.setting),
    url(r'^.+/setting/search/', views.search_member),
    url(r'^.+/setting/(?P<pk>.+)/add/$', views.add_member),
    url(r'^.+/setting/(?P<pk>.+)/sub/$', views.sub_member),
    url(r'^.+/edit_teamroom/$', views.edit_teamroom),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
