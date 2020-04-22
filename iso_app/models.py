from django.db import models
from django.utils import timezone

# Create your models here.

class UserInfo(models.Model) :
    user_name=models.CharField(max_length=50, default= "")
    user_id = models.CharField(primary_key=True, max_length=50, default= "")
    user_psw = models.CharField(max_length=50, default = "")
    user_email=models.CharField(max_length=50, default= "")
    user_pos=models.CharField(max_length=50, default= "")

    def __str__(self):
        return self.user_id

class TR(models.Model):
    class_id=models.AutoField(primary_key=True)
    project=models.CharField(max_length=50, default="프로젝트")
    subject=models.CharField(max_length=50, default="과목")
    team=models.CharField(max_length=50, default="팀")

    def __str__(self):
        return self.project

class Member(models.Model):
    member_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    team=models.ForeignKey(TR, on_delete=models.CASCADE)#복합키 지원 안함
    participate=models.IntegerField(default=100)
    role=models.CharField(max_length=50, default="역할")
    is_leader=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.member_id)

class UploadFileModel(models.Model):
    file_id=models.AutoField(primary_key=True)
    team=models.ForeignKey(TR, on_delete=models.CASCADE)
    #group=models.ForeignKey(FileFolder, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    file = models.FileField(null=True)#upload_to='message/%Y/%m/%d/' : 경로가 이렇게 생김 ex)message/2018/11/09/센서2.jpg
        
class Post(models.Model):
    team=models.ForeignKey(TR, on_delete=models.CASCADE)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    tag = models.CharField(max_length=50)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Notice(models.Model):
    team=models.ForeignKey(TR, on_delete=models.CASCADE)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Notification(models.Model):
    team=models.ForeignKey(TR, on_delete=models.CASCADE)
    sender=models.ForeignKey(UserInfo, related_name='sender', on_delete=models.CASCADE) #ME
    receiver=models.ForeignKey(UserInfo, related_name='receiver', on_delete=models.CASCADE) #YOU
    text=models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
    def __str__(self):
        return self.text

class Calendar(models.Model):
    cal_id = models.AutoField(primary_key=True)
    team = models.ForeignKey(TR, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Participate(models.Model):
    par_id= models.AutoField(primary_key=True)
    team=models.ForeignKey(TR, on_delete=models.CASCADE)
    text=models.TextField()

    def __str__(self):
        return self.text
