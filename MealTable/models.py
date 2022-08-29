
from django.db import models

# Create your models here.

class Meal(models.Model):
    menu = models.TextField(blank=True)

    def __str__(self):
        return self.menu


class MealList(models.Model):
    date = models.DateField(blank=True)

    breakfast = models.ForeignKey(
        Meal, 
        blank=True, 
        null=True,
        on_delete=models.CASCADE,
        related_name="breakfast_id",
    )
    lunch = models.ForeignKey(
        Meal,
        null=True,
        blank=True, 
        on_delete=models.CASCADE,
        related_name="lunch"
    )
    dinner = models.ForeignKey(
        Meal, 
        null=True,
        blank=True, 
        on_delete=models.CASCADE,
        related_name="dinner"
    )

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'meal_lists'

    def update_meal(self, data, number):
        if number == 1:
            self.breakfast = data
        if number == 2:
            self.lunch = data
        if number == 3:
            self.dinner = data
        self.save()
        return self

