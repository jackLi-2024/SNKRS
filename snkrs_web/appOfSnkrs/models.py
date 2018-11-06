from django.db import models

# Create your models here.

# t_account表：
class Account(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, null=False, unique=True)
    password = models.CharField(max_length=64, null=False)

    def __str__(self):
        return "<Account Object: {}>".format(self.phone)
