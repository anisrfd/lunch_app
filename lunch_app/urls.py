from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from restaurant_app.views import (restaurant_create, menu_upload, employee_create, today_menu, vote_for_menu,
                                  register, get_winner, logout_view, )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', register, name='register'),
    path('restaurant/create/', restaurant_create, name='create_restaurant'),
    path('restaurant/<int:id>/menu/upload/', menu_upload, name='upload_menu'),
    path('employee/create/', employee_create, name='create_employee'),
    path('menu/today/', today_menu, name='today_menu'),
    path('menu/<int:menu_id>/vote/', vote_for_menu, name='vote_menu'),
    path('menu/results/', get_winner, name='results'),
    path('logout/', logout_view, name='logout'),
]
