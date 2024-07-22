from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('category/<str:cat>', views.category, name='category'),
    path('register/', views.register_user, name='register'),
    path('product/<int:pk>', views.product, name='product'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_info/', views.update_info, name='update_info'),    
    path('add_product/', views.add_product, name='add_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('list_products/', views.list_products, name='list_products'),
]