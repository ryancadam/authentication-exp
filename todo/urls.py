"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # authorization
    path('signup/', views.usersignup, name='usersignup'),
    path('logout/', views.userlogout, name='userlogout'),
    path('login/', views.userlogin, name='userlogin'),

    # todo
    path('current/', views.current, name='current'),
    path('completed/', views.completed, name='completed'),
    path('create/', views.create, name='create'),
    path('', views.home, name='home'),
    path('todo/<int:todo_pk>', views.seetodo, name='seetodo'),
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),
]
