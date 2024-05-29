import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from django.db import models

# Create your models here.


class CustomUserManager(BaseUserManager):

    def create_user(
        self, email, password=None, name=None, company=None, **extra_fields
    ):
        if not email:
            raise ValueError("Email must be set!")
        if not password:
            raise ValueError("Passowrd must be set!")
        if not name:
            raise ValueError("Name must be set!")
        if not company:
            raise ValueError("Company must be set!")

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, company=company, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email=None, password=None, name=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email!")
        if not password:
            raise ValueError("User must have a password!")
        if not name:
            raise ValueError("Name must be set!")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        user = self.create_user(email, password, name, **extra_fields)
        user.is_superuser = True
        user.save()

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True)
    company = models.CharField(max_length=255, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "company"]

    objects = CustomUserManager()

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    email = models.EmailField(max_length=100, blank=False)
    subject = models.CharField(max_length=255, blank=False)
    message = models.TextField(blank=False)

    def __str__(self):
        return self.message
