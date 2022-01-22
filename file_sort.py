# %%
import os.path as op
import re
import logging
import hashlib
import numpy as np
import logging
import file_hash
import tqdm


def group_files_by_ext(files, extensions, ext_set):
    files_by_extension = {ext: list() for ext in ext_set}

    for file, ext in zip(files, extensions):
        files_by_extension[ext].append(file)

    return files_by_extension


def get_extension_set(extensions):

    return set(extensions)


def get_file_extensions(files):

    ext_func = lambda x: re.compile("\.[a-z]+").findall(x)[-1][1:]
    extensions = list(map(ext_func, files))

    return extensions


def group_files_by_size(files):

    filesizes = [op.getsize(file) for file in files]
    filesizes_set = set(filesizes)
    files_by_size = {filesize: list() for filesize in filesizes_set}

    for full_file, filesize in zip(files, filesizes):
        files_by_size[filesize].append(full_file)

    return files_by_size


def get_uniques_simple(files: list[str]) -> tuple[list[str], list[str]]:

    """Given a list of file paths, determine which files are unique
    and which are duplicates of each other.

    Parameters
    ----------
    files : list[str]
        List of files to check.

    Returns
    -------
    uniques: list[str]
        List of unique files
    dupe_files: list[str]
        List of duplicate files.  If any file in "uniques" has duplicates,
        this list should contain them.
    """

    unique_files = list()
    dupe_files = list()
    digests = list()

    for file in files:
        digests.append(file_hash.hash_full(file))

    digest_set = set(digests)
    hash_to_file = dict()

    for digest_unique in digest_set:
        hash_to_file[digest_unique] = list()

    for digest, file in zip(digests, files):
        hash_to_file[digest].append(file)

    for file_list in hash_to_file.values():
        unique_files.append(file_list[0])

        if len(file_list) > 1:
            dupe_files.extend([file for file in file_list[1:]])

    return unique_files, dupe_files
