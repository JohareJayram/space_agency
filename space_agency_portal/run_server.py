#!/usr/bin/env python
import os
import sys
import subprocess

# Set the project directory
project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

# Run the Django server
subprocess.run([sys.executable, 'manage.py', 'runserver'])