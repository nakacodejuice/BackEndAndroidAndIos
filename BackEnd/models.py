from django.db import models

# Create your models here.
class session(models.Model):
    access_token = models.CharField(max_length=36, primary_key=True)
    token_type = models.CharField(max_length=100,default='bearer')
    expires_in = models.IntegerField(default=3600)
    datetimecreate = models.DateTimeField('date created', auto_now_add=True)
    uiduser = models.CharField(max_length=36, primary_key=True)
    def __str__(self):
        return self.uiduser+'/'+str(self.datetimecreate)

    class Meta:
        ordering = ["-datetimecreate"]

class MobileUsers(models.Model):
    login = models.CharField(max_length=36,primary_key=True)
    status = models.CharField(max_length=15)
    password = models.CharField(max_length=36)
    uiduser = models.CharField(max_length=36, primary_key=True)
    datetimecreate = models.DateTimeField('date created', auto_now_add=True)
    def __str__(self):
        return self.login+'-'+str(self.uiduser)

class GasUsers(models.Model):
    account = models.CharField(max_length=10,primary_key=True)
    uiduser = models.CharField(max_length=36)
    def __str__(self):
        return self.account+'/'+str(self.uiduser)