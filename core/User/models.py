import hashids
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from core.Joke.models import Joke, JokeSeen
from .tasks import send_activation_link_to_email
from .utils import RegistrationCodeHandler


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    REGISTRATION_CODE_EXPIRE_TIME_SECONDS = 60 * 60 * 24 # 1 day

    username = models.CharField(max_length=255, unique=True, db_index=True, null=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True, null=True)

    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.label

    @property
    def tg_nickname(self):
        return f'@{self.username}'

    @property
    def label(self):
        return self.email or self.id

    def archive(self):
        self.is_active = False
        self.save()

    def restore(self):
        self.is_active = True
        self.save()

    def hashid(self):
        return hashids.Hashids(settings.HASHID_SECRET, min_length=settings.HASHID_LENGTH)

    def send_activation_mail(self, request=None):
        handler = RegistrationCodeHandler(self, request=request)
        link = handler.generate_activation_link()
        print(link)
        send_activation_link_to_email.apply_async(kwargs={'user': self, 'link': link})
        return True
