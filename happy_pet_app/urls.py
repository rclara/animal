from django.urls import path
from.import views


urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register_user),
    path('success', views.success),
    path('forgot', views.forgot),
    ############################
    path('dashboard', views.dashboard),
    path('add_pet', views.register_pet),
    path('pet_portal/<int:id>', views.pet_portal),
    path('daily_log/<int:id>', views.daily_log)
]