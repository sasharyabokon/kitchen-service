from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Ingredient(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class DishType(models.Model):
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class Dish(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="dishes")
    ingredients = models.ManyToManyField(Ingredient, related_name="dishes", blank=True)

    class Meta:
            ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class Cook(AbstractUser):
    years_of_experience = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("username",)

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})
