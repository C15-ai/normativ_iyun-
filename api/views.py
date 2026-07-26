from linecache import cache

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from rest_framework.views import APIView

from api.models import Post
from api.serializers import PostSerializer, RegisterSerializer
from api.tasks import salom_task, sleep_task
from api.throttles import PostCreateThrottle


# def salom(request):
#     return  JsonResponse({'massage':'Hello DRF'})


# class PostListCreateAPIView(APIView):
#
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer_class = PostSerializer
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self,request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class PostDetailAPIView(APIView):
#
#     def get(self, request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request,pk):
#         post = get_object_or_404(Post, pk=pk)
#         serializer = PostSerializer(post, request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request,pk):
#         post = get_object_or_404(Post, pk=pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



@method_decorator(cache_page(60) , name="list")
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]

    filterset_fields = ['title','created_at']

    search_fields = ['title','content']
    ordering_fields = ['created_at' , 'title']

    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        cache.clear()
    def perform_update(self, serializer):
        serializer.save()
        cache.clear()
    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()
    def get_throttles(self):
        if self.action == "create":
            return [PostCreateThrottle]
        return super().get_throttles()





class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            print(request.data)
            return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)
        return JsonResponse({'status': 'fail'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self,request):
        logout(request)
        return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)



class TestView(APIView):
    def get(self , request):
        salom_task.delay()
        sleep_task.delay()

        return Response({
            "massage" : "ikkalasiyam ishladi"
        })




