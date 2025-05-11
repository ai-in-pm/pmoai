from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from pmoai.task import Task


class TaskTestCase(BaseModel):
    """Represents a test case for a task."""
    
    name: str = Field(description="The name of the test case.")
    description: str = Field(description="A description of the test case.")
    inputs: Dict[str, Any] = Field(description="The inputs for the test case.")
    expected_output: Optional[Dict[str, Any]] = Field(None, description="The expected output for the test case.")
    expected_output_contains: Optional[List[str]] = Field(None, description="Strings that should be in the output.")
    expected_output_excludes: Optional[List[str]] = Field(None, description="Strings that should not be in the output.")


class TaskTestResult(BaseModel):
    """Represents the result of a task test."""
    
    test_case: TaskTestCase = Field(description="The test case that was executed.")
    passed: bool = Field(description="Whether the test passed.")
    actual_output: Any = Field(description="The actual output of the test.")
    error: Optional[str] = Field(None, description="The error message if the test failed.")
    execution_time: float = Field(description="The execution time of the test in seconds.")


class TaskTester(BaseModel):
    """Tests tasks with various test cases."""
    
    def test_task(
        self, task: Task, test_cases: List[TaskTestCase]
    ) -> List[TaskTestResult]:
        """Test a task with a list of test cases.
        
        Args:
            task: The task to test.
            test_cases: The test cases to run.
            
        Returns:
            The results of the tests.
        """
        results = []
        
        for test_case in test_cases:
            result = self._run_test_case(task, test_case)
            results.append(result)
        
        return results
    
    def _run_test_case(self, task: Task, test_case: TaskTestCase) -> TaskTestResult:
        """Run a single test case for a task.
        
        Args:
            task: The task to test.
            test_case: The test case to run.
            
        Returns:
            The result of the test.
        """
        import time
        
        # Execute the task and measure execution time
        start_time = time.time()
        try:
            result = task.execute(inputs=test_case.inputs)
            actual_output = result.raw
            execution_time = time.time() - start_time
            
            # Determine if the test passed
            passed = self._check_test_result(test_case, actual_output)
            
            return TaskTestResult(
                test_case=test_case,
                passed=passed,
                actual_output=actual_output,
                execution_time=execution_time,
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return TaskTestResult(
                test_case=test_case,
                passed=False,
                actual_output=None,
                error=str(e),
                execution_time=execution_time,
            )
    
    def _check_test_result(self, test_case: TaskTestCase, actual_output: Any) -> bool:
        """Check if the test result matches the expected output.
        
        Args:
            test_case: The test case to check.
            actual_output: The actual output of the test.
            
        Returns:
            Whether the test passed.
        """
        # Check exact match if expected_output is provided
        if test_case.expected_output is not None:
            return actual_output == test_case.expected_output
        
        # Check if output contains expected strings
        if test_case.expected_output_contains:
            for expected_str in test_case.expected_output_contains:
                if expected_str not in str(actual_output):
                    return False
        
        # Check if output excludes certain strings
        if test_case.expected_output_excludes:
            for excluded_str in test_case.expected_output_excludes:
                if excluded_str in str(actual_output):
                    return False
        
        # If no specific checks were provided, or all checks passed, the test passes
        return True
    
    def generate_report(self, results: List[TaskTestResult]) -> str:
        """Generate a report of test results.
        
        Args:
            results: The test results to include in the report.
            
        Returns:
            A formatted report of the test results.
        """
        total_tests = len(results)
        passed_tests = sum(1 for result in results if result.passed)
        failed_tests = total_tests - passed_tests
        
        report = f"""
# Task Test Report

## Summary
- Total Tests: {total_tests}
- Passed: {passed_tests}
- Failed: {failed_tests}
- Success Rate: {(passed_tests / total_tests) * 100:.2f}%

## Test Results
"""
        
        for i, result in enumerate(results, 1):
            status = "✅ PASSED" if result.passed else "❌ FAILED"
            report += f"""
### Test {i}: {result.test_case.name} - {status}
- Description: {result.test_case.description}
- Execution Time: {result.execution_time:.2f} seconds
"""
            
            if not result.passed and result.error:
                report += f"- Error: {result.error}\n"
        
        return report
