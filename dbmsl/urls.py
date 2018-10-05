"""dbms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path,include
from django.contrib import admin
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url('admin/', admin.site.urls),
    url('invoice/',views.invoice,name='invoice'),
    url('transaction/',views.my_transaction,name='my_transaction'),
    url('transactions/',views.transactions,name='transactions'),
    url('otp/',views.verifyotp,name='otp'),
    url('add_money/',views.add_money,name='add_money'),
    url('register/',views.register,name = 'register'),
    url('user/',views.user,name = 'user'),
    url('update/',views.update,name = 'update'),
    url('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    url('logout/',views.logout,name='logout'),
    url('profile/', views.profile, name='profile'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),
    path(
        'admin/password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='admin_password_reset',
    ),
    path(
        'admin/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
   # path('admin/doc',include('django.contrib.admindocs.urls')),
]
