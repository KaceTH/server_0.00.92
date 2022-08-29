from .models import Meal, MealList
from rest_framework.serializers import ModelSerializer

class MealSerializer(ModelSerializer):
    class Meta:
        model = Meal
        fields = [
            'menu'
        ]


class ReadBreakfast(ModelSerializer):
    breakfast = MealSerializer(read_only=True)
    
    class Meta:
        model = MealList
        fields = [
            'date',
            'breakfast'
        ]


class ReadLunch(ModelSerializer):
    lunch = MealSerializer(read_only=True)
    
    class Meta:
        model = MealList
        fields = [
            'date',
            'lunch'
        ]
         

class ReadDinner(ModelSerializer):
    dinner = MealSerializer(read_only=True)
    
    class Meta:
        model = MealList
        fields = [
            'date',
            'dinner'
        ]
         

class ReadMealList(ModelSerializer):
    breakfast = MealSerializer(read_only=True)
    lunch = MealSerializer(read_only=True)
    dinner = MealSerializer(read_only=True)

    class Meta:

        model = MealList
        fields = [
            'date',
            'breakfast',
            'lunch',
            'dinner'
        ]

        
class MakeMealList(ModelSerializer):
    class Meta:
        breakfast = MealSerializer()
        model = MealList
        fields = [
            'breakfast',
            'lunch',
            'date',
        ]
