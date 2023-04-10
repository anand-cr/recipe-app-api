from rest_framework.routers import DefaultRouter
from recipe import views
from django.urls import include, path

router = DefaultRouter()
# This creates the recipe endpont and it will have autogenerated urls depending on the functionality that is enabled in the view
router.register('recipes', views.RecipeViewSet)
router.register('tag', views.TagViewSet)
app_name = 'recipe'  # for the tests

urlpatterns = [
    path('', include(router.urls)),
]
