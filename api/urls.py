from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (PostViewSet, RegisterView, LoginView, LogoutView, TestView, )

router = DefaultRouter()
router.register("posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("test-task/", TestView.as_view()),
]
# urlpatterns = [
#     # path('api/hello/', salom),
#     path('api/v1/posts/list-create/', PostListCreateAPIView.as_view()),
#     path('api/v1/posts/detail/<int:pk>/', PostDetailAPIView.as_view()),
#
# ]


# urlpatterns = [
#     path("", include(router.urls)),
#
#     path("register/", RegisterView.as_view()),
#     path("login/", LoginView.as_view()),
#     path("logout/", LogoutView.as_view()),
# ]




