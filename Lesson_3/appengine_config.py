import sys
import os

# point appengine to third-party python libraries in the project
sys.path.insert(2, os.path.join(os.path.abspath('.'), 'lib'))
