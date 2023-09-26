import os
from typing import List

current_working_directory = os.getcwd()


def get_absolute_path(path: List[str]) -> str:
    target_path = os.path.join(*path)
    return os.path.join(current_working_directory, target_path)