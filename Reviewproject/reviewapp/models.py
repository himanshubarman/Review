from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
# Create your models here.



class AccountManager(BaseUserManager):
	def create_user(self, email ,password, **extra_fields):
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must enter password")
		user = self.model(
			email = self.normalize_email(email),
			**extra_fields
			)
		user.set_password(password)
		user.is_active = True
		user.save(using=self._db)
		return user
	
	def create_staffuser(self, email, password):
		user = self.create_user(email,password=password)
		user.is_staff = True
		user.is_active = True
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email = self.normalize_email(email),
			password=password,
			username=username
			)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.is_active = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
	SEMESTER_CHOICES = ( 
	("1", "Student"), 
	("2", "Tutor"),
	("3", "Admin"),)
	
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = models.EmailField(max_length=30, unique=True)
	date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last_login', auto_now_add=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	
	objects = AccountManager()
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username"]
	def __str__(self):
		return self.email
	
	def has_perm(self, perm, obj=None):
		return self.is_admin
	
	def has_module_perms(self, app_label):
		return True
	
	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')
	
	def set_username_as_email(self):
		username = self.email
		return username

	def get_full_name(self):
		full_name = "{0}".format(self.first_name)
		return full_name.strip()
	
	def get_short_name(self):
		return self.first_name

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	"""Create a Token instance for any User instance created."""
	if created:
		Token.objects.get_or_create(user=instance)


class Product(models.Model):
	name = models.CharField(max_length=255, null=False, blank=False)
	price= models.DecimalField(max_digits=10, decimal_places=2,default=0)
	image = models.ImageField(upload_to ='uploads/')
	description = models.CharField(max_length=255, null=True, blank=True)


class Review(models.Model):
	RATING_CHOICES = ( 
	("0", "None"),
	("1", "Very Poor"), 
	("2", "Bad"),
	("3", "Average"),
	("4", "Good"),
	("5", "Excellent"),)
	product_item = models.ForeignKey(Product, models.CASCADE, related_name='product')
	sender = models.ForeignKey(User, models.CASCADE, related_name='reviewsender')
	comment = models.CharField(max_length=255)
	rating = models.CharField(max_length = 20, choices = RATING_CHOICES, default = '0')
	timestamp = models.DateTimeField(default=timezone.now)
	calculated_review = models.BooleanField(default=False)

class ActivityLog(models.Model):
	product_item = models.ForeignKey(Product, models.CASCADE, related_name='activity_product')
	user = models.ForeignKey(User, models.CASCADE, related_name='user_activity')
	event = models.CharField(max_length=255, default="review added")
	date = models.DateTimeField(auto_now_add=True)

class RatingEvaluationString(models.Model):
	product_item = models.ForeignKey(Product, models.CASCADE, related_name='activity_product_string')
	string_review = models.CharField(max_length=255)
	fromat_string_review = models.CharField(max_length=255)
	event = models.CharField(max_length=255, default="review string added")
	date = models.DateTimeField(auto_now_add=True)


