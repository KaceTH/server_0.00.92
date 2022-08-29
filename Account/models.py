from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class TimeStampedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):

    USER_TYPES = (
        (1, 'Student'),
        (2, 'Teacher'),
        (3, 'Parents')
    )
    
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=40, blank=True)
    school = models.CharField(max_length=100, default="Unnamed")
    
    user_type = models.IntegerField(choices=USER_TYPES, default=1, blank=True)

    grade_number = models.IntegerField(default=0)
    class_number = models.IntegerField(default=0)
    student_number = models.IntegerField(default=0)

    is_verificated = models.BooleanField(default=False, blank=True)
    pw_access_due = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username

    def change_password(self, new_pw, pw_check):
        if new_pw == pw_check :
            self.password = new_pw
            self.save()
            return True
        return False

    def is_able_to_change(self):
        if self.pw_access_due is None:
            return False
        print(f"{datetime.utcnow().date()} >= {self.pw_access_due.date()}")
        print(f"{datetime.utcnow().time()} >= {self.pw_access_due.time()}")
        if datetime.utcnow().date() >= self.pw_access_due.date():
            return datetime.utcnow().time() >= self.pw_access_due.time()
        return False

    def done_pw_access(self):
        self.pw_access_due = None
        self.save()


class Verification(TimeStampedModel) :
    author = models.ForeignKey(
        User, 
        models.CASCADE,
        "author", 
        blank=False,
        null=False,
    )
    code = models.IntegerField(null=False)
    expiration_date = models.DateTimeField(blank=True, null=True)
    usage = models.IntegerField(default=1, blank=True)

    def set_end_date(self):
        self.expiration_date = datetime.utcnow() + timedelta(days=0, minutes=10)
        self.save()
        print(f'date saved to {self.expiration_date}')
        return 

    def is_end_date(self):
        print(f"{datetime.utcnow().date()} >= {self.expiration_date.date()}")
        print(f"{datetime.utcnow().time()} >= {self.expiration_date.time()}")
        if datetime.utcnow().date() >= self.expiration_date.date():
            return datetime.utcnow().time() >= self.expiration_date.time()
        False

    def send_verification(self) :
        name = f'[{self.code}] 학생알리미 인증코드'
        message = f'학생알리미 인증코드입니다 [{self.code}]'
        send_mail(
            name, #title
            message, #message
            f'학생알리미 <{settings.EMAIL_HOST_USER}>', #from
            [self.author.email], #to
        )

