from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None

    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=10)
    dob = models.DateField(null=True, blank=True)

    profile_pic = models.ImageField(null=True, blank=True)

    street = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=128, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def address(self):
        addr =  f"{self.street},\n{self.city}, {self.state},\n{self.country}, {self.pincode}"
        if 'None' in addr:
            return addr.replace('None,', '').replace('\n', '')
        return addr
