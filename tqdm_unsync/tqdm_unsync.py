# -*- coding: utf-8 -*-
"""
This is how to use TQDM and Unsync together. This is for multiple threads.

TQDM will keep the main visable after it completes.
TQDM will remove the sub thread progress bars as they complete.
"""

import random
import time

from tqdm import tqdm
from unsync import unsync


@unsync
def go():
    
    delay: float = random.uniform(0.01, 0.2)
    loops: int = random.randint(1, 30)
    
    for _ in tqdm(range(loops), desc="stuff", ascii=True, leave=False):
        time.sleep(delay)
    
    return "hi"


def start():

    loops: int = random.randint(100, 1000)
    tasks = [go() for _ in tqdm(range(loops), ascii=False, leave=True)]
    results = [task.result() for task in tasks]


if __name__ == "__main__":
    start()
