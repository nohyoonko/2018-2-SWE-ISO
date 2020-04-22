import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template.context_processors import csrf
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.core import serializers
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import random, string
from django.http import JsonResponse
from .forms import *
from .models import *
from django.views.generic import ListView, TemplateView
from .serializers import *#event_serializer
 
# Create your views here.

#join
def join(request) :

    UserInfos = UserInfo.objects.all()
    context = {'UserInfos' : UserInfos}
    return render(request, 'login/join.html', context)

def check_id(request):

    if request.method == 'GET' :
        user_id = request.GET.get('user_id',None)

        try:
            userinfo_list = UserInfo.objects.get(user_id = user_id)
            result = {"result" : 'true'}
        except :
            result = {"result" : 'false'}

    return JsonResponse(result)


def register_userinfo_db(request):

    if request.method == 'POST':  
        user_name=request.POST['user_name']
        #user_name = request.POST.get('user_name', False);
        user_id = request.POST['user_id']
        user_psw = request.POST['user_psw']
        #user_email = request.POST.get('user_email', False);
        user_email=request.POST['user_email']
        user_pos=request.POST['user_pos']

        new_userinfo = UserInfo(user_name=user_name, user_id = user_id, user_psw = user_psw, user_email=user_email, user_pos=user_pos)
        #멤버 객체 생성 
        new_userinfo.save()

        return render(request, 'login/success.html')

#login
def login(request) :
    return render(request, 'login/login.html')#, context)

def login_admin(request): 
    user_id = request.session.get('user_id', False)
    user_name = request.session.get('user_name', False)
    user_pos=request.session.get('user_pos', False)
    userinfo = UserInfo.objects.get(user_id = user_id)

    return redirect('/mypage')

def check_login(request) :
    user_id = request.GET.get('id',None)
    user_psw = request.GET.get('psw',None)
    try :
        userinfo = UserInfo.objects.get(user_id = user_id)
        if userinfo.user_psw != user_psw :
            result = { "result" : "psw_failed"}
        else :
            request.session['login_complete'] = True
            request.session['user_id'] = user_id
            request.session['user_name'] = userinfo.user_name
            request.session['user_pos'] = userinfo.user_pos

            result = { "result" : "success" }

    except :
        result = { "result" : "id_failed" }
        
    return JsonResponse(result)

def logout(request) :
    request.session['login_complete'] = False
    unknown_userinfo = UserInfo(user_name='unknown', user_id = 'unknown', user_pos='unknown')
    context = { 'userinfo' : unknown_userinfo }
    return render(request, 'login/login.html', context)

# notice
# notice
def notice_list(request):
    id = request.path.split('/')[1]
    user_id=request.session.get('user_id', 'unknown')
    receiver=UserInfo.objects.get(user_id=user_id)
    team = TR.objects.get(class_id = id)
    notification=Notification.objects.filter(team=team, receiver=receiver)
    notices = Notice.objects.filter(team=team)
    member=Member.objects.get(user=user_id, team=team.class_id)
    content={'team':team,'user_id':user_id, 'notices':notices, 'notification':notification, 'member':member}
    return render(request, 'notice/notice_list.html', content)

def notice_detail(request, pk):
    id = request.path.split('/')[1]
    notice = get_object_or_404(Notice, pk=pk)
    user_id=request.session.get('user_id', 'unknown')
    receiver=UserInfo.objects.get(user_id=user_id)
    team = TR.objects.get(class_id = id)
    member=Member.objects.get(user=user_id, team=team.class_id)
    notification=Notification.objects.filter(team=team, receiver=receiver)
    content={'notice': notice, 'notification':notification, 'user_id':user_id, 'team':team, 'member':member}
    return render(request, 'notice/notice_detail.html', content)

def notice_new(request):
    id = request.path.split('/')[1]
    user_id=request.session.get('user_id', 'unknown')
    receiver=UserInfo.objects.get(user_id=user_id)
    team = TR.objects.get(class_id = id)
    notification=Notification.objects.filter(team=team, receiver=receiver)
    member=Member.objects.get(user=user_id, team=team.class_id)
    if request.method == 'POST':
        form = NoticeForm(request.POST)        
        if form.is_valid():
            notice = form.save(commit=False)
            notice.team=team
            notice.author = member
            notice.published_date = timezone.now()
            notice.save()
            return redirect('./'+str(notice.pk))
    else:
        form = NoticeForm()
    content={'form': form, 'notification':notification, 'user_id':user_id, 'team':team, 'member':member}
    return render(request, 'notice/notice_new.html', content)

def notice_edit(request, pk):
    id = request.path.split('/')[1]
    notice = get_object_or_404(Notice, pk=pk)
    user_id=request.session.get('user_id', 'unknown')
    receiver=UserInfo.objects.get(user_id=user_id)
    team = TR.objects.get(class_id = id)
    member=Member.objects.get(user=user_id, team=team.class_id)
    notification=Notification.objects.filter(team=team, receiver=receiver)
    if request.method == "POST":
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = member
            notice.published_date = timezone.now()
            notice.save()
            return redirect('../')
    else:
        form = NoticeForm(instance=notice)
    content={'form': form, 'notification':notification, 'user_id':user_id, 'team':team, 'member':member}
    return render(request, 'notice/notice_edit.html', content)

def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.delete()
    return redirect('../../notice')

# mainpage
def main_teamroom(request): 
    if request.method == 'GET' :
        id = request.path.split('/')[1]
        team = TR.objects.get(class_id = id)#정보
        user_id=request.session.get('user_id', 'unknown')
        member=Member.objects.get(user=user_id, team=team)
        candidates = UploadFileModel.objects.filter(team=team)
        receiver=UserInfo.objects.get(user_id=user_id)
        notification=Notification.objects.filter(team=team, receiver=receiver)
        content={'candidates':candidates, 'team':team, 'user_id':user_id, 'notification':notification, 'member':member}
        return render(request, 'room/main_teamroom.html', content)

def today(request):
    id = request.path.split('/')[1]
    team = TR.objects.get(class_id = id)
    cals=Calendar.objects.filter(team=team)
    if request.method == 'GET' :
        d = request.GET.get('d',None)
        m = request.GET.get('m',None)
        y = request.GET.get('y',None)
        buf_s=list()
        buf_e=list()
        title=list()
        for cal in cals:
            buf_s=cal.start.split(' ')
            buf_e=cal.end.split(' ')
            buf_s_int=int(buf_s[2])
            buf_e_int=int(buf_e[2])
            d_int=int(d)
            if (buf_s[3]==y or buf_e[3]==y) and (buf_s[1]==m or buf_e[1]==m) and (buf_s_int<=d_int and buf_e_int>=d_int):
                title.append(cal.title)
        result={'title':title, 'result':"success"}
        return JsonResponse(result)

# post
def post_new(request):  
    id = request.path.split('/')[1]
    user_id=request.session.get('user_id', 'unknown')
    receiver=UserInfo.objects.get(user_id=user_id)
    team = TR.objects.get(class_id = id)
    notification=Notification.objects.filter(team=team, receiver=receiver)
    members=Member.objects.filter(team=team)
    member=Member.objects.get(team=team, user_id=user_id)
    posts = Post.objects.filter(team=team)
    content={'team':team,'user_id':user_id, 'posts':posts, 'members':members, 'notification':notification, 'member':member}

    if request.method == 'POST':
        tag=request.POST.get('tag', 'unknown')
        text=request.POST.get('text', 'unknown')
        published_date=timezone.now()
        post=Post(team=team, tag = tag, text = text, author = member, published_date = published_date)
        post.save()

        sender=UserInfo.objects.get(user_id=user_id)
        receiver = UserInfo.objects.get(user_name=tag)
        notification=Notification(team=team, sender=sender, receiver=receiver, text=text, published_date = published_date)
        notification.save()

        return redirect('./')
        
    return render(request, 'post/post_new.html', content)

def post_edit(request, pk):
    id = request.path.split('/')[1]
    user_id=request.session.get('user_id', 'unknown')
    receiver=UserInfo.objects.get(user_id=user_id)
    team = TR.objects.get(class_id = id)
    text=request.session.get('text', 'unknown')
    members=Member.objects.filter(team=team)
    member=Member.objects.get(team=team, user_id=user_id)
    post = get_object_or_404(Post, pk=pk)
    published_date=request.session.get('published_date', post.published_date)  # 전에 저장했을 때 시간 
    notification=Notification.objects.filter(team=team, receiver=receiver)
    content={'team':team,'user_id':user_id, 'members':members, 'notification':notification, 'member':member}

    if request.method == 'POST':
        tag=request.POST.get('tag', 'unknown')
        text=request.POST.get('text', 'unknown')
        post=Post.objects.filter(published_date=published_date)
        date=timezone.now()
        post.update(team=team, tag = tag, text = text, author = member, published_date = date)
        
        sender=UserInfo.objects.get(user_id=user_id)
        receiver = UserInfo.objects.get(user_name=tag)
        notification=Notification.objects.filter(team=team, published_date=published_date)
        notification.update(text=text, receiver=receiver, published_date = date)
        return redirect('../')

    if request.method == 'GET':
        tag=request.session.get('tag', post.tag)
        text=request.session.get('text', post.text)
        post=Post(team=team, tag = tag, text = text, author = member, published_date = published_date)
        content={'team':team,'user_id':user_id, 'post':post, 'members':members, 'notification':notification, 'member':member}
        return render(request, 'post/post_edit.html', content)

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    notification = get_object_or_404(Notification, pk=pk)
    notification.delete()
    return redirect('../../post')

#reference room
def reference(request):
    id = request.path.split('/')[1]
    user_id=request.session.get('user_id', 'unknown')
    receiver=UserInfo.objects.get(user_id=user_id)
    team = TR.objects.get(class_id = id)
    member=Member.objects.get(team=team, user_id=user_id)
    notification=Notification.objects.filter(team=team, receiver=receiver)
    if request.method == 'GET' :
        candidates = UploadFileModel.objects.filter(team=team)
        context = {'candidates':candidates,'team':team, 'user_id':user_id, 'notification':notification, 'member':member}
        return render(request, 'reference/success.html', context)

def upload_file(request):
    id = request.path.split('/')[1]
    user_id=request.session.get('user_id', 'unknown')
    receiver=UserInfo.objects.get(user_id=user_id)
    team = TR.objects.get(class_id = id)
    notification=Notification.objects.filter(team=team, receiver=receiver)
    member=Member.objects.get(user=user_id, team=team.class_id)
    content={'team':team, 'member':member, 'user_id':user_id, 'notification':notification}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            ref = form.save(commit=False)
            ref.team=team
            ref.member= member
            ref.save() 
            candidates = UploadFileModel.objects.filter(team=team) # 업로드된 파일들의 이름과 파일 정보 전송 
            content = {'candidates':candidates,'team':team, 'user_id':user_id, 'notification':notification, 'member':member}
            return redirect('./')
            #return render(request, 'reference/success.html', context)
    if request.method == 'GET' :
        form = UploadFileForm()
        content = {'form': form, 'team':team, 'user_id':user_id, 'notification':notification, 'member':member}
        return render(request, 'reference/upload.html', content)

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def delete_file(request):
    id = request.path.split('/')[1]
    user_id=request.session.get('user_id', 'unknown')
    receiver=UserInfo.objects.get(user_id=user_id)
    team = TR.objects.get(class_id = id)
    notification=Notification.objects.filter(team=team, receiver=receiver)

    file = request.path.split('/')[4]
    delete_file = UploadFileModel.objects.filter(team=team, file=file)
    delete_file.delete()
    return redirect('../')

#mypage
def mypage(request) :
    if request.method == 'GET':
        user_id=request.session.get('user_id', 'unknown')
        user_name=request.session.get('user_name', 'unknown')
        member=Member.objects.filter(user_id=user_id)
        return render(request, 'room/mypage.html', {'member':member, 'user_name':user_name})

def edit_mypage(request):
    if request.method == 'GET':
        user_id=request.session.get('user_id', False)
        user_name=request.session.get('user_name', False)
        userinfo = UserInfo(user_name=user_name, user_id = user_id)

        return render(request, 'room/edit_mypage.html', {'userinfo':userinfo})

def edit_mypage_success(request):
    if request.method == 'POST':
        user_id=request.session.get('user_id', False)
        userinfo = UserInfo.objects.filter(user_id=user_id)
        user_psw=request.POST.get('user_psw',False)
        user_email=request.POST.get('user_email',False)
        user_pos=request.POST.get('user_pos',False)

        userinfo.update(user_psw=user_psw,
        user_email=user_email,
        user_pos=user_pos)

        return redirect('../mypage/')

#class room
def create_room(request):
    if request.method == 'GET' :
        user_id = request.session.get('user_id', 'unknown')
        user_name = request.session.get('user_name', 'unknown')
        userinfo = UserInfo(user_name=user_name, user_id = user_id)
        context = { 'userinfo' : userinfo }

        return render(request, 'room/create_room.html', context)

def register_class_db(request):
    if request.method == 'POST':
        user_id=request.session.get('user_id', 'unknown')
        user_name=request.session.get('user_name', 'unknown')

        project=request.POST['project']
        subject = request.POST['subject']
        team = request.POST['team']
        new_class = TR(project=project, subject = subject, team = team)
        new_class.save()

        userinfo=UserInfo(user_id=user_id)

        new_member=Member(user_id=user_id, team=new_class)
        new_member.save()

        return redirect('../mypage/')

#setting
def setting(request):
    id = request.path.split('/')[1]
    user_id=request.session.get('user_id', 'unknown')
    receiver=UserInfo.objects.get(user_id=user_id)
    team = TR.objects.get(class_id = id)
    notification=Notification.objects.filter(team=team,receiver=receiver)
    if request.method == 'GET': 
        members = Member.objects.filter(team=team)
        member=Member.objects.get(team=team, user_id=user_id)
        content={'team':team, 'members':members, 'user_id':user_id, 'notification':notification, 'member':member}
        return render(request, 'room/setting.html', content)

def edit_teamroom(request):
    id = request.path.split('/')[1]
    user_id=request.session.get('user_id', 'unknown')
    receiver=UserInfo.objects.get(user_id=user_id)
    team = TR.objects.get(class_id = id)
    notification=Notification.objects.filter(team=team, receiver=receiver)
    Team = TR.objects.filter(class_id = id)
    if request.method == 'POST':
        project=request.POST.get('project',False)
        subject=request.POST.get('subject',False)
        team=request.POST.get('team',False)
        leader=request.POST.get('leader',False)
        team_par=request.POST.get('team_par',False)
        par=int(request.POST.get('par',False))
        team_update = TR.objects.get(class_id = id)
        #팀참여도
        Mem=Member.objects.filter(team=team_update, user=team_par)
        Mem.update(participate=par)
 
        Team.update(project=project,
        subject=subject,
        team=team)        

        members=Member.objects.filter(team=team_update)
        members.update(is_leader=False)#다시 false로 했다가
        member_l = Member.objects.filter(team=team_update, user=leader)
        member_l.update(is_leader=True)#팀장으로 지정된 사람만.

        return redirect('../setting/')

def search_member(request):
    id = request.path.split('/')[1]
    user_id=request.session.get('user_id', 'unknown')
    receiver=UserInfo.objects.get(user_id=user_id)
    team = TR.objects.get(class_id = id)
    notification=Notification.objects.filter(team=team, receiver=receiver)
    member=Member.objects.get(user=user_id, team=team.class_id)
    if request.method=="GET":
        users = UserInfo.objects.all()
        q = request.GET.get('q','')
        if q :
            users = users.filter(user_id=q)
        return render(request, 'room/add_member.html', { 'team' : team, 'users': users, 'q' : q, 'user_id':user_id, 'notification':notification, 'member':member})

def add_member(request, pk):
    if request.method=="GET":
        id = request.path.split('/')[1]
        i=0
        team = TR.objects.get(class_id = id)
        members=Member.objects.filter(team=team).values_list()
        for mem in members:
            if mem[1] == pk:
                i=1
            else:
                continue
        if i!=1:   
            member=Member(user_id=pk,team=team,)
            member.save()
        return redirect('../../')
 
def sub_member(request, pk):
    member = get_object_or_404(Member, pk=pk) # 속한 멤버만 보이도록 바꿔야함 
    #if(confirm('정말 삭제?')) :
    member.delete()
    return redirect('../../../setting')


#participate 
def participate(request):
    id = request.path.split('/')[1]
    user_id=request.session.get('user_id', 'unknown')
    receiver=UserInfo.objects.get(user_id=user_id)
    team = TR.objects.get(class_id = id)#정보
    notification=Notification.objects.filter(team=team, receiver=receiver)
    if request.method == 'GET' :
        members=Member.objects.filter(team=team)
        member=Member.objects.get(team=team, user_id=user_id)
        pars=Participate.objects.filter(team=team)
        content={'team':team,'user_id':user_id, 'members':members,  'notification':notification, 'member':member, 'pars':pars}
        return render(request, 'team_p/participate.html', content)
    else:
        text=request.POST.get('text', 'unknown')
        par=Participate(team=team, text = text)
        par.save()
        return redirect('./')
"""
def par_delete(request):
    id = request.path.split('/')[1]
    team = TR.objects.get(class_id = id)
    text=request.session.get('text', 'unknown')
    print(text)
    par=Participate.objects.filter(team=team, text=text)
    par.delete()
    return redirect('./')
"""
#calendar 
def calendar(request):
    id = request.path.split('/')[1]
    team = TR.objects.get(class_id = id)#정보
    user_id=request.session.get('user_id', 'unknown')
    member=Member.objects.get(team=team, user_id=user_id)
    receiver=UserInfo.objects.get(user_id=user_id)
    notification=Notification.objects.filter(team=team,receiver=receiver)
    cals=Calendar.objects.filter(team=team).values_list('title')#, 'start', 'end')
    content={'team':team,'user_id':user_id, 'notification':notification, 'cals':cals, 'member':member}
    return render(request, 'calendar/calendar.html', content)
    
def add_cal(request):
    id = request.path.split('/')[1]
    team = TR.objects.get(class_id = id)
    if request.method == 'GET' :
        title = request.GET.get('title',None)
        start = request.GET.get('start',None)
        end = request.GET.get('end',None)
        new_cal = Calendar(title=title, team=team, start=start, end=end)
        new_cal.save()
        result = { "result" : "success" }
        return JsonResponse(result)
        
