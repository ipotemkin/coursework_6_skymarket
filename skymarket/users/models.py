from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from users.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class UserRoles:
    # TODO закончите enum-класс для пользователя
    pass


class User(AbstractBaseUser):
    # TODO переопределение пользователя.
    # TODO подробности также можно поискать в рекоммендациях к проекту

    USER = "user"
    ADMIN = "admin"

    ROLES = [(USER, "Пользователь"), (ADMIN, "Администратор")]

    email = models.EmailField(
        null=True,
        blank=True,
        unique=True,
        verbose_name="Email"
    )
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    role = models.CharField(max_length=5, choices=ROLES, default=USER, verbose_name="Роль")

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
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_user(self):
        return self.role == User.USER
