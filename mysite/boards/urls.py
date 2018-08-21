from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'boards'
urlpatterns = [
    path('', views.BoardListView.as_view(), name="index"),
    path('boards/<int:pk>/', views.board_topics, name="board_topics"), # boards/1/
    path('boards/<int:pk>/new/', views.new_topic, name="new_topic"),
    
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
    name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
    name='password_change_done'),
    
    path('boards/<int:pk>/topics/<int:topic_pk>/', views.PostListView.as_view(), name="topic_posts"),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/', views.topic_reply, name="topic_reply"),

    path('boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/', views.PostUpdateView.as_view(), name="edit_post")   
]