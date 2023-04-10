from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
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

# NOTE8 : The recipe app
# Create the model
# register in admin
# create the serializer and viewset and include the router config in urls.py and then add the url to the main urls.py


class Recipe(models.Model):
    """Recipe object"""
    # We are creating a relation between recipe model and user model
    # on delete , if user deletes the profile , then all recipes will be deleted
    #
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=255)
    # in some database TextField have bad performance
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    # add this after creating the tag field
    # Many different recipes can have many different tags
    # tags here is a related field and expected to be passed in sepaerately
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

# NOTE11: Creating the tag
# add the tag feature to the recipe model
# register in admin
# add the serializer in recipe (check there)


class Tag(models.Model):
    """tag for filtering recipes"""
    name = models.CharField(max_length=225)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
