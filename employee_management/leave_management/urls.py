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
    
    # Leave Type
    path('leave-type/create', views.create_leave_type, name='create_leave_type'),
    path('leave-type/list', views.get_leave_type, name='list_leave_type'),
    path('leave-type/view/<int:id>', views.get_leave_type, name='view_leave_type'),
    path('leave-type/update/<int:id>', views.updated_deleted_leave_type, name='updated_leave_type'),
    path('leave-type/delete/<int:id>', views.updated_deleted_leave_type, name='deleted_leave_type'),
    
    # Leave Application
    path('leave-application/create', views.create_leave_application, name='create_leave_application'),
    # path('leave-application/list', views.get_leave_application, name='list_leave_application'),
    # path('leave-application/view/<int:id>', views.get_leave_application, name='view_leave_application'),
    path('leave-application/update/<int:id>', views.update_leave_application, name='updated_leave_application'),
    #path('leave-application/delete/<int:id>', views.delete_leave_application, name='deleted_leave_application'),
    # path('leave-application/status-update/<int:id>', views.update_leave_application_status, name='status_update_leave_application'),
    # path('leave-application/reliever-update/<int:id>', views.update_leave_application_reliever, name='reliever_update_leave_application'),
    path('leave-application/history/<int:id>', views.leave_application_history, name='leave_application_history'),
    
    # Leave Balance
    path('leave-balance', views.leave_balance, name='leave_balance'),
    
    # Leave History
    # path('leave-history/list', views.get_leave_history, name='list_leave_history'),
    # path('leave-history/view/<int:id>', views.get_leave_history, name='view_leave_history'),
]
