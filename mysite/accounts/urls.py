from django.urls import path, re_path
from accounts import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.sign_up, name="sign_up"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    
    path('reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html',
                                                        email_template_name='password_reset_email.html',
                                                        subject_template_name='password_reset_subject.txt'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
    name='password_reset_done'),
    
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
    name='password_reset_confirm'),
    path('reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
    name='password_reset_complete'),

    path('account/', views.CustomUserUpdateView.as_view(), name="my_account"),
    
]
