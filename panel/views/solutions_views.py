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
                  {'task': task,
                   'form': form,
                   'task_id': task_id,
                   'previous_solutions': previous_solutions,
                   'user': request.user,
                   'stats': count_stats(previous_solutions)
                   })


def count_stats(solutions):
    stats = {
        'solutions_number': len(solutions),
        'tests_number': 0,
        'tests_passed': 0,
        'tests_failed': 0,
        'average_test_time': 0,
        'total_time': 0,
    }
    results = []
    if len(solutions) == 0:
        return stats
    for solution in solutions:
        for value in solution.test_results.values():
            results.append(value)

    for result in results:
        if result['result'] == 'Pass':
            stats['tests_passed'] += 1
        else:
            stats['tests_failed'] += 1
        stats['total_time'] += result['execution_time']

    stats['tests_number'] = stats['tests_failed'] + stats['tests_passed']
    stats['average_test_time'] = stats['total_time'] / stats['tests_number']
    return stats
