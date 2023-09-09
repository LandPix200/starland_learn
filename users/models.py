from django.db import models


from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name="Adresse e-mail")
    is_teacher = models.BooleanField(
        default=False, verbose_name="Est enseignant")
    is_student = models.BooleanField(
        default=False, verbose_name="Est étudiant")
    last_name = models.CharField(max_length=255, verbose_name="Nom de famille")
    phone_number = models.CharField(
        max_length=20, verbose_name="Numéro de téléphone")
    country = models.CharField(max_length=255, verbose_name="Pays")
    city = models.CharField(max_length=255, verbose_name="Ville")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Teacher(User):
    is_teacher = True

    class Meta:
        proxy = True


class Student(User):
    is_student = True

    class Meta:
        proxy = True
