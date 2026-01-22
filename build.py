import subprocess
import sys
import os
from pathlib import Path

import docxcompose


def main() -> None:
    pkg_path = Path(docxcompose.__file__).parent

    if not pkg_path.exists():
        raise RuntimeError(f"docxcompose package not found: {pkg_path}")

    add_data_arg = f"{pkg_path}{os.pathsep}docxcompose"

    subprocess.check_call([
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name",
        "WordMerger",
        "--add-data",
        add_data_arg,
        "app/main.py",
    ])


if __name__ == "__main__":
    main()
