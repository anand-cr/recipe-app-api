from rest_framework.routers import DefaultRouter
from . import views
from django.urls import include, path


app_user = 'user'

urlpatterns = [
    # any request passed to /create will be handled by this view
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name="token"),
    path('me/', views.ManageUserView.as_view(), name="me")
]
