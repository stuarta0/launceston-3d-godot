import os
import re
import shutil
from create_scenes import create, LOD_CUSTOM

USE_LOD = True

project = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
dataset = os.path.join(project, 'dataset')
lods = (15, 17, 20)

if not os.path.exists(dataset):
    print("Dataset doesn't exist, cloning repository...")
    os.system('git clone https://github.com/stuarta0/launceston-3d.git dataset')
else:
    print("Dataset exists.")

print("Creating scenes...")
create(LOD_CUSTOM if USE_LOD else None)