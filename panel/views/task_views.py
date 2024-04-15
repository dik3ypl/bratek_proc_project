from django.shortcuts import render
from ..models import Task, Solution


def view_tasks(request):
    tasks = Task.objects.all()

    if request.user.is_authenticated:
        user_solutions = Solution.objects.filter(user=request.user)
        user_solutions_dict = {solution.task.id: True for solution in user_solutions}

    else:
        user_solutions_dict = {}

    return render(request, 'task/view_tasks.html', {'tasks': tasks, 'user_solutions_dict': user_solutions_dict})

