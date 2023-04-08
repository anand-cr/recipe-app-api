from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.


# NOTE: STEPS TO CREATE A CUSTOM USER
# make sure core is added to  insatlled apps
# 1. set up the user model
# 2. set the user manger
# 3. assign the user manager to the user
# 4. add the user to the settings.py : AUTH_USER_MODEL = 'core.User'
# 5 Migrate
# NOTE: when migrating if raise InconsistentMigrationHistory(because we already migrated the default user model and we overrode it)
# https://stackoverflow.com/a/48476148/11880076


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create save and return a new user"""
        if not email:
            raise ValueError("Users must have an email address")
        # extrafield is useful when we have extra fields
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # takes in the provided passsword and encrypts it
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """create and returm superuser"""

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
# overriding the default User
# abstractBaseUser : functionality of authentican sysytem ,permissionsmixin : functionality of permisssions and  has fields


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    # determins who can enter the admin
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # determine the field we use for authentication
