from .Address import AddressModel
from .BaseModel import BaseModel
from .Audits import AuditModel
from djongo import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from rest_framework_simplejwt.tokens import RefreshToken

from ..JWTConfig.CustiomJwt import CustomRefreshToken

@deconstructible
class UseremailValidator(validators.EmailValidator):
    message = _(
        'Enter a valid email. This value may contain only letters, '
        'numbers, and @/. characters.'
    )
    flags = 0

class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email) 
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

AUTH_PROVIDERS = { 'google': 'google', 'email': 'email'}

class Users(BaseModel,AbstractUser):

    _id = models.ObjectIdField()
 
    username_validator = UnicodeUsernameValidator()
    email_validator = UseremailValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'),
        max_length=250,
        unique=True,
        help_text=_('Required. 250 characters or fewer. Letters, digits and /_ only.'),
        validators=[email_validator],
        error_messages={
            'unique': _("A user with that email already exists."),
        },
        blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    auth_providers = models.CharField(max_length=255,blank=False,null = False,default=AUTH_PROVIDERS.get('email'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    groups = None
    user_permissions = None
    
    address = models.ArrayField(model_container=AddressModel)
    audits_data = models.EmbeddedField(model_container=AuditModel)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    
    def __str__(self):
        return self.email

    def get_id(self):
        return self._id

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    def tokens(self):
        refresh = CustomRefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    class Meta:
        abstract = False
        db_table = "Authors"




# User--> AbstractUser ---> (AbstractBaseUser, PermissionsMixin)