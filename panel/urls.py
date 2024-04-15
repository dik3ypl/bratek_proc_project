from django.urls import path

from .views import dashboard_views, task_views, solutions_views

urlpatterns = [
    path('', dashboard_views.dashboard, name='dashboard'),
    path('submit_solution/<int:task_id>/', solutions_views.submit_solution, name='submit_solution'),
    path('tasks/', task_views.view_tasks, name='view_tasks'),
]
