from datetime import date, datetime

# Create your views here.

import json
from .models import Meal, MealList
from django.views import View

from django.http import JsonResponse

import requests

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .serializer import ReadBreakfast, ReadDinner, ReadLunch, ReadMealList, MakeMealList

@method_decorator(csrf_exempt, name='dispatch')
class MealListView(View):
    def post(self, request):
        MealList.objects.all().delete()
        Meal.objects.all().delete()

        api_url = 'https://open.neis.go.kr/hub'
        app_url = 'mealServiceDietInfo'
        OFCDC = 'R10' #시도 교육청 코드
        SCHUL = '8750205' #표준학교코드
        key = '4f5ebbeb3aaf43409dd048e871679003'
        START = ''
        now_month = f'{datetime.utcnow()}'.replace('-', '')[0:6]
        
        req = requests.get(
            f'{api_url}/{app_url}?Type=json&ATPT_OFCDC_SC_CODE={OFCDC}&SD_SCHUL_CODE={SCHUL}&KEY={key}&MLSV_YMD={now_month}'
        ).json()

        # serializer = ReadMealList(MealList.objects.all(), many=True)


        for item in req['mealServiceDietInfo'][1]['row']:

            year = int(item['MLSV_FROM_YMD'][0:4])
            month = int(item['MLSV_FROM_YMD'][4:6])
            day = int(item['MLSV_FROM_YMD'][6:8])

            time = date(year,month,day)
            mealcode = int(item['MMEAL_SC_CODE'])

            try :
                meal_list = MealList.objects.get(date=time)
            except MealList.DoesNotExist:
                meal_list = MealList.objects.create(date=time)
            
            meal = Meal.objects.create(menu=item['DDISH_NM'])
            meal_list.update_meal(number= mealcode,data=meal)

            serializer = ReadMealList(MealList.objects.all(), many=True)
        return JsonResponse({
            "code" : 10802,
            "message" : "이번달 전채 급식 메뉴를 성공적으로 불러 왔습니다.",
            "status" : 200,
            "search list": serializer.data 
        })
        

    def get(self, request):
        serializer = ReadMealList(MealList.objects.all(), many=True)
        return JsonResponse({'search list' : serializer.data }, status=200)



class getmeal(View):
    def get(self, request) :
        try : timecode = f"{request.GET['timecode']}"
        except : timecode = None
        try : mealcode = int(request.GET['mealcode'])
        except : mealcode = None

        if timecode is not None :
            if len(timecode) != 6 and len(timecode) != 8:
                return JsonResponse({
                    "code" : "00801",
                    "message" : "시간코드의 형식이 올바르지 않습니다.",
                    "status" : 400,
                    "info" : {
                        "rules" : "연,달,월 8짜리 또는 연,달의 6자리를 입력해 주십시오."
                    }
                }, status=400)
            year = int(timecode[0:4])
            month = int(timecode[4:6])

            if len(timecode) == 6:
                query_set = MealList.objects.filter(date__year=year, date__month=month)
            elif len(timecode) == 8:
                day = int(timecode[6:8])
                query_set = MealList.objects.filter(date=date(year,month,day))
        else :
            query_set = MealList.objects.all()

        if mealcode == 1:
            serializer = ReadBreakfast(query_set, many=True)
        elif mealcode == 2:
            serializer = ReadLunch(query_set, many=True)
        elif mealcode == 3:
            serializer = ReadDinner(query_set, many=True)
        else :
            serializer = ReadMealList(query_set, many=True)
        
        return JsonResponse({
            "code" : "10801",
            "message" : "급식 메뉴를 성공적으로 불러 왔습니다.",
            "status" : 200,
            "info" : serializer.data
        }, safe=False, status=200)
    