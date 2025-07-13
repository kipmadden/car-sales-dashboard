"""
Performance optimization and caching utilities for the Car Sales Dashboard.

This module provides caching strategies, performance monitoring, and optimization
techniques to improve dashboard responsiveness and user experience.
"""

import functools
import time
import hashlib
import pickle
from typing import Any, Dict, Optional, Callable, Union
import threading
from datetime import datetime, timedelta
import logging
import pandas as pd
from car_sales_dashboard.utils.logging_config import perf_logger

logger = logging.getLogger(__name__)


class MemoryCache:
    """
    Thread-safe in-memory cache with TTL (Time To Live) support.
    
    Optimizes repeated operations like chart generation and data processing.
    """
    
    def __init__(self, default_ttl: int = 300):  # 5 minutes default
        """
        Initialize the memory cache.
        
        Args:
            default_ttl: Default time-to-live in seconds
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self.default_ttl = default_ttl
        self._stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_size': 0
        }
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate a cache key from arguments."""
        # Create a deterministic key from arguments
        key_data = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_expired(self, entry: Dict[str, Any]) -> bool:
        """Check if a cache entry has expired."""
        return datetime.now() > entry['expires_at']
    
    def _cleanup_expired(self):
        """Remove expired entries from cache."""
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if self._is_expired(entry)
            ]
            
            for key in expired_keys:
                del self._cache[key]
                self._stats['evictions'] += 1
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if not self._is_expired(entry):
                    self._stats['hits'] += 1
                    logger.debug(f"Cache hit for key: {key[:20]}...")
                    return entry['value']
                else:
                    # Remove expired entry
                    del self._cache[key]
                    self._stats['evictions'] += 1
            
            self._stats['misses'] += 1
            logger.debug(f"Cache miss for key: {key[:20]}...")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set a value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        with self._lock:
            ttl = ttl or self.default_ttl
            expires_at = datetime.now() + timedelta(seconds=ttl)
            
            self._cache[key] = {
                'value': value,
                'expires_at': expires_at,
                'created_at': datetime.now()
            }
            
            self._stats['total_size'] = len(self._cache)
            logger.debug(f"Cached value for key: {key[:20]}... (TTL: {ttl}s)")
    
    def invalidate(self, pattern: Optional[str] = None) -> int:
        """
        Invalidate cache entries.
        
        Args:
            pattern: Optional pattern to match keys (None = clear all)
            
        Returns:
            Number of entries invalidated
        """
        with self._lock:
            if pattern is None:
                count = len(self._cache)
                self._cache.clear()
                self._stats['evictions'] += count
                logger.info("Cache completely cleared")
                return count
            
            # Pattern-based invalidation
            keys_to_remove = [
                key for key in self._cache.keys()
                if pattern in key
            ]
            
            for key in keys_to_remove:
                del self._cache[key]
                self._stats['evictions'] += 1
            
            logger.info(f"Invalidated {len(keys_to_remove)} cache entries matching '{pattern}'")
            return len(keys_to_remove)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_requests = self._stats['hits'] + self._stats['misses']
            hit_ratio = self._stats['hits'] / total_requests if total_requests > 0 else 0
            
            return {
                **self._stats,
                'hit_ratio': hit_ratio,
                'total_requests': total_requests
            }


# Global cache instance
_cache = MemoryCache(default_ttl=300)  # 5 minutes


def cached(ttl: int = 300, cache_instance: Optional[MemoryCache] = None):
    """
    Decorator to cache function results.
    
    Args:
        ttl: Time-to-live in seconds
        cache_instance: Optional cache instance (uses global if None)
        
    Usage:
        @cached(ttl=600)  # Cache for 10 minutes
        def expensive_operation(param1, param2):
            # expensive computation
            return result
    """
    def decorator(func: Callable) -> Callable:
        cache = cache_instance or _cache
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            key_data = f"{func.__name__}:{args}:{sorted(kwargs.items())}"
            cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                perf_logger.log_performance_metric("cache_hit", func.__name__, 0)
                return result
            
            # Execute function and cache result
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Cache the result
            cache.set(cache_key, result, ttl)
            
            perf_logger.log_performance_metric("cache_miss", func.__name__, execution_time)
            return result
        
        return wrapper
    return decorator


def performance_monitor(operation_name: str = None):
    """
    Decorator to monitor function performance.
    
    Args:
        operation_name: Name for the operation (uses function name if None)
        
    Usage:
        @performance_monitor("data_processing")
        def process_data():
            # processing logic
            pass
    """
    def decorator(func: Callable) -> Callable:
        op_name = operation_name or func.__name__
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = _get_memory_usage()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                memory_delta = _get_memory_usage() - start_memory
                
                # Log performance metrics
                perf_logger.log_performance_metric(op_name, "success", execution_time)
                
                logger.debug(
                    f"Performance [{op_name}]: {execution_time:.3f}s, "
                    f"Memory: {memory_delta:+.1f}MB"
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                perf_logger.log_performance_metric(op_name, "error", execution_time)
                logger.error(f"Performance [{op_name}]: Failed after {execution_time:.3f}s - {e}")
                raise
        
        return wrapper
    return decorator


def _get_memory_usage() -> float:
    """Get current memory usage in MB."""
    try:
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # Convert to MB
    except ImportError:
        return 0.0  # psutil not available


class DataFrameOptimizer:
    """
    Utilities for optimizing pandas DataFrame operations.
    """
    
    @staticmethod
    def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize DataFrame data types to reduce memory usage.
        
        Args:
            df: DataFrame to optimize
            
        Returns:
            Optimized DataFrame
        """
        optimized = df.copy()
        
        for col in optimized.columns:
            col_type = optimized[col].dtype
            
            if col_type == 'object':
                # Try to convert to category if low cardinality
                unique_ratio = len(optimized[col].unique()) / len(optimized[col])
                if unique_ratio < 0.5:  # Less than 50% unique values
                    optimized[col] = optimized[col].astype('category')
            
            elif col_type == 'int64':
                # Downcast integers
                min_val = optimized[col].min()
                max_val = optimized[col].max()
                
                if min_val >= 0:
                    if max_val < 255:
                        optimized[col] = optimized[col].astype('uint8')
                    elif max_val < 65535:
                        optimized[col] = optimized[col].astype('uint16')
                    elif max_val < 4294967295:
                        optimized[col] = optimized[col].astype('uint32')
                else:
                    if min_val > -128 and max_val < 127:
                        optimized[col] = optimized[col].astype('int8')
                    elif min_val > -32768 and max_val < 32767:
                        optimized[col] = optimized[col].astype('int16')
                    elif min_val > -2147483648 and max_val < 2147483647:
                        optimized[col] = optimized[col].astype('int32')
            
            elif col_type == 'float64':
                # Downcast floats
                optimized[col] = pd.to_numeric(optimized[col], downcast='float')
        
        original_size = df.memory_usage(deep=True).sum()
        optimized_size = optimized.memory_usage(deep=True).sum()
        reduction = (1 - optimized_size / original_size) * 100
        
        logger.info(f"DataFrame optimization: {reduction:.1f}% memory reduction")
        
        return optimized
    
    @staticmethod
    def efficient_groupby(
        df: pd.DataFrame, 
        group_cols: list, 
        agg_dict: dict,
        sort: bool = False
    ) -> pd.DataFrame:
        """
        Perform efficient groupby operations.
        
        Args:
            df: DataFrame to group
            group_cols: Columns to group by
            agg_dict: Aggregation dictionary
            sort: Whether to sort results
            
        Returns:
            Grouped DataFrame
        """
        # Use observed=True for categorical columns to improve performance
        kwargs = {'observed': True} if any(df[col].dtype.name == 'category' for col in group_cols) else {}
        
        result = df.groupby(group_cols, sort=sort, **kwargs).agg(agg_dict)
        
        return result


class QueryOptimizer:
    """
    Utilities for optimizing data queries and filtering operations.
    """
    
    @staticmethod
    def build_efficient_filter(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Build an efficient filter chain for DataFrame.
        
        Args:
            df: DataFrame to filter
            filters: Dictionary of column: value filters
            
        Returns:
            Filtered DataFrame
        """
        result = df
        
        # Apply filters in order of selectivity (most selective first)
        filter_selectivity = {}
        
        for col, values in filters.items():
            if col in df.columns and values:
                if isinstance(values, (list, tuple)):
                    selectivity = len(values) / df[col].nunique()
                    filter_selectivity[col] = selectivity
                else:
                    filter_selectivity[col] = 1.0 / df[col].nunique()
        
        # Sort by selectivity (most selective first)
        sorted_filters = sorted(filter_selectivity.items(), key=lambda x: x[1])
        
        for col, _ in sorted_filters:
            values = filters[col]
            if isinstance(values, (list, tuple)):
                result = result[result[col].isin(values)]
            else:
                result = result[result[col] == values]
        
        return result


# Global cache control functions
def get_cache_stats() -> Dict[str, Any]:
    """Get global cache statistics."""
    return _cache.get_stats()


def clear_cache(pattern: Optional[str] = None) -> int:
    """Clear cache entries."""
    return _cache.invalidate(pattern)


def get_cache_instance() -> MemoryCache:
    """Get the global cache instance."""
    return _cache
