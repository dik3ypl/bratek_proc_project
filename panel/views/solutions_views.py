from django.shortcuts import render, redirect
from ..forms import SolutionForm
from django.contrib.auth.decorators import login_required
from ..functions import run_tests
from ..models import Solution, Task


@login_required
def submit_solution(request, task_id):
    if request.method == 'POST':
        form = SolutionForm(request.POST, request.FILES)

        if form.is_valid():
            solution = form.save()
            results = run_tests(solution)
            solution.test_results = results
            solution.save()
            return redirect('submit_solution', task_id=solution.task.id)
    else:
        form = SolutionForm(initial={'task': task_id, 'user': request.user})

    previous_solutions = Solution.objects.filter(user=request.user, task_id=task_id)
    task = Task.objects.get(id=task_id)

    return render(request, 'panel/submit_solution.html',
                  {'task': task, 'form': form, 'task_id': task_id, 'previous_solutions': previous_solutions,
                   'user': request.user})