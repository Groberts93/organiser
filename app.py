import os
import os.path as op
import sys
import re
import logging
import shutil as sh
import tqdm
import time

import file_sort


def main(args):

    # Input and counting files

    in_path = args[1]
    out_path = args[2]

    print(f"counting files in {in_path} and below...")
    files = [file for root, dirs, files in os.walk(in_path) for file in files]
    roots = [root for root, dirs, files in os.walk(in_path)]

    full_paths = [
        op.abspath(op.join(root, file))
        for root, _, files in os.walk(in_path)
        for file in files
    ]
    print(f"counted {len(full_paths)} files")

    # group files by size

    print(f"grouping files by size...")
    files_by_size = file_sort.group_files_by_size(full_paths)

    print("finding duplicates...")
    t_start = time.perf_counter()

    uniques = list()
    duplicates = list()

    for file_size, file_list in files_by_size.items():

        unique_files, duplicate_files = file_sort.get_uniques_simple(file_list)

        uniques.extend(unique_files)
        duplicates.extend(duplicate_files)

    t_stop = time.perf_counter()
    t_elapsed = t_stop - t_start

    print(f"duplicate sorting finished in {t_elapsed:.1f}")
    print(f"uniques: {len(uniques)} \nduplicates: {len(duplicates)}")
    print(
        f"total check: {len(files)} files in, {len(uniques) + len(duplicates)} files out"
    )

    uniques_extensions = file_sort.get_file_extensions(uniques)
    duplicates_extensions = file_sort.get_file_extensions(duplicates)

    ext_set_unique = file_sort.get_extension_set(uniques_extensions)
    ext_set_duplicate = file_sort.get_extension_set(duplicates_extensions)

    print("grouping files by extension...")
    uniques_by_extension = file_sort.group_files_by_ext(
        uniques, uniques_extensions, ext_set_unique
    )

    duplicates_by_extension = file_sort.group_files_by_ext(
        duplicates, duplicates_extensions, ext_set_duplicate
    )

    print("making output directories...")
    for path, ext_set in zip(
        ("unique", "duplicate"), [ext_set_unique, ext_set_duplicate]
    ):

        for ext in ext_set:
            try:
                os.makedirs(op.join(out_path, path, ext))
            except FileExistsError as err:
                logging.warn(err)

    files_by_extension = {
        "unique": uniques_by_extension,
        "duplicate": duplicates_by_extension,
    }

    files_copied = {"unique": 0, "duplicate": 0}
    files_failed = {"unique": 0, "duplicate": 0}
    total_files = {"unique": len(uniques), "duplicate": len(duplicates)}

    print(f"copying {total_files['unique']} and {total_files['duplicate']}")

    for path, ext_set in zip(
        ("unique", "duplicate"), [ext_set_unique, ext_set_duplicate]
    ):

        for ext in ext_set:
            for file in files_by_extension[path][ext]:
                try:
                    sh.copyfile(file, op.join(out_path, path, ext, op.basename(file)))
                    files_copied[path] = files_copied[path] + 1
                except (FileExistsError, FileNotFoundError) as err:
                    logging.warn(err)
                    files_failed[path] = files_failed[path] + 1

        print(
            f"of {total_files[path]} {path} files, {files_copied[path]} copied successfully and {files_failed[path]} failed"
        )

        print(f"view output at {out_path}")


if __name__ == "__main__":
    main(sys.argv)
