from unicodedata import category
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.views import View
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from Account.models import User

from Posting.models import Post
from .serlializer import EditPost, MakePost, ReadPost

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class PostListView(View):
    def get(self, request) :
        try : 
            page = int(request.GET['page'])
            start = 10 * (page - 1)
            end = 10 * (page)
        except : 
            start = 0
            end = 10

        posts = Post.objects.all().order_by('-id')[start : end]

        serializer = ReadPost(posts, many=True)
        return JsonResponse({
            "code" : "11001",
	        "message" : "게시판 목록을 불러 왔습니다.",
	        "status" : 200,
            "info" : serializer.data
        }, status=200)

    def post(self, request) :
        try: 
            data = JSONParser().parse(request)
            username = data['user_id']
            title = data['title']
            content = data['content']
            category = int(data['category'])

        except : return JsonResponse({
            "code" : "01110",
            "message" : "유저가 존재하지 않습니다.",
            "status" : 400	
        })

        try : user = User.objects.get(username=username)
        except : return JsonResponse({
            "code" : "01102",
            "message" : "유저가 존재하지 않습니다.",
            "status" : 404
        })

        post = Post.objects.create(
            author = user,
            text=content,
            title=title,
            format=category
        )
        
        serlializer = ReadPost(post)
        return JsonResponse({
            "code" : "11101",
	        "message" : "게시글을 성공적으로 올렸습니다.",
	        "status" : 201,
            "info" : serlializer.data
        }, status=201)
        
@csrf_exempt
def PostEditView(request, post_id):
    try :
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({
            "code" : "01001",
            "message" : "게시글이 삭제 되었거나 존재하지 않습니다.",
            "status" : 404
        }, status=301)

    if request.method == 'GET':
        serializer = ReadPost(post)
        return JsonResponse({
            "code" : "11001",
            "message" : "게시판 목록을 불러 왔습니다.",
            "status" : 200,
            "info" : serializer.data
        }, status=200)
        
    if request.method == 'PUT':
        try :data = JSONParser().parse(request)
        except : return JsonResponse({
            "code" : "01110",
	        "message" : "Json 형식이 잘못되었습니다.",
	        "status" : 400
        }, status=400)

        serializer = EditPost(post, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "code" : "11101",
                "message" : "게시글을 성공적으로 수정하였습니다.",
                "status" : 201
            }, status=201)
        return JsonResponse({
            "code" : "01102",
            "message" : "문법이 잘못 되었습니다.",
            "status" : 405,
            "info" : {
                "response" : f"{data}"
            }
        })

    if request.method == 'DELETE':
        post.delete()
        return JsonResponse({
            "code" : "11102",
            "message" : "게시글을 성공적으로 삭제하였습니다.",
            "status" : 200
        }, status=200)


def GetNotice(request) :
    if request.method == 'GET':
        try : 
            page = int(request.GET['page'])
            start = 10 * (page - 1)
            end = 10 * (page)
        except : 
            page = 0
            start = 0
            end = 10
        try : grade = int(request.GET['gradecode'])
        except : grade = 0
        print(f'grade : {grade}')
        if grade == 0 :
            posts = Post.objects.filter(format=3).order_by('-id')[start : end]
        else :
            posts = Post.objects.filter(format=3).filter(author__grade_number=grade).order_by('-id')[start : end]

        serializer = ReadPost(posts, many=True)

        return JsonResponse({
            "code" : "10091",
            "message" : "공지사항를 성공적으로 불러 왔습니다.",
            "status" : 200,
            "info" : serializer.data
        }, status=200)

        
