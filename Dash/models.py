from django.db import models
from django_db_logger.models import StatusLog
# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=32, unique=True)
    permissions = models.ManyToManyField('Permission', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Role'

class UserInfo(models.Model):
    name = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'UserInfo'

class Permission(models.Model):
    name = models.CharField(max_length=32, unique=True)
    url = models.URLField(max_length=128, unique=True)
    perm_code = models.CharField(max_length=32)
    perm_group = models.ForeignKey('PermGroup', blank=True, on_delete=models.CASCADE)
    pid = models.ForeignKey('Permission', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Permission'

class PermGroup(models.Model):
    name = models.CharField(max_length=32, unique=True)
    menu = models.ForeignKey('Menu', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'PermGroup'

class Menu(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Menu'
