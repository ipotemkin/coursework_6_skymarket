from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models

from skymarket.settings import UserRoles
from users.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):

    ROLES = [(UserRoles.USER, "Пользователь"), (UserRoles.ADMIN, "Администратор")]

    email = models.EmailField(unique=True, verbose_name="Email address")
    first_name = models.CharField(max_length=64, verbose_name="Имя")
    last_name = models.CharField(max_length=64, verbose_name="Фамилия")
    phone = models.CharField(max_length=128, verbose_name="Телефон для связи")
    role = models.CharField(max_length=5, choices=ROLES, default=UserRoles.USER, verbose_name="Роль")

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    # также для работы модели пользователя должен быть переопределен
    # менеджер объектов
    objects = UserManager()

    # эта константа определяет поле для логина пользователя
    USERNAME_FIELD = 'email'

    # эта константа содержит список с полями,
    # которые необходимо заполнить при создании пользователя
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']  #, "role"]

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER
