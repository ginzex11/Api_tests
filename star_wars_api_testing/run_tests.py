# run_tests.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from star_wars_api_testing.core.logger import TestLogger
import pytest
from datetime import datetime
from star_wars_api_testing.config.test_config import TestConfig

def main():
    # Setup logging
    logger = TestLogger('test_runner')
    
    # Create necessary directories
    os.makedirs(TestConfig.LOG_DIR, exist_ok=True)
    os.makedirs(TestConfig.DATA_DIR / "test_data", exist_ok=True)
    os.makedirs(TestConfig.DATA_DIR / "results", exist_ok=True)
    
    logger.start_test(
        test_name="Test Suite Execution",
        description="Running all tests in the test suite"
    )
    
    # Run pytest 
    args = [
        "star_wars_api_testing/tests/",  
        "-v",
        "-s"  
    ]
    
    # Run pytest
    try:
        result = pytest.main(args)
        if result == 0:
            logger.end_test(status="PASS")
            logger.log_step(
                step="All tests executed",
                expected="All tests should pass",
                actual="All tests passed",
                status="PASS"
            )
        elif result == 5:  # pytest exit code for no tests ran
            logger.end_test(status="WARNING")
            logger.log_step(
                step="Test execution",
                expected="Tests should run",
                actual="No tests were found or executed",
                status="WARNING"
            )
        else:
            logger.end_test(status="FAIL")
            logger.log_step(
                step="Test execution",
                expected="All tests should pass",
                actual=f"Tests failed or had errors. Exit code: {result}",
                status="FAIL"
            )
    except Exception as e:
        logger.end_test(status="ERROR")
        logger.log_step(
            step="Test execution",
            expected="Tests should run without errors",
            actual=str(e),
            status="ERROR"
        )

    logger.save_report()

if __name__ == "__main__":
    main()