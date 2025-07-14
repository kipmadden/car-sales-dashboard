"""
Performance and Load Testing Module

Comprehensive performance testing and benchmarking utilities
for the Car Sales Dashboard application.
"""

import time
import psutil
import threading
import multiprocessing
import concurrent.futures
import memory_profiler
import tracemalloc
import gc
from typing import Dict, List, Any, Callable, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import statistics
import json
import sys
import os
from pathlib import Path


@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    execution_time: float
    memory_usage: float
    cpu_usage: float
    memory_peak: float
    function_calls: int
    cache_hits: int = 0
    cache_misses: int = 0
    success: bool = True
    error_message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class LoadTestConfig:
    """Load testing configuration"""
    concurrent_users: int = 10
    duration_seconds: int = 60
    ramp_up_seconds: int = 10
    target_requests_per_second: float = 5.0
    max_response_time_ms: float = 1000.0
    error_threshold_percent: float = 5.0


class PerformanceProfiler:
    """Advanced performance profiling utilities"""
    
    def __init__(self):
        self.active_profiles = {}
        self.results = []
    
    def start_profile(self, profile_id: str) -> None:
        """Start a performance profile session"""
        tracemalloc.start()
        
        self.active_profiles[profile_id] = {
            'start_time': time.perf_counter(),
            'start_memory': psutil.Process().memory_info().rss,
            'start_cpu_times': psutil.Process().cpu_times(),
            'tracemalloc_snapshot': tracemalloc.take_snapshot()
        }
    
    def end_profile(self, profile_id: str) -> PerformanceMetrics:
        """End a performance profile session and return metrics"""
        if profile_id not in self.active_profiles:
            raise ValueError(f"Profile {profile_id} not found")
        
        profile_data = self.active_profiles[profile_id]
        
        # Calculate execution time
        execution_time = time.perf_counter() - profile_data['start_time']
        
        # Calculate memory usage
        current_memory = psutil.Process().memory_info().rss
        memory_usage = (current_memory - profile_data['start_memory']) / 1024 / 1024  # MB
        
        # Calculate CPU usage
        current_cpu_times = psutil.Process().cpu_times()
        cpu_usage = (
            (current_cpu_times.user - profile_data['start_cpu_times'].user) +
            (current_cpu_times.system - profile_data['start_cpu_times'].system)
        )
        
        # Get memory peak from tracemalloc
        current_snapshot = tracemalloc.take_snapshot()
        memory_peak = current_snapshot.peak_traced / 1024 / 1024  # MB
        
        # Stop tracemalloc
        tracemalloc.stop()
        
        # Clean up
        del self.active_profiles[profile_id]
        
        metrics = PerformanceMetrics(
            execution_time=execution_time,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            memory_peak=memory_peak,
            function_calls=1  # Simplified for now
        )
        
        self.results.append(metrics)
        return metrics
    
    def profile_function(self, func: Callable, *args, **kwargs) -> Tuple[Any, PerformanceMetrics]:
        """Profile a single function execution"""
        profile_id = f"func_{func.__name__}_{time.time()}"
        
        self.start_profile(profile_id)
        
        try:
            result = func(*args, **kwargs)
            success = True
            error_message = None
        except Exception as e:
            result = None
            success = False
            error_message = str(e)
        
        metrics = self.end_profile(profile_id)
        metrics.success = success
        metrics.error_message = error_message
        
        return result, metrics


class LoadTestRunner:
    """Load testing framework for dashboard endpoints"""
    
    def __init__(self, config: LoadTestConfig):
        self.config = config
        self.results = []
        self.active_tests = []
        self.stop_event = threading.Event()
    
    def simulate_user_session(self, user_id: int, target_function: Callable) -> List[PerformanceMetrics]:
        """Simulate a single user session"""
        session_results = []
        session_start = time.time()
        request_interval = 1.0 / self.config.target_requests_per_second
        
        profiler = PerformanceProfiler()
        
        while (time.time() - session_start) < self.config.duration_seconds:
            if self.stop_event.is_set():
                break
            
            request_start = time.time()
            
            try:
                # Execute target function with profiling
                result, metrics = profiler.profile_function(target_function)
                metrics.timestamp = datetime.now()
                session_results.append(metrics)
                
            except Exception as e:
                # Record failed request
                failed_metrics = PerformanceMetrics(
                    execution_time=time.time() - request_start,
                    memory_usage=0,
                    cpu_usage=0,
                    memory_peak=0,
                    function_calls=1,
                    success=False,
                    error_message=str(e)
                )
                session_results.append(failed_metrics)
            
            # Wait for next request
            elapsed = time.time() - request_start
            sleep_time = max(0, request_interval - elapsed)
            time.sleep(sleep_time)
        
        return session_results
    
    def run_load_test(self, target_function: Callable) -> Dict[str, Any]:
        """Run a comprehensive load test"""
        print(f"🚀 Starting load test with {self.config.concurrent_users} users...")
        print(f"📊 Duration: {self.config.duration_seconds}s, Target RPS: {self.config.target_requests_per_second}")
        
        all_results = []
        test_start_time = time.time()
        
        # Use ThreadPoolExecutor for concurrent users
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.concurrent_users) as executor:
            # Submit user sessions
            futures = []
            for user_id in range(self.config.concurrent_users):
                # Stagger user starts during ramp-up period
                delay = (user_id / self.config.concurrent_users) * self.config.ramp_up_seconds
                
                future = executor.submit(self._delayed_user_session, user_id, target_function, delay)
                futures.append(future)
            
            # Collect results
            for future in concurrent.futures.as_completed(futures):
                try:
                    user_results = future.result()
                    all_results.extend(user_results)
                except Exception as e:
                    print(f"❌ User session failed: {e}")
        
        test_duration = time.time() - test_start_time
        
        # Analyze results
        analysis = self._analyze_load_test_results(all_results, test_duration)
        
        print(f"✅ Load test completed in {test_duration:.2f}s")
        print(f"📈 Total requests: {analysis['total_requests']}")
        print(f"🎯 Success rate: {analysis['success_rate']:.2f}%")
        print(f"⚡ Avg response time: {analysis['avg_response_time']:.2f}ms")
        
        return analysis
    
    def _delayed_user_session(self, user_id: int, target_function: Callable, delay: float) -> List[PerformanceMetrics]:
        """Start a user session with initial delay"""
        time.sleep(delay)
        return self.simulate_user_session(user_id, target_function)
    
    def _analyze_load_test_results(self, results: List[PerformanceMetrics], test_duration: float) -> Dict[str, Any]:
        """Analyze load test results and generate report"""
        if not results:
            return {'error': 'No results to analyze'}
        
        # Basic metrics
        total_requests = len(results)
        successful_requests = sum(1 for r in results if r.success)
        failed_requests = total_requests - successful_requests
        success_rate = (successful_requests / total_requests) * 100
        
        # Response time metrics (convert to milliseconds)
        response_times = [r.execution_time * 1000 for r in results if r.success]
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            median_response_time = statistics.median(response_times)
            p95_response_time = np.percentile(response_times, 95)
            p99_response_time = np.percentile(response_times, 99)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
        else:
            avg_response_time = median_response_time = p95_response_time = p99_response_time = 0
            min_response_time = max_response_time = 0
        
        # Throughput metrics
        actual_rps = total_requests / test_duration
        successful_rps = successful_requests / test_duration
        
        # Memory metrics
        memory_usage = [r.memory_usage for r in results if r.success and r.memory_usage > 0]
        avg_memory_usage = statistics.mean(memory_usage) if memory_usage else 0
        peak_memory_usage = max(memory_usage) if memory_usage else 0
        
        # Performance thresholds check
        threshold_violations = sum(
            1 for rt in response_times 
            if rt > self.config.max_response_time_ms
        )
        threshold_violation_rate = (threshold_violations / len(response_times)) * 100 if response_times else 0
        
        # Error analysis
        error_types = {}
        for result in results:
            if not result.success and result.error_message:
                error_type = type(Exception(result.error_message)).__name__
                error_types[error_type] = error_types.get(error_type, 0) + 1
        
        # Overall assessment
        load_test_passed = (
            success_rate >= (100 - self.config.error_threshold_percent) and
            avg_response_time <= self.config.max_response_time_ms and
            threshold_violation_rate <= self.config.error_threshold_percent
        )
        
        return {
            'test_config': {
                'concurrent_users': self.config.concurrent_users,
                'duration_seconds': self.config.duration_seconds,
                'target_rps': self.config.target_requests_per_second,
                'max_response_time_ms': self.config.max_response_time_ms
            },
            'summary': {
                'total_requests': total_requests,
                'successful_requests': successful_requests,
                'failed_requests': failed_requests,
                'success_rate': success_rate,
                'test_duration': test_duration,
                'load_test_passed': load_test_passed
            },
            'response_times': {
                'avg_response_time': avg_response_time,
                'median_response_time': median_response_time,
                'p95_response_time': p95_response_time,
                'p99_response_time': p99_response_time,
                'min_response_time': min_response_time,
                'max_response_time': max_response_time,
                'threshold_violations': threshold_violations,
                'threshold_violation_rate': threshold_violation_rate
            },
            'throughput': {
                'actual_rps': actual_rps,
                'successful_rps': successful_rps,
                'target_rps': self.config.target_requests_per_second
            },
            'memory': {
                'avg_memory_usage_mb': avg_memory_usage,
                'peak_memory_usage_mb': peak_memory_usage
            },
            'errors': {
                'error_types': error_types,
                'error_rate': (failed_requests / total_requests) * 100
            },
            'raw_results': results
        }


class BenchmarkSuite:
    """Comprehensive benchmarking suite for dashboard components"""
    
    def __init__(self):
        self.profiler = PerformanceProfiler()
        self.benchmarks = {}
    
    def benchmark_data_operations(self) -> Dict[str, Any]:
        """Benchmark data-related operations"""
        from car_sales_dashboard.utils.testing_framework import TestDataGenerator
        
        benchmarks = {}
        
        # Data generation benchmarks
        for size in [100, 1000, 10000]:
            def generate_data():
                return TestDataGenerator.generate_sales_data(size)
            
            result, metrics = self.profiler.profile_function(generate_data)
            benchmarks[f'data_generation_{size}'] = {
                'execution_time_ms': metrics.execution_time * 1000,
                'memory_usage_mb': metrics.memory_usage,
                'data_size': size,
                'success': metrics.success
            }
        
        # Data processing benchmarks
        test_data = TestDataGenerator.generate_sales_data(5000)
        
        # Filtering
        def filter_data():
            return test_data[test_data['sales_volume'] > test_data['sales_volume'].median()]
        
        result, metrics = self.profiler.profile_function(filter_data)
        benchmarks['data_filtering'] = {
            'execution_time_ms': metrics.execution_time * 1000,
            'memory_usage_mb': metrics.memory_usage,
            'success': metrics.success
        }
        
        # Aggregation
        def aggregate_data():
            return test_data.groupby(['vehicle_type', 'region']).agg({
                'sales_volume': ['sum', 'mean', 'count'],
                'gas_price': 'mean'
            })
        
        result, metrics = self.profiler.profile_function(aggregate_data)
        benchmarks['data_aggregation'] = {
            'execution_time_ms': metrics.execution_time * 1000,
            'memory_usage_mb': metrics.memory_usage,
            'success': metrics.success
        }
        
        # Sorting
        def sort_data():
            return test_data.sort_values(['date', 'sales_volume'], ascending=[True, False])
        
        result, metrics = self.profiler.profile_function(sort_data)
        benchmarks['data_sorting'] = {
            'execution_time_ms': metrics.execution_time * 1000,
            'memory_usage_mb': metrics.memory_usage,
            'success': metrics.success
        }
        
        return benchmarks
    
    def benchmark_chart_operations(self) -> Dict[str, Any]:
        """Benchmark chart creation operations"""
        from car_sales_dashboard.components.charts import create_sales_trend_chart
        from car_sales_dashboard.utils.testing_framework import TestDataGenerator
        
        benchmarks = {}
        
        # Chart creation with different data sizes
        for size in [100, 1000, 5000]:
            test_data = TestDataGenerator.generate_sales_data(size)
            
            def create_chart():
                return create_sales_trend_chart(test_data)
            
            result, metrics = self.profiler.profile_function(create_chart)
            benchmarks[f'chart_creation_{size}'] = {
                'execution_time_ms': metrics.execution_time * 1000,
                'memory_usage_mb': metrics.memory_usage,
                'data_size': size,
                'success': metrics.success
            }
        
        return benchmarks
    
    def benchmark_validation_operations(self) -> Dict[str, Any]:
        """Benchmark validation operations"""
        from car_sales_dashboard.utils.validation import DataValidator, InputSanitizer
        from car_sales_dashboard.utils.testing_framework import TestDataGenerator
        
        benchmarks = {}
        
        # Data validation benchmarks
        for size in [100, 1000, 5000]:
            test_data = TestDataGenerator.generate_sales_data(size)
            
            def validate_data():
                return DataValidator.validate_dataframe(test_data, 'sales_data')
            
            result, metrics = self.profiler.profile_function(validate_data)
            benchmarks[f'data_validation_{size}'] = {
                'execution_time_ms': metrics.execution_time * 1000,
                'memory_usage_mb': metrics.memory_usage,
                'data_size': size,
                'success': metrics.success
            }
        
        # Input sanitization benchmarks
        test_strings = ["test string"] * 1000
        
        def sanitize_strings():
            return [InputSanitizer.sanitize_string(s) for s in test_strings]
        
        result, metrics = self.profiler.profile_function(sanitize_strings)
        benchmarks['input_sanitization'] = {
            'execution_time_ms': metrics.execution_time * 1000,
            'memory_usage_mb': metrics.memory_usage,
            'input_count': len(test_strings),
            'success': metrics.success
        }
        
        return benchmarks
    
    def run_full_benchmark_suite(self) -> Dict[str, Any]:
        """Run complete benchmark suite"""
        print("🏃‍♂️ Running comprehensive benchmark suite...")
        
        suite_start = time.time()
        
        # Run individual benchmark categories
        data_benchmarks = self.benchmark_data_operations()
        chart_benchmarks = self.benchmark_chart_operations()
        validation_benchmarks = self.benchmark_validation_operations()
        
        suite_duration = time.time() - suite_start
        
        # Combine results
        all_benchmarks = {
            'data_operations': data_benchmarks,
            'chart_operations': chart_benchmarks,
            'validation_operations': validation_benchmarks
        }
        
        # Calculate summary statistics
        all_times = []
        all_memory = []
        all_success = []
        
        for category, benchmarks in all_benchmarks.items():
            for benchmark_name, results in benchmarks.items():
                if results.get('success', False):
                    all_times.append(results.get('execution_time_ms', 0))
                    all_memory.append(results.get('memory_usage_mb', 0))
                    all_success.append(results.get('success', False))
        
        summary = {
            'total_benchmarks': len(all_times),
            'success_rate': (sum(all_success) / len(all_success)) * 100 if all_success else 0,
            'avg_execution_time_ms': statistics.mean(all_times) if all_times else 0,
            'max_execution_time_ms': max(all_times) if all_times else 0,
            'avg_memory_usage_mb': statistics.mean(all_memory) if all_memory else 0,
            'max_memory_usage_mb': max(all_memory) if all_memory else 0,
            'suite_duration_seconds': suite_duration
        }
        
        print(f"✅ Benchmark suite completed in {suite_duration:.2f}s")
        print(f"📊 Total benchmarks: {summary['total_benchmarks']}")
        print(f"🎯 Success rate: {summary['success_rate']:.2f}%")
        print(f"⚡ Avg execution time: {summary['avg_execution_time_ms']:.2f}ms")
        
        return {
            'summary': summary,
            'benchmarks': all_benchmarks,
            'timestamp': datetime.now().isoformat()
        }


def generate_performance_report(results: Dict[str, Any], output_file: str = "performance_report.json") -> None:
    """Generate detailed performance report"""
    
    # Convert datetime objects to strings for JSON serialization
    def serialize_results(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, PerformanceMetrics):
            return {
                'execution_time': obj.execution_time,
                'memory_usage': obj.memory_usage,
                'cpu_usage': obj.cpu_usage,
                'memory_peak': obj.memory_peak,
                'function_calls': obj.function_calls,
                'success': obj.success,
                'error_message': obj.error_message,
                'timestamp': obj.timestamp.isoformat()
            }
        return obj
    
    # Serialize results
    serializable_results = json.loads(
        json.dumps(results, default=serialize_results)
    )
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=2)
    
    print(f"📋 Performance report saved to: {output_file}")


# Example usage and testing functions
def example_target_function():
    """Example function for load testing"""
    from car_sales_dashboard.utils.testing_framework import TestDataGenerator
    
    # Simulate dashboard data loading and chart creation
    data = TestDataGenerator.generate_sales_data(1000)
    
    # Simulate some processing
    processed = data.groupby('vehicle_type')['sales_volume'].sum()
    
    # Simulate chart creation
    chart_data = {
        'data': processed.to_dict(),
        'layout': {'title': 'Sales by Vehicle Type'}
    }
    
    return chart_data


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Performance Testing Suite")
    parser.add_argument("--test-type", choices=['benchmark', 'load', 'profile'], 
                       default='benchmark', help="Type of performance test to run")
    parser.add_argument("--users", type=int, default=10, help="Number of concurrent users for load test")
    parser.add_argument("--duration", type=int, default=60, help="Test duration in seconds")
    parser.add_argument("--output", default="performance_results.json", help="Output file for results")
    
    args = parser.parse_args()
    
    if args.test_type == 'benchmark':
        # Run benchmark suite
        suite = BenchmarkSuite()
        results = suite.run_full_benchmark_suite()
        generate_performance_report(results, args.output)
        
    elif args.test_type == 'load':
        # Run load test
        config = LoadTestConfig(
            concurrent_users=args.users,
            duration_seconds=args.duration
        )
        runner = LoadTestRunner(config)
        results = runner.run_load_test(example_target_function)
        generate_performance_report(results, args.output)
        
    elif args.test_type == 'profile':
        # Run profiling
        profiler = PerformanceProfiler()
        result, metrics = profiler.profile_function(example_target_function)
        
        profile_results = {
            'function_name': 'example_target_function',
            'metrics': metrics,
            'result_sample': str(result)[:200] if result else None
        }
        generate_performance_report(profile_results, args.output)
