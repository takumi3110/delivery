from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, is_superuser, **extra_fields):
        if not username:
            raise ValueError('指定されたユーザー名を設定する必要があります')
        user = self.model(username=username, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('社員番号', max_length=30, unique=True)
    screenname = models.CharField('氏名', max_length=255)
    Department = models.CharField('部署', max_length=255, default="[]")
    Position = models.CharField('役職', max_length=20, default="[]")
    email = models.CharField('メールアドレス', max_length=255, default="[]")
    is_active = models.BooleanField('有効フラグ', default=True)
    is_staff = models.BooleanField('スタッフ', default=True)
    created_date = models.DateTimeField('登録日時', auto_now_add=True)
    modified_date = models.DateTimeField('更新日時', auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return str(self.screenname)

    def get_absolute_url(self):
        return reverse('user:myp', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = verbose_name

    def get_full_name(self):
        return str(self.screenname)

    get_short_name = get_full_name