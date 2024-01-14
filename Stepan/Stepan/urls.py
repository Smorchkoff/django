"""
URL configuration for Stepan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ChitayGorod import views
from Stepan import settings

change_url = [
    path('password', views.change_password, name='password'),
    path('email', views.change_email, name='email'),
    path('login', views.change_login, name='login')
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book_create/', views.book_create, name='book_create'),
    path('favourite/', views.show_favorite_books, name='favourite'),
    path('profile/', views.show_profile, name='profile'),
    path('edit_profle/', views.edit_profile, name='edit_profile'),
    path('change/password', views.change_password, name='change_password'),
    path('change/login', views.change_login, name='change_login'),
    path('change/email', views.change_email, name='change_email'),
    path('book/<int:book_id>', views.showBook, name='book'),
    path('author/<int:author_id>', views.showAuthor, name='author'),
    path('books/', views.showBooks, name='books'),
    path('authors/', views.showAuthors, name='authors'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('favorites/', views.show_favorite_books, name='favorites'),
    path('profile/', views.show_profile, name='profile'),
    path('', views.index, name='catalog'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
