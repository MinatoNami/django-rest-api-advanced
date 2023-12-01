"""
Database models
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


def recipe_image_file_path(instance, filename):
    """
    Generate file path for new recipe image
    """
    # get the extension of the file
    ext = os.path.splitext(filename)[1]
    # create the filename
    filename = f'{uuid.uuid4()}{ext}'

    # return the path
    return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user profile"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)  # encrypts the password
        # standard procedure for saving objects in django
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True  # is_superuser is created by PermissionsMixin
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # this is required for django to work with our custom user model
    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        # this is the user model that is active in the project
        settings.AUTH_USER_MODEL,
        # if the user is deleted, delete the recipe
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)  # optional field
    # this is a string because the Tag model is defined below
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        # this is the user model that is active in the project
        settings.AUTH_USER_MODEL,
        # if the user is deleted, delete the recipe
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        # this is the user model that is active in the project
        settings.AUTH_USER_MODEL,
        # if the user is deleted, delete the recipe
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
