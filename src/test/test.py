#!/usr/bin/env python

import unittest
import pdb
import os, sys

def main():
    for i in range(100):
        pdb.set_trace()
        print "I is", i

__name__ == "__main__":
    main()
    
