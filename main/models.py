from __future__ import unicode_literals
from datetime import date
from django.db import models

# Create your models here.

class Master(models.Model):
	
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=250)
	address = models.TextField()
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	zipcode = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	coins = models.CharField(max_length=50)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.firstname

	def __unicode__(self):
		return self.firstname

	class Meta:
		ordering = ["-timestamp"]


