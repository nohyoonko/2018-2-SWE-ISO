from django import forms
from .models import *#UploadFileModel, Post, Member
from django.contrib.auth.models import User

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFileModel
        fields = ('file',)

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('tag', 'text',)

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('title', 'text',)

class LoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password'] # 로그인 시에는 유저이름과 비밀번호만 입력 받는다.
