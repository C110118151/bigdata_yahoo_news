from django.urls import path
from . import views

app_name="core"

urlpatterns = [
    path('', views.home, name='home'),
    path('get_city_news_titles', views.get_city_news_titles, name='get_city_news_titles'),
]



# app_name="core"

# urlpatterns = [
    
#     # the first way:
#     path('', views.home, name='home'),
#     path('api_get_top_userkey/', views.api_get_top_userkey),

# ]
