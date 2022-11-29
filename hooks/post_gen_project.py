import os
import shutil

local_development = bool("{{ cookiecutter.local_development }}")


if not local_development:
    print('hello')
    os.remove('makefile')
    shutil.rmtree('docs/makefile')
