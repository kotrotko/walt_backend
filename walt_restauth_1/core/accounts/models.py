from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def _create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.

        Note:
            This method is independent for internal use and should not be called directly.
            Use 'create_user' or 'create_superuser' instead.
        """
        if not email:
            raise ValueError('Email is Required.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        user = self._create_user(email, password, **extra_fields)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.

        Returns:
            User: The created superuser instance.

        Note:
            This method calls '_create_user' internally to create the superuser.
            It sets the appropriate flags for a superuser and performs necessary checks.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    ROLES = (
        ('employer', 'Employer'),
        ('jobseeker', 'Jobseeker'),
    )
    roles = models.CharField(max_length=20, choices=ROLES, default='jobseeker')
    email = models.EmailField(max_length=30, verbose_name='Email', blank=False, null=True, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['roles']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        app_label = 'accounts'

    def __str__(self):
        return f'{self.email}'


# source: https://www.webforefront.com/django/customauthbackend.html
class EmailBackend(object):
    '''Authentication backend that allows users to authenticate using their email address.

    This backend is used to authenticate users by their email address instead of the traditional username.
    It checks if the provided email exists in the database and verifies the password for authentication.

    Usage:
        In Django settings.py file, the 'AUTHENTICATION_BACKENDS' is:
        AUTHENTICATION_BACKENDS = [
            'path.to.EmailBackend',
            ...
        ]

    Note:
        This backend assumes the existence of a custom user model where email is used as the unique identifier.
        '''
    def authenticate(self, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
