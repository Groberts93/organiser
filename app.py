# %%

import os
import os.path as op
import sys
import re
import logging
import shutil as sh

# %%
in_path = "/mnt/c/Users/gawr/Downloads"
out_path = "/home/grobs/orgtest/"

files = [file for root, dirs, files in os.walk(in_path) for file in files]
roots = [root for root, dirs, files in os.walk(in_path)]

if not op.isdir(out_path):
    os.makedirs(out_path)

# %%
full_paths = [
    op.join(root, file) for root, _, files in os.walk(in_path) for file in files
]

# %%

ext_func = lambda x: re.compile("\.[a-z]+").findall(x)[-1][1:]
extensions = list(map(ext_func, full_paths))

# %%

extension_set = set(extensions)
extension_paths = {extension: op.join(out_path, extension) for extension in extension_set}

for extension_path in extension_paths.values():
    try:
        os.mkdir(extension_path)
    except FileExistsError as err:
        logging.warning(err)


# %%

for file, full_path, extension in zip(files, full_paths, extensions):
    sh.copyfile(full_path, op.join(extension_paths[extension], file))
    
# %%
