#!/usr/bin/env python

import os, sys
import sqlite3

from log import get_logger
logger = get_logger(__name__)

# enum Priority
class Priority:
    NONE = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class CacheItem(object):
    """
    Convenience holder for a single entry in the Priority Cache
    """

    def __init__(self):
        self.id = 0
        self.date = None
        self.title = ""
        self.url = ""
        self.text_blob = ""
        self.priority = Priority.NONE

class PriorityCache(object):
    """
    A simple priority cache implementation. Objects may be inserted in any
    order, but are retrieved as an ordered list.
    """

    def __init__(self):
        """
        Constructor
        """
        self.items = {}
        pass

    def insert(self, item):
        """
        Inserts a given CacheItem
        """
        logger.debug("Inserting into Cache: " + str(item))

    def get(self):
        return self.items


