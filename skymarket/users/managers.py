from django.contrib.auth.models import (
    BaseUserManager
)


# TODO здесь должен быть менеджер для модели Юзера.
# TODO Поищите эту информацию в рекомендациях к проекту
# from users.models import User
from skymarket.settings import UserRoles


class UserManager(BaseUserManager):
    """
    функция создания пользователя — в нее мы передаем обязательные поля
    """

    def _create_base_user(self, email, first_name, last_name, phone, password=None, role=UserRoles.USER):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, first_name, last_name, phone, password=None):
        return self._create_base_user(email, first_name, last_name, phone, password, role=UserRoles.USER)

    def create_superuser(self, email, first_name, last_name, phone, password=None):
        """
        функция для создания суперпользователя — с ее помощью мы создаем админинстратора
        это можно сделать с помощью команды createsuperuser
        """

        return self._create_base_user(email, first_name, last_name, phone, password, role=UserRoles.ADMIN)
