from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from django.http import JsonResponse

from ..models import User

from Account.utils import generate_access_token, generate_refresh_token


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try :
            data = JSONParser().parse(request)
        except : 
            return JsonResponse({
                "message" : "Json 문법오류",
                "info" : f"{data}"
            }, status=400)

        username = data['user_id']
        password = data['password']
        try :
            loginUser = User.objects.get(username=username, password=password)
        except :
            return JsonResponse({
                "code" : "00101",
                "message" : "해당하는 사용자 아이디 또는 비밀번호가 존재하지 않습니다. ",
                "status" : 404
            }, status=404)
        
        access_token = generate_access_token(loginUser)
        refresh_token = generate_refresh_token(loginUser)

        tokens = dict(
            user_id=username,
            name=loginUser.name,
            access_token=access_token,
            refresh_token=refresh_token
        )
        res = dict(
            code="10101",
            message="로그인이 완료되었습니다.",
            status=200,
            info = tokens
        )
        return JsonResponse(
            res, safe=False,status=200
        )

    else :
        message = "You must send 'POST' request"
        res = dict(
            code="00105",
            message=message,
            status=400
        )
        return JsonResponse(
            res, safe=False, status=400
        )
