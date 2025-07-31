from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
import os

app_name = 'Calls'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('new_call/', views.new_call, name='new_call'),
    path('user_calls/', views.user_calls, name='user_calls'),
    path('admin_calls/', views.admin_calls, name='admin_calls'),
    path('users/', views.users_view, name='users_view'),
    path('view/<int:chamado_id>/', views.view, name='view'),
    path('change_status/<int:chamado_id>/', views.change_status, name='change_status'),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))