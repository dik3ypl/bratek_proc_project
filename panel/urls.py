from django.urls import path

from .views import dashboard_views, task_views, solutions_views, group_views

urlpatterns = [
    path('', dashboard_views.dashboard, name='dashboard'),

    path('group/create', group_views.create, name='group_create'),

    path('groups/mine', group_views.my_groups, name='my_groups'),

    path('join-group/', group_views.join_group, name='join_group'),
    path('join-group-as-student/', group_views.join_group_as_student, name='join_group_as_student'),
    path('join-group-as-instructor/', group_views.join_group_as_instructor, name='join_group_as_instructor'),

    path('submit_solution/<int:task_id>/', solutions_views.submit_solution, name='submit_solution'),
    path('tasks/', task_views.view_tasks, name='view_tasks'),
]
