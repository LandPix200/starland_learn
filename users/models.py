from django.db import models

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, name, email,  phone_number, county, city, password=None, **extra_fields):
        if not email:
            raise ValueError(
                "L'adresse e-mail est obligatoire pour créer un utilisateur")

        email = self.normalize_email(email)
        user = self.model(
            email=email, name=name, phone_number=phone_number, county=county, city=city,
            **extra_fields
        )
        user.set_password(password)

        user.save(using=self._db)
        return user


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
