from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('result/<int:result_id>/', views.view_result, name='view_result'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_view, name='profile'),
]
