from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from ..models import Task, Solution, Group, GroupMembership


@login_required
def view_tasks(request):
    user = request.user

    user_groups = Group.objects.filter(memberships__user=user) | Group.objects.filter(creator=user)

    tasks = Task.objects.filter(group__in=user_groups)

    group_filter = request.GET.get('group')
    task_name_filter = request.GET.get('task_name')
    role_filter = request.GET.get('role')
    is_active_filter = request.GET.get('is_active')

    if group_filter:
        tasks = tasks.filter(group__id=group_filter)

    if task_name_filter:
        tasks = tasks.filter(title__icontains=task_name_filter)

    tasks_with_submission = []
    for task in tasks:
        submitted_solutions_count = Solution.objects.filter(user=user, task=task).count()
        is_submitted = submitted_solutions_count > 0

        is_active = True
        if task.end_date and task.end_date < timezone.now():
            is_active = False
        if task.max_attempts and submitted_solutions_count >= task.max_attempts:
            is_active = False

        if is_active_filter:
            if is_active_filter == 'yes' and not is_active:
                continue
            if is_active_filter == 'no' and is_active:
                continue

        user_role = GroupMembership.objects.filter(group=task.group, user=user).first()
        if user_role:
            user_role = user_role.role
        else:
            user_role = 'Unknown'

        if role_filter and role_filter != user_role:
            continue

        tasks_with_submission.append({
            'id': task.id,
            'title': task.title,
            'group': task.group,
            'description': task.description,
            'submitted': is_submitted,
            'max_attempts': task.max_attempts if task.max_attempts else 'Unlimited',
            'end_date': task.end_date if task.end_date else 'No deadline',
            'is_active': is_active,
            'role': user_role
        })

    return render(request, 'panel/view_tasks.html', {
        'title': 'My Tasks',
        'tasks': tasks_with_submission,
        'user_groups': user_groups,
        'group_filter': group_filter,
        'task_name_filter': task_name_filter,
        'role_filter': role_filter,
        'is_active_filter': is_active_filter
    })
