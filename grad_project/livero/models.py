from importlib.resources import *

from django.db import models

from django.contrib.auth.models import AbstractUser


class TimestampedModel(models.Model):
    """
    Abstract model to contain information about creation/update time.

    :created_at: date and time of record creation.
    :updated_at: date and time of any update happends for the record.
    """

    created_at = models.DateTimeField(verbose_name="وقت الانشاء", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Update Date/Time", auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


class Users(AbstractUser):
    username = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        unique=True,
    )
    email = models.EmailField(
        max_length=125,
        unique=True,
        error_messages={
            "unique": ("A user with that email already exists."),
        },
    )
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    age = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    # android_token = models.CharField(max_length=256, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "mobile"]

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.email


class Symptoms(TimestampedModel):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class ChronicDiseases(TimestampedModel):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Medicine(TimestampedModel):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Tests(TimestampedModel):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Doctors(TimestampedModel):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    specification = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class SymptomsTests(TimestampedModel):
    symptoms = models.ForeignKey(Symptoms, on_delete=models.CASCADE)
    tests = models.ForeignKey(Tests, on_delete=models.CASCADE)

    def __str__(self):
        return self.symptoms.name + ' ' + self.tests.name


class UserStatus(TimestampedModel):
    min = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, blank=True, null=True)
    max = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, blank=True, null=True)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status


class MedicineAllergy(TimestampedModel):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Readings(TimestampedModel):
    blood_types = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B_"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]
    users = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
    blood = models.CharField(max_length=255, null=True, blank=True, choices=blood_types)
    urine = models.DecimalField(max_digits=90, decimal_places=2, default=0.0, null=True, blank=True)
    kidney = models.DecimalField(max_digits=120, decimal_places=2, default=0.0, null=True, blank=True)
    symptoms = models.ManyToManyField(Symptoms, blank=True, related_name="reading_sym")
    chironic_dieases = models.ManyToManyField(ChronicDiseases, null=True, related_name="reading_chi")
    medicine_allergy = models.BooleanField(default=False)
    user_status = models.ForeignKey(UserStatus, on_delete=models.CASCADE, blank=True, null=True)
    fbi_result = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    def __str__(self):
        return str(self.fbi_result)


class Hospitals(TimestampedModel):
    name = models.CharField(max_length=255)
    phone = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="image", blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Laps(TimestampedModel):
    name = models.CharField(max_length=255)
    phone = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="image", blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
