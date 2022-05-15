from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, null=True, unique=True)
    address = models.ForeignKey(
        "address.Address", on_delete=models.CASCADE, related_name="address", null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
