import hashlib
import logging
from re import M
import numpy as np
import os.path as op


def hash_slice(file, min_blocks: int) -> str:

    hash = hashlib.sha256()

    with open(file, "rb") as fp:
        n_blocks = op.getsize(file) / hash.block_size
        logging.debug(f"file has at least {n_blocks} blocks")

        if n_blocks > min_blocks:
            block_step = np.floor((n_blocks - min_blocks) / min_blocks).astype(np.int32)
        else:
            block_step = 0

        for nchunk in range(min_blocks):
            chunk = fp.read(hash.block_size)

            if not chunk:
                break

            hash.update(chunk)

            fp.seek(block_step * hash.block_size, 1)

    return hash.hexdigest()


def hash_full(file) -> str:

    hash = hashlib.sha256()

    with open(file, "rb") as fp:
        file_bytes = fp.read()

    hash.update(file_bytes)

    return hash.hexdigest()
