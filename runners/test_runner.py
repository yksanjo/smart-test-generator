"""Test Runner - Executes generated tests and collects results."""

import subprocess
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class TestRunner:
    """Runs generated tests and collects results."""
    
    def __init__(self):
        self.results: Dict[str, Any] = {}
        
    def run(self, test_dir: Path, test_files: List[str]) -> Dict[str, Any]:
        """Run all generated tests.
        
        Args:
            test_dir: Directory containing test files.
            test_files: List of test file paths.
            
        Returns:
            Dictionary containing test results.
        """
        results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0,
            "total": 0,
            "duration": 0,
            "failed_tests": [],
            "test_files": []
        }
        
        if not test_files:
            print("  ⚠️  No test files to run")
            return results
        
        start_time = time.time()
        
        # Run pytest on all test files
        try:
            result = self._run_pytest(test_dir)
            
            # Parse results
            if result.returncode == 0:
                results["passed"] = len(test_files)
                results["total"] = len(test_files)
            else:
                results = self._parse_pytest_output(result.stdout, results)
                
        except Exception as e:
            print(f"  ❌ Error running tests: {e}")
            results["errors"] = len(test_files)
            results["failed_tests"].append(str(e))
        
        results["duration"] = time.time() - start_time
        
        self.results = results
        return results
    
    def _run_pytest(self, test_dir: Path) -> subprocess.CompletedProcess:
        """Run pytest on test directory.
        
        Args:
            test_dir: Directory containing test files.
            
        Returns:
            CompletedProcess instance.
        """
        # Run pytest with verbose output
        cmd = [
            "python", "-m", "pytest",
            str(test_dir),
            "-v",
            "--tb=short",
            "--no-header",
            "-q"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        return result
    
    def _parse_pytest_output(self, output: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """Parse pytest output to extract test results.
        
        Args:
            output: Pytest stdout/stderr output.
            results: Results dictionary to update.
            
        Returns:
            Updated results dictionary.
        """
        lines = output.split('\n')
        
        # Look for pytest summary line
        for line in lines:
            if 'passed' in line or 'failed' in line or 'error' in line:
                # Parse summary like "5 passed, 2 failed"
                if 'passed' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'passed':
                            try:
                                results["passed"] = int(parts[i-1])
                            except (ValueError, IndexError):
                                pass
                
                if 'failed' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'failed':
                            try:
                                results["failed"] = int(parts[i-1])
                            except (ValueError, IndexError):
                                pass
                            
                if 'error' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'error':
                            try:
                                results["errors"] = int(parts[i-1])
                            except (ValueError, IndexError):
                                pass
                            
                if 'skipped' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'skipped':
                            try:
                                results["skipped"] = int(parts[i-1])
                            except (ValueError, IndexError):
                                pass
        
        # Calculate total
        results["total"] = results["passed"] + results["failed"] + results["errors"] + results["skipped"]
        
        # Extract failed test names
        for line in lines:
            if 'FAILED' in line or 'ERROR' in line:
                # Extract test name
                if '::' in line:
                    test_name = line.split('::')[-1].strip()
                    results["failed_tests"].append(test_name)
        
        return results
    
    def run_single_test(self, test_file: Path, test_name: Optional[str] = None) -> Dict[str, Any]:
        """Run a single test file or test function.
        
        Args:
            test_file: Path to test file.
            test_name: Optional specific test function name.
            
        Returns:
            Dictionary containing test results.
        """
        results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0,
            "duration": 0,
            "failed_tests": []
        }
        
        cmd = [
            "python", "-m", "pytest",
            str(test_file),
            "-v"
        ]
        
        if test_name:
            cmd.extend(["-k", test_name])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            results = self._parse_pytest_output(result.stdout, results)
            
        except subprocess.TimeoutExpired:
            results["errors"] = 1
            results["failed_tests"].append("Test timed out")
        except Exception as e:
            results["errors"] = 1
            results["failed_tests"].append(str(e))
        
        return results
    
    def run_with_coverage(self, test_dir: Path, source_dir: Path) -> Dict[str, Any]:
        """Run tests with coverage reporting.
        
        Args:
            test_dir: Directory containing test files.
            source_dir: Directory containing source code to measure coverage for.
            
        Returns:
            Dictionary containing test results with coverage.
        """
        results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0,
            "total": 0,
            "duration": 0,
            "coverage": {}
        }
        
        cmd = [
            "python", "-m", "pytest",
            str(test_dir),
            "--cov", str(source_dir),
            "--cov-report", "json",
            "-v"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            results = self._parse_pytest_output(result.stdout, results)
            
            # Try to read coverage data
            coverage_file = Path("coverage.json")
            if coverage_file.exists():
                with open(coverage_file, 'r') as f:
                    coverage_data = json.load(f)
                    results["coverage"] = coverage_data.get("totals", {})
                    
        except Exception as e:
            results["errors"] = 1
            print(f"Error running tests with coverage: {e}")
        
        return results
    
    def get_test_summary(self) -> str:
        """Get a human-readable summary of test results.
        
        Returns:
            Summary string.
        """
        if not self.results:
            return "No tests run yet."
        
        summary = []
        summary.append("=" * 50)
        summary.append("TEST RESULTS SUMMARY")
        summary.append("=" * 50)
        summary.append(f"Total: {self.results.get('total', 0)}")
        summary.append(f"Passed: {self.results.get('passed', 0)}")
        summary.append(f"Failed: {self.results.get('failed', 0)}")
        summary.append(f"Skipped: {self.results.get('skipped', 0)}")
        summary.append(f"Errors: {self.results.get('errors', 0)}")
        summary.append(f"Duration: {self.results.get('duration', 0):.2f}s")
        
        if self.results.get('failed_tests'):
            summary.append("")
            summary.append("Failed Tests:")
            for test in self.results['failed_tests']:
                summary.append(f"  - {test}")
        
        summary.append("=" * 50)
        
        return "\n".join(summary)
