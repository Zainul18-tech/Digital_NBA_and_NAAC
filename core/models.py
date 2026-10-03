from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="departments"
    )

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Program(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="programs"
    )

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)

    duration_years = models.PositiveIntegerField(default=4)
    sanctioned_intake = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class AcademicYear(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True
    )

    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()

    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.name