import json
from datetime import datetime
from logger.logger import logger

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

# defining the cache class
'''
LRU cache is a cache removal algorithm where the least recently used items in a cache are removed to allocate space for new additions
Implementation : LRU supports the Fast item lookup, constant time (o(1)) insertion and deletion,Ordered storage.
HashMap - hold the keys and address of the Nodes of Doubly LinkedList.Doubly LinkedList will hold the values of keys.

'''

# Exception class for cache
class ArgumentsError(Exception):
    def __init__(self, message):
        self.message = message

class Node:
    """
    Doubly linked list node for storing cached items.
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
        
class LRUCache:
    """
    LRU cache implementation using a doubly linked list and a hashmap.
    """
    def __init__(self, capacity, cache_file):
        if capacity <= 0:
            raise ArgumentsError("Capacity must be a positive integer")
        self.capacity = capacity
        self.size = 0
        self.head = None
        self.tail = None
        self.cache = {}
        self.cache_file = cache_file
        
        # Load cache from disk if file exists
        try:
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
                for key, value in cache_data.items():
                    node = Node(key, value)
                    self.cache[key] = node
                    self._add_to_front(node)
                    self.size += 1
            logger.info("Cache loaded from disk.")          
        except FileNotFoundError:
            logger.info("Cache file not found on disk.")
            pass

    def _save_to_disk(self):
        # Save the cache to disk using JSON serialization
        cache_data = {}
        for key, node in self.cache.items():
            cache_data[key] = node.value
        with open(self.cache_file, 'w') as f:
            logger.info("Cache saved to disk.")
            json.dump(cache_data, f, cls = DateTimeEncoder)
        
    def get(self, key):
        # Check if the key is in the cache
        if key in self.cache:
            # Move the node to the front of the list
            node = self.cache[key]
            self._move_to_front(node)
            return node.value
        else:
            return None
        
    def put(self, key, value):
        # Check if the key is already in the cache
        if key in self.cache:
            # Update the value and move the node to the front of the list
            node = self.cache[key]
            node.value = value
            self._move_to_front(node)
        else:
            # Create a new node and add it to the front of the list
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_front(node)
            self.size += 1
            
            # If the cache is over capacity, remove the least recently used node
            if self.size > self.capacity:
                removed_node = self._remove_last()
                del self.cache[removed_node.key]
                self.size -= 1

            # Save the cache to disk every 5 new inserts
            if self.size % 5 == 0:
                self._save_to_disk()

    def display_cache(self):
        cache = []
        for key, node in self.cache.items():
            cache.append((key, node.value))
        return cache

    def _add_to_front(self, node):
        # Add a node to the front of the list
        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        
    def _remove_last(self):
        # Remove the last node from the list and return it
        node = self.tail
        if self.tail.prev:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            self.head = None
            self.tail = None
        return node
        
    def _move_to_front(self, node):
        # Move a node to the front of the list
        if node == self.head:
            return
        elif node == self.tail:
            self.tail = node.prev
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        node.next = self.head
        node.prev = None
        self.head.prev = node
        self.head = node
