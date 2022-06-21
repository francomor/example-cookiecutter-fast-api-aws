import os
import sys

from runtime.src import initial_data

cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(f"{cwd}/../src"))

initial_data.main()
