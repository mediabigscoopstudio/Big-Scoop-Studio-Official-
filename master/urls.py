from django.contrib import admin
from django.urls import path,include
from master import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
urlpatterns = [
    path('', include('core.urls')),
    path("admin/", admin.site.urls),#backdoor access

    path("signin",views.signin_view,name='signin'),
    path("logout",views.logout_view,name='logout'),
    
    path("",views.index,name='index'),
    # Team Management
    path("teams",views.teams,name='teams'),
    path('add_user', views.add_user, name='add_user'),
    # Client Management
    path('clients', views.clients, name='clients'),
    path('add_client', views.add_client, name='add_client'),
    # Client Management
    path('projects', views.projects, name='projects'),
    path('save_project', views.save_project, name='save_project'),
    path('project_details/<int:id>/',views.project_details,name='project_details'),
    path('projects/<int:project_id>/save-task/',views.save_task,name='save_task'),
    path('task/<int:task_id>/update-status/',views.update_task_status,name='update_task_status'),
    # My Task Management
    path('my-tasks/',views.my_tasks,name='my_tasks'),
    path('my-tasks/update/<int:task_id>/',views.update_my_task_status,name='update_my_task_status'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)