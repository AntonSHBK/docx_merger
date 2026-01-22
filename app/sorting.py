import random
import re
from pathlib import Path
from typing import List


def get_docx_files(directory: Path) -> List[Path]:
    return list(directory.glob("*.docx"))


def sort_by_name(files: List[Path], reverse: bool = False) -> List[Path]:
    return sorted(files, key=lambda f: f.name, reverse=reverse)


def sort_by_creation_date(files: List[Path], reverse: bool = False) -> List[Path]:
    return sorted(files, key=lambda f: f.stat().st_ctime, reverse=reverse)


def sort_random(files: List[Path]) -> List[Path]:
    files_copy = files[:]
    random.shuffle(files_copy)
    return files_copy


def sort_by_regex(
    files: List[Path],
    pattern: str,
    reverse: bool = False,
) -> List[Path]:
    """
    pattern должен содержать группу с номером
    пример: ^(\\d+)_.*\\.docx$
    """
    regex = re.compile(pattern)

    def extract_key(file: Path) -> int:
        match = regex.search(file.name)
        if not match:
            raise ValueError(
                f"Файл '{file.name}' не соответствует регулярному выражению"
            )
        return int(match.group(1))

    return sorted(files, key=extract_key, reverse=reverse)
