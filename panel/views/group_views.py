from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from panel.controllers import group_controller
from panel.forms.group_form import GroupForm
from panel.models import Group


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
def my_groups(request):
    user_groups = Group.objects.filter(creator=request.user)
    return render(request, 'panel/groups.html', {'title': 'My groups', 'groups': user_groups})
