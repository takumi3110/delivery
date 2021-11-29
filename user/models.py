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


class Unit(models.Model):
    name = models.CharField(verbose_name="グループ名", max_length=100, unique=True)
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="グループ管理者")
    memo = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Unit_Member(models.Model):
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE,
        verbose_name="所属グループ名"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Unit_request(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="申請ユーザー"
    )
    join_Unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE,
        verbose_name="申請グループ",
        related_name="req_joinUnit",
    )
    Date = models.DateTimeField(
        default=timezone.now,
        verbose_name='申請日',
        blank=True, null=True,
    )
    end_Date = models.DateTimeField(
        verbose_name='追加日',
        blank=True, null=True,
    )
    memo = models.TextField(
        blank=True, null=True,
        verbose_name='メモ'
    )
    Flg = models.BooleanField(
        verbose_name="作業フラグ",
        default=False,
    )

    def __str__(self):
        return "%s" % self.user.get_full_name()


class Unit_history(models.Model):
    Work_cho = (
        ("1", "グループ作成依頼"),
        ("2", "グループ参加申請"),
        ("3", "グループ作成"),
        ("4", "グループメンバー追加"),
        ("5", "グループメンバー削除"),
        ("6", "参加申請拒否"),
    )
    status = models.CharField(choices=Work_cho, max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.CharField(max_length=150, null=True, blank=True)
    Date = models.DateTimeField(
        default=timezone.now,
        verbose_name='案件作成日',
        blank=True, null=True,
    )
    memo = models.TextField(
        null=True, blank=True,
        verbose_name="備考",
    )

    def __str__(self):
        return "%s %s" % (self.status, self.user)


class conf(models.Model):
    stt_cho = (
        ('1', 'AmiVoice'),
        ('2', 'GCP')
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True
    )
    Default_stt = models.CharField(
        max_length=20, choices=stt_cho,
        default='1',
    )
    Default_conf = models.BooleanField(
        default=False,
        verbose_name='初期設定フラグ',
    )
    def __str__(self):
        return str(self.user)
