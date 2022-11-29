import os
import shutil
local_dev = "{{ cookiecutter.local_dev }}"
print(local_dev)
if not local_dev:

    os.remove('makefile')
    shutil.rmtree('docs/makefile')
