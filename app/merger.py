from pathlib import Path
from typing import List

from docx import Document
from docx.document import Document as DocumentType
from docxcompose.composer import Composer


def merge_docx(files: List[Path]) -> DocumentType:
    if not files:
        raise ValueError("Нет файлов для объединения")

    master: DocumentType = Document(files[0])
    composer = Composer(master)

    for file_path in files[1:]:
        master.add_page_break()
        composer.append(Document(file_path))
    return master
