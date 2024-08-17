from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser, Post
from .serializers import PostSerializer
from django.utils.decorators import method_decorator
from . models import CustomUser
from rest_framework import viewsets, permissions
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
import json

# Create your views here.

@csrf_exempt
def token(request):
    response = JsonResponse({'message': 'CSRF token set'})

    response.set_cookie('csrftoken', request.META.get('CSRF_COOKIE', ''), httponly=True)
    return response


def home(request):
    return HttpResponse('<h1> welcome to the underworld </h1>')

class HelloWorld(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, World!"})
@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    if request.method == 'POST':
    
        try:
            data = json.loads(request.body)
            User = get_user_model()
            user = User.objects.create_user(
                username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    first_name=data['first_name'],
                    last_name=data['last_name']
            )
            user.save()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return JsonResponse({'error': 'Invalid request method'}, status=405)    

    

#user loggin in
@api_view(['POST'])
def user_login(request):
    data = request.data
    user = authenticate(username=data['email'], password=data['password'])
    print(f"User: {user}")  # Debugging print statement

    
    if user is not None:
        # Check if a token already exists; if not, create one
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'message': 'Login successful',
            'auth_token': token.key
        }, status=200)
    else: 
        return JsonResponse({'error': 'Invalid username or password'}, status=401)


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        print("Delete account view hit.")
        print(f"User: {request.user}")
        print(f"Headers: {request.headers}")
        user = request.user
        user.delete()
        return JsonResponse({"detail": "Account deleted successfully."}, status=204)



@api_view(['POST'])
def create_post(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    # Ensure `post_type` is included in request data
    if 'post_type' not in request.data:
        return Response({'error': 'post_type is required'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PostListView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chatroom_id = self.kwargs['chatroom_pk']
        return Message.objects.filter(chatroom__id=chatroom_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    
   