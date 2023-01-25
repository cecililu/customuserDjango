from datetime import timezone
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.itercompat import is_iterable
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    # def with_perm(
    #     self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    # ):
    #     if backend is None:
    #         backends = auth._get_backends(return_tuples=True)
    #         if len(backends) == 1:
    #             backend, _ = backends[0]
    #         else:
    #             raise ValueError(
    #                 "You have multiple authentication backends configured and "
    #                 "therefore must provide the `backend` argument."
    #             )
    #     elif not isinstance(backend, str):
    #         raise TypeError(
    #             "backend must be a dotted import path string (got %r)." % backend
    #         )
    #     else:
    #         backend = auth.load_backend(backend)
    #     if hasattr(backend, "with_perm"):
    #         return backend.with_perm(
    #             perm,
    #             is_active=is_active,
    #             include_superusers=include_superusers,
    #             obj=obj,
    #         )
    #     return self.none()






class ClusterType(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Municipality(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
         
class Ward(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    municipality=models.ForeignKey(Municipality,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.name

class TestDisasterModel(models.Model):
    name= name = models.CharField(max_length=255)
    municipality=models.ForeignKey(Municipality,on_delete=models.CASCADE,null=True,blank=True)
    ward=models.ForeignKey(Ward,on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.name
 
class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),

        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    
    name = models.CharField(_("name"), max_length=150, blank=True)
    # last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_CDO = models.BooleanField(default=False)
    is_Municipality = models.BooleanField(default=False)
    is_Ward = models.BooleanField(default=False)
    is_cluster = models.BooleanField(default=False)
    cluster_type = models.ForeignKey(ClusterType, on_delete=models.CASCADE, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, null=True, blank=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, blank=True)
    
    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    
    def __str__(self):
        return self.username
    
# activity log and signal
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestDisasterModel

class ActivityLog(models.Model):
    action_name = models.CharField(max_length=255)
    deployed_inventory = models.IntegerField()
    time_of_action = models.DateTimeField(auto_now_add=True)
    disaster = models.ForeignKey(TestDisasterModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.action_name

@receiver(post_save, sender=TestDisasterModel)
def create_activity_log(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            action_name='disasterstart', 
            deployed_inventory=0, 
            time_of_action=timezone.now(), 
            disaster=instance
        )
