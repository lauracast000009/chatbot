from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet, ExerciseResultViewSet, chat_interact

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'results', ExerciseResultViewSet, basename='result')

urlpatterns = [
    path('', include(router.urls)),
    path('chat/', chat_interact, name='chat_interact'),
]
