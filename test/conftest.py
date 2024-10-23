import os
import sys

# Add the src directory to the sys.path in order to be able to import the modules
__this_dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(__this_dir__, "..", "src"))
