from django.urls import path

from . import views

app_name = 'boards'
urlpatterns = [
    path('', views.index, name="index"),
    path('boards/<int:pk>/', views.board_topics, name="board_topics"), # boards/1/
    path('boards/<int:pk>/new/', views.new_topic, name="new_topic")
]