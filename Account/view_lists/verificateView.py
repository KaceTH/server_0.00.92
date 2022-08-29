from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from django.http import JsonResponse

from Account.models import User, Verification

from random import randint

@csrf_exempt
def email_verification(request, username):
    try:
        getUser = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({
	        "code" : "00302",
	        "message" : f"{username} 라는 유저는 존재하지않습니다.",
	        "status": 404 
        }, status=404)

    if request.method == 'GET':
        try:
            usage = request.GET['usage']
        except:
            usage = 1
        
        if getUser.is_verificated == True and usage == 1 :
            return JsonResponse({
                "code" : "00303",
                "message" : "메일 인증을 이미 완료하였습니다",
                "status": 403 
            }, status=403)
        
        
        code = randint(123456,999999)

        try :
            getVerific = Verification.objects.get(author=getUser)
            getVerific.delete()
        except Verification.DoesNotExist:
            pass

        verification = Verification.objects.create(
            author=getUser,
            code=code,
            usage=usage
        )
        verification.send_verification()
        verification.set_end_date()

        info = dict(user_id=username, email=getUser.email)

        return JsonResponse({
            "code" : "10301",
            "message" : "메일인증코드를 전송하였습니다.",
            "status" : 200,
            "info" : info
        }, status=200)

    if request.method == 'POST':
        data = JSONParser().parse(request)

        code = data['code']
        try: usage = data['usage'] 
        except: usage = 1

        try :
            getVerific = Verification.objects.get(author=getUser, usage=usage)
        except Verification.DoesNotExist:
            return JsonResponse({
                "code" : "00304",
                "message" : "메일 인증이 존재하지 않습니다.",
                "status": 404
            }, status=404)

        

        if getVerific.is_end_date():
            return JsonResponse({
                "code" : "00305",
                "message" : "기간이 만료되었습니다.",
                "status": 400
            }, status=400)

        if code == getVerific.code :
            getVerific.delete()

            if usage == 1:
                getUser.is_verificated = True
                getUser.save()
            elif usage == 2:
                getUser.pw_access_due = datetime.utcnow()
                getUser.save()

            return JsonResponse({
                "code" : "10302",
                "message" : "메일인증을 완료하였습니다.",
                "status" : 200,
            }, status=200)
        return JsonResponse({
            "code" : "00306",
            "message" : "코드가 일치하지 않습니다.",
            "status": 400
        }, status=400)
