from django.contrib import admin
from django.urls import path
from newsapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.home_page, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('category/<slug:category_name_slug>/<slug:news_number_slug>', views.news, name='each_news_page'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
