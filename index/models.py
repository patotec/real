from email.mime import image
from django.db import models
from django.utils.text import slugify

class Contact(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField()
	subject = models.CharField(max_length=2000)
	message = models.TextField()

	def __str__ (self):
		return self.name

class Team(models.Model):
	name = models.CharField(max_length=200)
	image = models.FileField()

	def __str__ (self):
		return self.name

class Review(models.Model):
	name = models.CharField(max_length=200)
	image = models.ImageField()
	body = models.TextField()

	def __str__ (self):
		return self.name



class Place(models.Model):
	name = models.CharField(max_length=200)
	image = models.ImageField()

	def __str__ (self):
		return self.name



class Property(models.Model):
	CATEGORY_CHOICES = (
    ('Rent', 'Rent'),
    ('Sale', 'Sell')
   
)
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	price = models.IntegerField()
	bedrooms = models.IntegerField()
	bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
	garage = models.IntegerField(default=0)
	sqft = models.IntegerField()
	latitude = models.CharField(max_length=200,default='40.765710')
	longitude = models.CharField(max_length=200,default='-73.976150')
	image = models.ImageField()
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=10 ,null=True)
	photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
	photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
	photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
	photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
	photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
	slug = models.SlugField(blank=True)
	created = models.DateTimeField(auto_now_add=True)


	def __str__ (self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Property, self).save(*args, **kwargs)
# Create your models here.
