from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('<int:city_id>/', views.city_dashboard),
    path('profile/<int:user_id>/', views.show_profile),
    path('new/', views.new_activity),
    path('show/<int:activity_id>/', views.show_activity),
    path('edit/<int:activity_id>/', views.edit_activity),
    path('update/<int:activity_id>/', views.update_activity),
    path('about/', views.about_us),
    path('create/', views.create_activity),
    path('delete/<int:activity_id>/', views.delete_activity),
    path('like_activity/<int:activity_id>/', views.like_activity),
    path('dislike_activity/<int:activity_id>/', views.dislike_activity),
    path('random/', views.show_random),
    path('random/get/', views.pick_random),
    path('add_city/', views.add_city),
    path('create_city/', views.create_city),
]