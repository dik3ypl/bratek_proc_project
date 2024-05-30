from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from panel.controllers import group_controller
from panel.enums.role import Role
from panel.forms.group_form import GroupForm
from panel.forms.join_group_as_instructor_form import JoinGroupAsInstructorForm
from panel.forms.join_group_as_student_form import JoinGroupAsStudentForm
from panel.models import Group
from panel.models.group import GroupMembership


@login_required
def create(request):
    form = GroupForm()
    if request.method == 'POST':
        new_group = group_controller.create_group(request.POST, request.user, request.FILES)
        if new_group:
            messages.success(request, 'New group created')
            return redirect('dashboard')

        messages.error(request, 'Cannot create a new group')
        form = GroupForm(request.POST, request.FILES)

    return render(request, 'panel/create_group.html', {'form': form})


@login_required
def join_group(request):
    student_form = JoinGroupAsStudentForm()
    instructor_form = JoinGroupAsInstructorForm()
    return render(request, 'panel/join_group.html', {'student_form': student_form, 'instructor_form': instructor_form})


@login_required
@require_http_methods(["POST"])
def join_group_as_student(request):
    form = JoinGroupAsStudentForm(request.POST)
    if form.is_valid():
        join_code = form.cleaned_data['join_code_student']
        group = Group.objects.filter(join_code=join_code).first()
        if group and request.user is not group.creator:
            GroupMembership.objects.create(group=group, user=request.user, role=Role.STUDENT)
            messages.success(request, 'You have successfully joined the group as a student')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid join code for student')
    else:
        messages.error(request, 'Invalid form submission')
    return redirect('join_group')


@login_required
@require_http_methods(["POST"])
def join_group_as_instructor(request):
    form = JoinGroupAsInstructorForm(request.POST)
    if form.is_valid():
        join_code = form.cleaned_data['join_code_instructor']
        group = Group.objects.filter(join_code_for_instructor=join_code).first()
        if group is not group.creator:
            GroupMembership.objects.create(group=group, user=request.user, role=Role.INSTRUCTOR)
            messages.success(request, 'You have successfully joined the group as an instructor')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid join code for instructor')
    else:
        messages.error(request, 'Invalid form submission')
    return redirect('join_group')


@login_required
def my_groups(request):
    user = request.user

    role_filter = request.GET.get('role')
    user_filter = request.GET.get('user')
    group_name_filter = request.GET.get('group_name')

    created_groups = Group.objects.filter(creator=user)
    instructor_groups = Group.objects.filter(memberships__user=user, memberships__role=Role.INSTRUCTOR)
    student_groups = Group.objects.filter(memberships__user=user, memberships__role=Role.STUDENT)

    groups_with_roles = []

    for group in created_groups:
        groups_with_roles.append({'group': group, 'role': 'OWNER'})

    for group in instructor_groups:
        groups_with_roles.append({'group': group, 'role': 'INSTRUCTOR'})

    for group in student_groups:
        groups_with_roles.append({'group': group, 'role': 'STUDENT'})

    if role_filter:
        groups_with_roles = [g for g in groups_with_roles if g['role'] == role_filter.upper()]

    if user_filter:
        groups_with_roles = [g for g in groups_with_roles if
                             user_filter.lower() in g['group'].creator.get_full_name().lower()]

    if group_name_filter:
        groups_with_roles = [g for g in groups_with_roles if group_name_filter.lower() in g['group'].name.lower()]

    return render(request, 'panel/my_groups.html', {'title': 'My Groups', 'groups_with_roles': groups_with_roles})
