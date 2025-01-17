from django.contrib import admin
from django.urls import path
from stack import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('subscribe/<int:author_id>/', views.subscribe, name='subscribe'),
    path('unsubscribe/<int:author_id>/', views.unsubscribe, name='unsubscribe'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)