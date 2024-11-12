from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'),
    path('user/change-password', views.change_password, name='change_password'),
    path('admin/login', views.login_admin, name='admin_login'),
    path('user/view/<str:username>', views.user_get_view,name='user_view'),
    path('user/<int:id>', views.get_by_user_id,name='user_view_by_id'),
    path('user/list', views.user_get_list, name='user_list'),
    path('user/delete/<int:id>', views.updated_deleted_user, name='user_deleted'),
    path('user/update/<int:id>', views.updated_deleted_user, name='user_updated'),
    path('logout',views.logout_user, name='logout'),
    
    # Department
    path('department/create', views.create_department, name='create_department'),
    path('department/list', views.get_department, name='list_department'),
    path('department/view/<int:id>', views.get_department, name='view_department'),
    path('department/update/<int:id>', views.updated_deleted_department, name='updated_department'),
    path('department/delete/<int:id>', views.updated_deleted_department, name='deleted_department'),
    # Additional CRUD endpoints for models can be added here
]
