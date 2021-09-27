from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
	path('<int:quiz_id>/',views.fill),
	path('<int:quiz_id>/edit', views.edit_quiz),
	path('query',views.search_quizzes),
	path('<int:quiz_id>/score',views.score_quiz),
]