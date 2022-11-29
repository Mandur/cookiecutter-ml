import os
import shutil

local_development = bool("{{ cookiecutter.local_development }}")


if not local_development:
    print('hello')
    shutil.rmtree('docs/makefile')
