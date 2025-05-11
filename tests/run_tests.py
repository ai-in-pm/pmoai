import unittest
import sys

def run_tests():
    """Run all tests in the tests directory."""
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(run_tests())
