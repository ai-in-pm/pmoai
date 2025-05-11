import hashlib
import json
import logging
import os
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from pmoai.tools.base_tool import BaseTool
from pmoai.utilities.paths import cache_storage_path

logger = logging.getLogger(__name__)


class CacheTools:
    """
    A class for caching tool results to avoid redundant API calls.
    """

    def __init__(
        self,
        cache_dir: Optional[str] = None,
        ttl: Optional[int] = None,
        enabled: bool = True,
    ):
        """
        Initialize the cache tools.

        Args:
            cache_dir: Directory to store cache files
            ttl: Time-to-live for cache entries in seconds
            enabled: Whether caching is enabled
        """
        self.cache_dir = cache_dir or os.path.join(cache_storage_path(), "tools_cache")
        self.ttl = ttl  # Time-to-live in seconds
        self.enabled = enabled
        
        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)
        
        logger.debug(f"Initialized tool cache at {self.cache_dir}")

    def wrap_tools(self, tools: List[BaseTool]) -> List[BaseTool]:
        """
        Wrap tools with caching functionality.

        Args:
            tools: List of tools to wrap

        Returns:
            List of wrapped tools
        """
        if not self.enabled:
            return tools
            
        wrapped_tools = []
        for tool in tools:
            # Skip tools that have custom cache functions
            if hasattr(tool, "cache_function") and tool.cache_function != BaseTool.cache_function:
                wrapped_tools.append(tool)
                continue
                
            # Create a wrapped version of the tool
            wrapped_tool = self._wrap_tool(tool)
            wrapped_tools.append(wrapped_tool)
            
        return wrapped_tools
        
    def _wrap_tool(self, tool: BaseTool) -> BaseTool:
        """
        Wrap a single tool with caching functionality.

        Args:
            tool: Tool to wrap

        Returns:
            Wrapped tool
        """
        original_run = tool._run
        cache_dir = self.cache_dir
        ttl = self.ttl
        
        def wrapped_run(*args: Any, **kwargs: Any) -> Any:
            # Generate a cache key based on tool name and arguments
            cache_key = self._generate_cache_key(tool.name, args, kwargs)
            cache_file = os.path.join(cache_dir, f"{cache_key}.pkl")
            
            # Check if we have a valid cache entry
            cached_result = self._get_cached_result(cache_file, ttl)
            if cached_result is not None:
                logger.debug(f"Cache hit for tool {tool.name}")
                return cached_result
                
            # Execute the original tool
            result = original_run(*args, **kwargs)
            
            # Cache the result
            self._cache_result(cache_file, result)
            
            return result
            
        # Replace the _run method with our wrapped version
        tool._run = wrapped_run
        
        return tool
        
    def _generate_cache_key(
        self, tool_name: str, args: Tuple[Any, ...], kwargs: Dict[str, Any]
    ) -> str:
        """
        Generate a cache key based on tool name and arguments.

        Args:
            tool_name: Name of the tool
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Cache key string
        """
        # Create a dictionary of all arguments
        all_args = {
            "tool_name": tool_name,
            "args": args,
            "kwargs": kwargs,
        }
        
        # Convert to a stable string representation
        try:
            args_str = json.dumps(all_args, sort_keys=True)
        except (TypeError, ValueError):
            # If JSON serialization fails, use a simpler approach
            args_str = str(all_args)
            
        # Create a hash of the arguments
        return hashlib.md5(args_str.encode()).hexdigest()
        
    def _get_cached_result(
        self, cache_file: str, ttl: Optional[int]
    ) -> Optional[Any]:
        """
        Get a cached result if it exists and is valid.

        Args:
            cache_file: Path to the cache file
            ttl: Time-to-live in seconds

        Returns:
            Cached result or None if not found or expired
        """
        if not os.path.exists(cache_file):
            return None
            
        # Check if the cache entry has expired
        if ttl is not None:
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if datetime.now() - file_mtime > timedelta(seconds=ttl):
                logger.debug(f"Cache entry expired: {cache_file}")
                return None
                
        # Load the cached result
        try:
            with open(cache_file, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            logger.warning(f"Error loading cache file {cache_file}: {e}")
            return None
            
    def _cache_result(self, cache_file: str, result: Any) -> None:
        """
        Cache a tool result.

        Args:
            cache_file: Path to the cache file
            result: Result to cache
        """
        try:
            with open(cache_file, "wb") as f:
                pickle.dump(result, f)
        except Exception as e:
            logger.warning(f"Error caching result to {cache_file}: {e}")
            
    def clear_cache(self, tool_name: Optional[str] = None) -> int:
        """
        Clear the cache for a specific tool or all tools.

        Args:
            tool_name: Name of the tool to clear cache for, or None for all tools

        Returns:
            Number of cache entries cleared
        """
        count = 0
        for cache_file in Path(self.cache_dir).glob("*.pkl"):
            if tool_name is None or tool_name in cache_file.stem:
                try:
                    os.remove(cache_file)
                    count += 1
                except Exception as e:
                    logger.warning(f"Error removing cache file {cache_file}: {e}")
                    
        return count
