import os
import os.path as op
import sys
import re
import logging
import shutil as sh
import tqdm
import time

from tqdm import trange
from time import sleep


def main():

    pbar1 = tqdm.tqdm(
        total=100,
        position=0,
        colour="green",
        desc="First",
        ncols=80,
        mininterval=0.02,
        unit=" files",
    )
    pbar2 = tqdm.tqdm(
        total=100, position=1, colour="red", desc="Second", ncols=80, mininterval=0.02
    )
    pbar3 = tqdm.tqdm(
        total=100, position=2, colour="blue", desc="Third", ncols=80, mininterval=0.02
    )
    pbar4 = tqdm.tqdm(
        total=100, position=3, colour="cyan", desc="Fourth", ncols=80, mininterval=0.02
    )

    for i in range(100):

        for bar in [pbar1, pbar2, pbar3, pbar4]:
            bar.update(1)

        time.sleep(0.02)


if __name__ == "__main__":
    main()
