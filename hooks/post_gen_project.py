import os
import shutil

local_development = bool("{{ cookiecutter.local_development }}")


if not local_development:
    os.remove('makefile')
    os.removedirs('docs/makefile')
