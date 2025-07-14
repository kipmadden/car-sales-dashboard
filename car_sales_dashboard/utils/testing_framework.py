"""
Testing Framework and Code Quality Module

Provides comprehensive testing utilities, code quality checks,
and performance benchmarks for the Car Sales Dashboard.
"""

import unittest
import pytest
import pandas as pd
import numpy as np
import time
import psutil
import os
import sys
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from pathlib import Path

# Testing configuration
@dataclass
class TestConfig:
    """Configuration for testing framework"""
    test_data_size: int = 1000
    performance_threshold_ms: float = 100.0
    memory_threshold_mb: float = 50.0
    coverage_threshold: float = 0.80
    max_complexity: int = 10
    
    # Test data paths
    test_data_dir: Path = Path("tests/data")
    reports_dir: Path = Path("tests/reports")
    
    # Quality metrics
    code_quality_standards: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.code_quality_standards is None:
            self.code_quality_standards = {
                'max_line_length': 100,
                'max_function_length': 50,
                'max_class_length': 200,
                'min_test_coverage': 80,
                'max_cognitive_complexity': 15
            }


class TestDataGenerator:
    """Generate realistic test data for dashboard testing"""
    
    @staticmethod
    def generate_sales_data(
        rows: int = 1000,
        start_date: str = "2020-01-01",
        seed: int = 42
    ) -> pd.DataFrame:
        """Generate realistic car sales test data"""
        np.random.seed(seed)
        
        # Date range
        dates = pd.date_range(start=start_date, periods=rows, freq='D')
        
        # Base sales with trend and seasonality
        trend = np.linspace(100, 150, rows)
        seasonal = 20 * np.sin(2 * np.pi * np.arange(rows) / 365.25)
        noise = np.random.normal(0, 10, rows)
        sales_volume = np.maximum(0, trend + seasonal + noise)
        
        # Exogenous variables
        gas_price = 3.0 + 0.5 * np.sin(2 * np.pi * np.arange(rows) / 365.25) + np.random.normal(0, 0.2, rows)
        cpi = 200 + np.cumsum(np.random.normal(0, 1, rows))
        search_volume = 50 + 30 * np.sin(2 * np.pi * np.arange(rows) / 365.25) + np.random.normal(0, 5, rows)
        
        # Vehicle types
        vehicle_types = ['Sedan', 'SUV', 'Truck', 'Coupe', 'Hatchback']
        vehicle_type = np.random.choice(vehicle_types, rows)
        
        # Regions
        regions = ['North', 'South', 'East', 'West', 'Central']
        region = np.random.choice(regions, rows)
        
        # States
        states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI']
        state = np.random.choice(states, rows)
        
        # Models
        models = [f'Model_{chr(65+i)}' for i in range(10)]
        model = np.random.choice(models, rows)
        
        return pd.DataFrame({
            'date': dates,
            'sales_volume': sales_volume.round(0).astype(int),
            'gas_price': gas_price.round(2),
            'cpi': cpi.round(1),
            'search_volume': search_volume.round(0).astype(int),
            'vehicle_type': vehicle_type,
            'region': region,
            'state': state,
            'model': model,
            'sales': sales_volume.round(0).astype(int)  # Alias for compatibility
        })
    
    @staticmethod
    def generate_forecast_data(
        historical_data: pd.DataFrame,
        forecast_months: int = 12
    ) -> pd.DataFrame:
        """Generate realistic forecast data based on historical data"""
        last_date = historical_data['date'].max()
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=forecast_months * 30,
            freq='D'
        )
        
        # Simple trend continuation with uncertainty
        last_sales = historical_data['sales_volume'].tail(30).mean()
        trend = np.linspace(last_sales, last_sales * 1.1, len(future_dates))
        uncertainty = np.random.normal(0, last_sales * 0.1, len(future_dates))
        
        predicted_sales = np.maximum(0, trend + uncertainty)
        confidence_lower = predicted_sales * 0.8
        confidence_upper = predicted_sales * 1.2
        
        return pd.DataFrame({
            'date': future_dates,
            'predicted_sales': predicted_sales.round(0).astype(int),
            'confidence_lower': confidence_lower.round(0).astype(int),
            'confidence_upper': confidence_upper.round(0).astype(int)
        })


class PerformanceTester:
    """Performance testing and benchmarking utilities"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.results = []
    
    def measure_execution_time(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Measure function execution time"""
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
        
        end_time = time.perf_counter()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        memory_delta = end_memory - start_memory
        
        performance_result = {
            'function_name': func.__name__,
            'execution_time_ms': execution_time,
            'memory_usage_mb': memory_delta,
            'success': success,
            'error': error,
            'result_size': len(str(result)) if result else 0,
            'timestamp': time.time()
        }
        
        self.results.append(performance_result)
        return performance_result
    
    def benchmark_data_operations(self) -> Dict[str, Any]:
        """Benchmark common data operations"""
        test_data = TestDataGenerator.generate_sales_data(self.config.test_data_size)
        
        benchmarks = {}
        
        # Data loading
        def load_data():
            return TestDataGenerator.generate_sales_data(1000)
        benchmarks['data_loading'] = self.measure_execution_time(load_data)
        
        # Data filtering
        def filter_data():
            return test_data[test_data['sales_volume'] > test_data['sales_volume'].mean()]
        benchmarks['data_filtering'] = self.measure_execution_time(filter_data)
        
        # Data aggregation
        def aggregate_data():
            return test_data.groupby('vehicle_type')['sales_volume'].agg(['sum', 'mean', 'count'])
        benchmarks['data_aggregation'] = self.measure_execution_time(aggregate_data)
        
        # Data sorting
        def sort_data():
            return test_data.sort_values(['date', 'sales_volume'])
        benchmarks['data_sorting'] = self.measure_execution_time(sort_data)
        
        return benchmarks
    
    def check_performance_thresholds(self, results: Dict[str, Any]) -> Dict[str, bool]:
        """Check if performance meets defined thresholds"""
        checks = {}
        
        for operation, result in results.items():
            # Time threshold check
            time_ok = result['execution_time_ms'] <= self.config.performance_threshold_ms
            
            # Memory threshold check
            memory_ok = result['memory_usage_mb'] <= self.config.memory_threshold_mb
            
            # Success check
            success_ok = result['success']
            
            checks[operation] = {
                'time_threshold_met': time_ok,
                'memory_threshold_met': memory_ok,
                'execution_successful': success_ok,
                'overall_pass': time_ok and memory_ok and success_ok
            }
        
        return checks


class CodeQualityChecker:
    """Code quality analysis and metrics"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.project_root = Path.cwd()
        self.python_files = list(self.project_root.glob("**/*.py"))
        self.exclude_patterns = [
            "__pycache__",
            ".git",
            "venv",
            "env",
            ".pytest_cache",
            "htmlcov",
            "test_*.py"
        ]
    
    def get_project_files(self) -> List[Path]:
        """Get all Python files in the project"""
        filtered_files = []
        for file_path in self.python_files:
            # Skip excluded patterns
            if any(pattern in str(file_path) for pattern in self.exclude_patterns):
                continue
            filtered_files.append(file_path)
        return filtered_files
    
    def analyze_file_complexity(self, file_path: Path) -> Dict[str, Any]:
        """Analyze complexity metrics for a Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Basic metrics
            total_lines = len(lines)
            code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
            comment_lines = len([line for line in lines if line.strip().startswith('#')])
            blank_lines = total_lines - code_lines - comment_lines
            
            # Function and class counts
            function_count = content.count('def ')
            class_count = content.count('class ')
            
            # Estimate complexity (simple heuristic)
            complexity_indicators = [
                'if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except:', 'with '
            ]
            estimated_complexity = sum(content.count(indicator) for indicator in complexity_indicators)
            
            return {
                'file_path': str(file_path),
                'total_lines': total_lines,
                'code_lines': code_lines,
                'comment_lines': comment_lines,
                'blank_lines': blank_lines,
                'function_count': function_count,
                'class_count': class_count,
                'estimated_complexity': estimated_complexity,
                'comment_ratio': comment_lines / max(code_lines, 1),
                'avg_complexity_per_function': estimated_complexity / max(function_count, 1)
            }
        
        except Exception as e:
            return {
                'file_path': str(file_path),
                'error': str(e),
                'analysis_failed': True
            }
    
    def generate_quality_report(self) -> Dict[str, Any]:
        """Generate comprehensive code quality report"""
        files = self.get_project_files()
        file_analyses = []
        
        total_lines = 0
        total_functions = 0
        total_classes = 0
        total_complexity = 0
        
        for file_path in files:
            analysis = self.analyze_file_complexity(file_path)
            if not analysis.get('analysis_failed'):
                file_analyses.append(analysis)
                total_lines += analysis.get('total_lines', 0)
                total_functions += analysis.get('function_count', 0)
                total_classes += analysis.get('class_count', 0)
                total_complexity += analysis.get('estimated_complexity', 0)
        
        # Calculate averages
        avg_lines_per_file = total_lines / max(len(file_analyses), 1)
        avg_complexity_per_file = total_complexity / max(len(file_analyses), 1)
        avg_functions_per_file = total_functions / max(len(file_analyses), 1)
        
        # Quality flags
        quality_issues = []
        
        for analysis in file_analyses:
            if analysis.get('total_lines', 0) > self.config.code_quality_standards['max_class_length']:
                quality_issues.append(f"File too long: {analysis['file_path']}")
            
            if analysis.get('comment_ratio', 0) < 0.1:
                quality_issues.append(f"Low comment ratio: {analysis['file_path']}")
            
            if analysis.get('avg_complexity_per_function', 0) > self.config.code_quality_standards['max_cognitive_complexity']:
                quality_issues.append(f"High complexity: {analysis['file_path']}")
        
        return {
            'summary': {
                'total_files': len(file_analyses),
                'total_lines': total_lines,
                'total_functions': total_functions,
                'total_classes': total_classes,
                'avg_lines_per_file': avg_lines_per_file,
                'avg_complexity_per_file': avg_complexity_per_file,
                'avg_functions_per_file': avg_functions_per_file
            },
            'file_analyses': file_analyses,
            'quality_issues': quality_issues,
            'quality_score': max(0, 100 - len(quality_issues) * 5)  # Simple scoring
        }


class TestRunner:
    """Main test runner for comprehensive testing"""
    
    def __init__(self, config: TestConfig = None):
        self.config = config or TestConfig()
        self.performance_tester = PerformanceTester(self.config)
        self.quality_checker = CodeQualityChecker(self.config)
        self.test_results = {}
    
    def run_unit_tests(self) -> Dict[str, Any]:
        """Run unit tests for core functionality"""
        results = {}
        
        # Test data generation
        try:
            test_data = TestDataGenerator.generate_sales_data(100)
            results['data_generation'] = {
                'success': True,
                'data_shape': test_data.shape,
                'columns': list(test_data.columns),
                'data_types': test_data.dtypes.to_dict()
            }
        except Exception as e:
            results['data_generation'] = {'success': False, 'error': str(e)}
        
        # Test data validation
        try:
            from car_sales_dashboard.utils.validation import DataValidator
            is_valid, errors = DataValidator.validate_dataframe(test_data, 'sales_data')
            results['data_validation'] = {
                'success': True,
                'is_valid': is_valid,
                'errors': errors
            }
        except Exception as e:
            results['data_validation'] = {'success': False, 'error': str(e)}
        
        # Test error handling
        try:
            from car_sales_dashboard.utils.error_handler import ErrorHandler, Validators
            
            # Test validators
            valid_result = Validators.positive_number(1.5)
            invalid_result = Validators.positive_number(-1.5)
            
            results['error_handling'] = {
                'success': True,
                'positive_validation': valid_result,
                'negative_validation': invalid_result
            }
        except Exception as e:
            results['error_handling'] = {'success': False, 'error': str(e)}
        
        return results
    
    def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance benchmarks"""
        try:
            benchmarks = self.performance_tester.benchmark_data_operations()
            threshold_checks = self.performance_tester.check_performance_thresholds(benchmarks)
            
            return {
                'success': True,
                'benchmarks': benchmarks,
                'threshold_checks': threshold_checks,
                'performance_summary': {
                    'total_operations': len(benchmarks),
                    'passed_thresholds': sum(1 for check in threshold_checks.values() if check['overall_pass']),
                    'avg_execution_time': np.mean([b['execution_time_ms'] for b in benchmarks.values()]),
                    'avg_memory_usage': np.mean([b['memory_usage_mb'] for b in benchmarks.values()])
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests for component interaction"""
        results = {}
        
        # Test chart creation workflow
        try:
            test_data = TestDataGenerator.generate_sales_data(500)
            
            # Test chart components import
            from car_sales_dashboard.components.charts import create_sales_trend_chart
            
            # Create forecast data
            forecast_data = TestDataGenerator.generate_forecast_data(test_data, 6)
            
            # Combine historical and forecast
            combined_data = pd.concat([
                test_data[['date', 'sales_volume']].rename(columns={'sales_volume': 'sales'}),
                forecast_data[['date', 'predicted_sales']].rename(columns={'predicted_sales': 'sales'})
            ]).reset_index(drop=True)
            
            # Test chart creation
            chart_dict = create_sales_trend_chart(combined_data)
            
            results['chart_workflow'] = {
                'success': True,
                'chart_keys': list(chart_dict.keys()),
                'data_points': len(combined_data)
            }
        except Exception as e:
            results['chart_workflow'] = {'success': False, 'error': str(e)}
        
        # Test caching system
        try:
            from car_sales_dashboard.utils.performance import MemoryCache, cached
            
            cache = MemoryCache()
            cache.set('test_key', 'test_value', ttl=60)
            retrieved = cache.get('test_key')
            
            results['caching_system'] = {
                'success': True,
                'cache_set_get': retrieved == 'test_value',
                'cache_stats': cache.get_stats()
            }
        except Exception as e:
            results['caching_system'] = {'success': False, 'error': str(e)}
        
        return results
    
    def run_code_quality_analysis(self) -> Dict[str, Any]:
        """Run code quality analysis"""
        try:
            quality_report = self.quality_checker.generate_quality_report()
            return {
                'success': True,
                'quality_report': quality_report
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites and generate comprehensive report"""
        print("🧪 Running comprehensive test suite...")
        print("=" * 60)
        
        # Run all test types
        self.test_results['unit_tests'] = self.run_unit_tests()
        self.test_results['performance_tests'] = self.run_performance_tests()
        self.test_results['integration_tests'] = self.run_integration_tests()
        self.test_results['code_quality'] = self.run_code_quality_analysis()
        
        # Generate summary
        summary = self.generate_test_summary()
        self.test_results['summary'] = summary
        
        return self.test_results
    
    def generate_test_summary(self) -> Dict[str, Any]:
        """Generate test execution summary"""
        total_tests = 0
        passed_tests = 0
        
        # Count test results
        for test_type, results in self.test_results.items():
            if test_type == 'summary':
                continue
                
            if isinstance(results, dict):
                for test_name, result in results.items():
                    total_tests += 1
                    if isinstance(result, dict) and result.get('success', False):
                        passed_tests += 1
        
        success_rate = (passed_tests / max(total_tests, 1)) * 100
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': success_rate,
            'overall_status': 'PASS' if success_rate >= 80 else 'FAIL',
            'timestamp': time.time(),
            'config': {
                'test_data_size': self.config.test_data_size,
                'performance_threshold_ms': self.config.performance_threshold_ms,
                'memory_threshold_mb': self.config.memory_threshold_mb
            }
        }


def generate_test_report(test_results: Dict[str, Any], output_file: str = "test_report.md") -> None:
    """Generate a markdown test report"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Car Sales Dashboard - Test Report\n\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Summary
        summary = test_results.get('summary', {})
        f.write("## Test Summary\n\n")
        f.write(f"- **Total Tests**: {summary.get('total_tests', 0)}\n")
        f.write(f"- **Passed**: {summary.get('passed_tests', 0)}\n")
        f.write(f"- **Failed**: {summary.get('failed_tests', 0)}\n")
        f.write(f"- **Success Rate**: {summary.get('success_rate', 0):.1f}%\n")
        f.write(f"- **Overall Status**: {summary.get('overall_status', 'UNKNOWN')}\n\n")
        
        # Detailed results
        for test_type, results in test_results.items():
            if test_type == 'summary':
                continue
                
            f.write(f"## {test_type.replace('_', ' ').title()}\n\n")
            
            if isinstance(results, dict):
                for test_name, result in results.items():
                    if isinstance(result, dict):
                        status = "PASS" if result.get('success', False) else "FAIL"
                    else:
                        status = "PASS" if result else "FAIL"
                    f.write(f"### {test_name.replace('_', ' ').title()}\n")
                    f.write(f"**Status**: {status}\n\n")
                    
                    if isinstance(result, dict):
                        if not result.get('success', False) and 'error' in result:
                            f.write(f"**Error**: `{result['error']}`\n\n")
                        
                        # Add specific details based on test type
                        if 'execution_time_ms' in result:
                            f.write(f"**Execution Time**: {result['execution_time_ms']:.2f}ms\n")
                        if 'memory_usage_mb' in result:
                            f.write(f"**Memory Usage**: {result['memory_usage_mb']:.2f}MB\n")
                    
                    f.write("\n")
        
        f.write("---\n")
        f.write("*Report generated by Car Sales Dashboard Testing Framework*\n")
    
    print(f"📊 Test report generated: {output_file}")


# CLI interface for running tests
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Car Sales Dashboard Test Runner")
    parser.add_argument("--test-type", choices=['unit', 'performance', 'integration', 'quality', 'all'], 
                       default='all', help="Type of tests to run")
    parser.add_argument("--data-size", type=int, default=1000, help="Size of test data")
    parser.add_argument("--output", default="test_report.md", help="Output report file")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Configure test runner
    config = TestConfig(test_data_size=args.data_size)
    runner = TestRunner(config)
    
    # Run specified tests
    if args.test_type == 'all':
        results = runner.run_all_tests()
    elif args.test_type == 'unit':
        results = {'unit_tests': runner.run_unit_tests()}
    elif args.test_type == 'performance':
        results = {'performance_tests': runner.run_performance_tests()}
    elif args.test_type == 'integration':
        results = {'integration_tests': runner.run_integration_tests()}
    elif args.test_type == 'quality':
        results = {'code_quality': runner.run_code_quality_analysis()}
    
    # Generate report
    if args.test_type == 'all':
        generate_test_report(results, args.output)
    
    # Print summary
    if 'summary' in results:
        summary = results['summary']
        print(f"\n🎯 Test Results: {summary['passed_tests']}/{summary['total_tests']} passed")
        print(f"📈 Success Rate: {summary['success_rate']:.1f}%")
        print(f"🏆 Overall Status: {summary['overall_status']}")
    else:
        print("\n✅ Test execution completed")
