from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.

class ProjectProfile(models.Model):
    """
    项目组
    """
    name = models.CharField(max_length=30, verbose_name=_('项目组'),default="")
    owner = models.CharField(max_length=128,verbose_name=_('负责人'))
    class Meta:
        verbose_name = "项目组"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class UserProfile(AbstractUser):
    """
    用户
    """
    nickname = models.CharField(max_length=30,blank=True, verbose_name=_('姓名'),default='')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name=_('邮箱'))
    project = models.ForeignKey(ProjectProfile,null=True,blank=True,verbose_name=_('项目组'),
                                on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class HostProfile(models.Model):
    PLATFORM_CHOICES = (
        ('Physical', '物理机'),
        ('Virtual', '虚拟机'),
        ('Container', '容器'),
        ('Disk','硬盘')
    )
    hostname = models.CharField(max_length=32,verbose_name=_('主机名'))
    ip = models.CharField(max_length=16, primary_key=True,verbose_name=_('IP地址'))
    type = models.CharField(max_length=128, choices=PLATFORM_CHOICES,default='Virtual',
                            verbose_name=_('类型'))
    serial_number = models.CharField(max_length=32,null=True,blank=True,verbose_name=_('序列号'))
    asset_number = models.CharField(max_length=32,null=True,blank=True,verbose_name=_('资产号'))
    position = models.CharField(max_length=128,null=True,blank=True,verbose_name=_('位置'))
    project = models.ForeignKey(ProjectProfile,null=True,blank=True,verbose_name=_('项目组'),
                                on_delete=models.SET_NULL)
    owner = models.ForeignKey(UserProfile,null=True,blank=True,verbose_name=_('负责人'),
                              on_delete=models.SET_NULL)
    parent = models.ForeignKey("self", null=True, blank=True, verbose_name=_('宿主'),
                                 help_text="宿主",related_name="sub_cat",on_delete=models.CASCADE)
    idle = models.BooleanField(default=True,verbose_name=_('空闲'))
    class Meta:
        verbose_name = "资产"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip

