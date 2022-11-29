import os
import shutil
local_dev = "{{ cookiecutter.local_dev }}"

if local_dev == "False":

    os.remove('makefile')
    shutil.rmtree('docs/makefile')
