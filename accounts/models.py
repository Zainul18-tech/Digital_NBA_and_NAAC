from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        FACULTY = "FACULTY", "Faculty"
        HOD = "HOD", "Head of Department"
        NBA_COORDINATOR = "NBA_COORDINATOR", "NBA Coordinator"
        NAAC_COORDINATOR = "NAAC_COORDINATOR", "NAAC Coordinator"
        REVIEWER = "REVIEWER", "Reviewer"

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.FACULTY
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    department = models.ForeignKey(
    'core.Department',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='users'
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"