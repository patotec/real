from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid
from index.models import Property


class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50,default='0')
    accountbalance = models.CharField(max_length=50,default='5')
    image = models.ImageField(default='pro_ny6h2o.png',blank=True)
    is_email_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Request(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    property = models.ForeignKey(Property,on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.email

class Pay_method(models.Model):
    name = models.CharField(max_length=50,default='0')
    wallet = models.CharField(max_length=500,default='0')
    image = models.FileField()
    visible = models.BooleanField(default=True)
    slug = models.SlugField(blank=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Pay_method, self).save(*args, **kwargs)

class Payment(models.Model):
    user = models.CharField(max_length=50,default='0')
    name = models.CharField(max_length=50,default='0')
    price = models.CharField(max_length=50,default='0')
    wallet = models.CharField(max_length=500,default='0')
    image = models.FileField()
    approve = models.BooleanField(default=False)
    def __str__(self):
        return self.name



class ChangePasswordCode(models.Model):
	user_email = models.EmailField(max_length=50)
	user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class ChangePassword(models.Model):
	new_password = models.CharField(max_length=50, blank = False, null = False)
	confirm_new_password = models.CharField(max_length=50, blank = False, null = False)