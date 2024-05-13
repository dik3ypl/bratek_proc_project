from ..forms.group_form import GroupForm
from ..models import Group


def create_group(form_data, user, files=None):
    form = GroupForm(form_data, files)
    if form.is_valid():
        group = form.save(commit=False)
        group.creator = user
        group.save()
        return group
    else:
        return None
