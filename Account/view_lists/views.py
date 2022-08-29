from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie 
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

from Account.models import User, Verification
from Account.serializer import CreateUser, EditUser, ReadUser, CreateVerification

from django.core.mail import send_mail
from django.conf import settings
from random import randint

# Create your views here.


@csrf_exempt
def signUp(request):
    data = JSONParser().parse(request)

    if request.method == 'POST':
        try :
            User.objects.get(username=data['user_id'])
            return JsonResponse({
                "code" : "00201",
                "message" : "해당 아이디는 중복됩니다.",
                "status" : 405
            }, status=400)
        except :
            pass

        try :
            User.objects.get(email=data['email'])
            return JsonResponse({
            	"code" : "00203",
	            "message" : "메일인증을 실패하였습니다.",
	            "status" : 400
            }, status=400)
        except :
            pass

        try :
            User.objects.get(
                grade_number    = data['grade_number'],
                class_number    = data['class_number'],
                student_number  = data['student_number']
            )
            return JsonResponse({
            	"code" : "00202",
	            "message" : "해당 학생 또는 학생번호를 이용하는 사용자가 이미 존재합니다.",
	            "status" : 405
            }, status=400)
        except :
            pass

        serializer = CreateUser(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "code" : "10201",
	            "message" : "회원가입이 완료 되었습니다.",
                "status" : 201,
                "info" : serializer.data
            }, safe=False, status=201)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
@csrf_exempt
def user_setting(request, username):
    try:
        getUser = User.objects.get(username=username)
    except :
        return JsonResponse({
        "code" : "00702",
        "message" : f"{username}라는 유저는 존재하지않습니다.",
        "status": 404 
    }, status=404)
        
    if request.method == 'GET':
        serializer = ReadUser(getUser)
        return JsonResponse({	
            "code" : "10701",
	        "message" : "회원정보를 불러왔습니다.",
	        "status" : 200,
            "info" : serializer.data
        }, safe=False, status=200)
    
    if request.method == 'PUT':
        data = JSONParser().parse(request)

        try :
            User.objects.get(email=data['email'])
            return JsonResponse({
            	"code" : "00704",
	            "message" : "메일을 이용중인 사용자가 이미 존재합니다.",
	            "status": 400
            }, status=400)
        except :
            pass

        try :
            User.objects.get(
                grade_number    = data['grade_number'],
                class_number    = data['class_number'],
                student_number  = data['student_number']
            )
            return JsonResponse({
                "code" : "00705",
                "message" : "해당 학생 또는 학생번호를 이용하는 사용자가 이미 존재합니다.",
                "status" : 405
            }, status=405)
        except :
            pass
        
        serializer = EditUser(getUser, data=data)

        if serializer.is_valid():
            serializer.save()
        return JsonResponse({
            "code" : "10702",
	        "message" : "회원정보가 바뀌었습니다.",
	        "status" : 201,
            "info" : serializer.data
        }, safe=False, status=201)
    
    if request.method == 'DELETE':
        data = JSONParser().parse(request)

        if getUser.password == data['password']:
            getUser.delete()
            return JsonResponse({
                "code" : "10703",
	            "message" : "회원 탈퇴가 정상적으로 완료되었습니다.",
	            "status" : 205
            }, status=205)
        else :
            return JsonResponse({
                "code" : "00703",
	            "message" : "비밀번호가 일치 하지 않습니다.",
	            "status": 400
            }, status=400)

    return JsonResponse({
        "message" : "You must send ['GET', 'POST', 'DELETE'] request"
    }, safe=False, status=400)


@csrf_exempt
def change_pw_verification(request, username):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        new_pw = data['new_pw']
        pw_check = data['pw_check']

        try :
            getUser = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                "code" : "00403",
                "message" : f"{username}라는 유저는 존재하지않습니다.",
                "status" : 404,
            }, status=404)

        if getUser.is_able_to_change() == False:
            return JsonResponse({
                "code" : "00404",
                "message" : "이메일 인증을 다시 시도하여 주십시요.",
                "status": 400
            }, status=400)

        if new_pw == pw_check:
            getUser.change_password(new_pw=new_pw, pw_check=pw_check)
            getUser.done_pw_access()
            return JsonResponse({
                "code" : "10401",
                "message" : "비밀번호 변경이 완료 되었습니다.",
                "status" : 201
            }, status=201)
        else :
            return JsonResponse({
                "code" : "00402",
                "message" : "비밀번호가 확인번호와 같지 않습니다.",
                "status" : "400"
            }, status=400)

    return JsonResponse({
        "message" : "You must send ['POST'] request"
    }, safe=False, status=400)


@csrf_exempt
def change(request, username):
    if request.method == 'POST':

        data = JSONParser().parse(request)

        password    = data['password']
        new_pw      = data['new_pw']
        pw_check    = data['new_pw']

        try :
            user = User.objects.get(username=username, password=password)
        except :
            return JsonResponse({
                "code" : "00403",
            	"message" : "일치하는 유저기 존재하지 않습니다.",
                "status": 404
            }, status=400)

        if (password == new_pw) :
            return JsonResponse({
                "code" : "00402",
                "message" : "기존의 비밀번호와 다른 비밀번호를 입력해 주십시오.",
                "status" : "400"
            },status=400)

        if user.change_password(new_pw=new_pw, pw_check=pw_check) == True :
            return JsonResponse({
                "code" : 10401,
                "message" : "비밀번호 변경이 완료 되었습니다.",
                "status" : 201,
            }, status=201)

    return JsonResponse({
        "message" : "You must send ['POST'] request"
    }, safe=False, status=400)

