# Small helper tool to detect current OS and set the environment 
import os
import sys
import platform

def base_path():
    os = platform.system()

    if os == 'Darwin':
        base_path = '/Users/carldraper/Documents'
    else:
        base_path = '/opt'
    return base_path