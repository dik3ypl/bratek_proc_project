from django.core.files.storage import default_storage
from ..models import TestCase
import subprocess
import time


def run_tests(solution):
    test_cases = TestCase.objects.filter(task=solution.task)
    results = {}

    file_content = default_storage.open(solution.solution_file.name).read()

    for test_case in test_cases:
        input_data = test_case.input_data.encode()

        start_time = time.time()

        process = subprocess.Popen(['python3', solution.solution_file.path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate(input=input_data)

        end_time = time.time()
        execution_time = end_time - start_time

        if process.returncode != 0:
            results[test_case.id] = {'error': error.decode(), 'execution_time': execution_time}
        else:
            actual_output = output.decode()
            expected_output = test_case.expected_output.strip()
            if actual_output.strip() == expected_output:
                results[test_case.id] = {'result': 'Pass', 'execution_time': execution_time}
            else:
                results[test_case.id] = {'result': 'Fail', 'actual_output': actual_output, 'execution_time': execution_time}

    return results
