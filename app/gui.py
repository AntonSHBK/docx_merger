import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from merger import merge_docx
from sorting import (
    get_docx_files,
    sort_by_name,
    sort_by_creation_date,
    sort_random,
    sort_by_regex,
)


class DocxMergerGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Word Merger")

        self.input_dir: Path | None = None
        self.result_document = None

        # ===== UI VARIABLES =====
        self.sort_mode = tk.StringVar(value="name")
        self.sort_order = tk.StringVar(value="asc")  # asc | desc

        self.regex_pattern = tk.StringVar(
            value=r"^(\d+)_.*\.docx$"
        )

        self._build_ui()
        self._update_regex_state()

    def _build_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        # ---- Folder ----
        tk.Button(frame, text="Выбрать папку", command=self.choose_folder).pack(fill="x")
        self.folder_label = tk.Label(frame, text="Папка не выбрана")
        self.folder_label.pack(anchor="w", pady=5)

        # ---- Sorting mode ----
        tk.Label(frame, text="Способ сортировки:").pack(anchor="w")

        for text, value in [
            ("По имени", "name"),
            ("По дате создания", "date"),
            ("Случайный порядок", "random"),
            ("По регулярному выражению", "regex"),
        ]:
            tk.Radiobutton(
                frame,
                text=text,
                variable=self.sort_mode,
                value=value,
                command=self._update_regex_state,
            ).pack(anchor="w")

        # ---- Regex ----
        tk.Label(frame, text="Регулярное выражение:").pack(anchor="w")

        self.regex_entry = tk.Entry(
            frame,
            textvariable=self.regex_pattern,
            width=50,
        )
        self.regex_entry.pack(fill="x")

        tk.Label(
            frame,
            text="Пример: ^(\\d+)_.*\\.docx$ | Файлы называется как '1_file.docx', '2_file.docx' и т.д.",
            fg="gray",
        ).pack(anchor="w", pady=(0, 10))

        # ---- Sort order ----
        tk.Label(frame, text="Порядок сортировки:").pack(anchor="w")

        tk.Radiobutton(
            frame,
            text="По возрастанию",
            variable=self.sort_order,
            value="asc",
        ).pack(anchor="w")

        tk.Radiobutton(
            frame,
            text="По убыванию",
            variable=self.sort_order,
            value="desc",
        ).pack(anchor="w")

        # ---- Buttons ----
        tk.Button(frame, text="Объединить", command=self.merge).pack(fill="x", pady=5)
        tk.Button(frame, text="Выгрузить", command=self.export).pack(fill="x")

    def _update_regex_state(self):
        if self.sort_mode.get() == "regex":
            self.regex_entry.config(state="normal")
        else:
            self.regex_entry.config(state="disabled")

    def choose_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.input_dir = Path(path)
            self.folder_label.config(text=str(self.input_dir))

    def merge(self):
        if not self.input_dir:
            messagebox.showerror("Ошибка", "Папка не выбрана")
            return

        try:
            files = get_docx_files(self.input_dir)
            if not files:
                raise ValueError("В папке нет .docx файлов")

            reverse = self.sort_order.get() == "desc"
            mode = self.sort_mode.get()

            if mode == "name":
                files = sort_by_name(files, reverse=reverse)

            elif mode == "date":
                files = sort_by_creation_date(files, reverse=reverse)

            elif mode == "random":
                files = sort_random(files)

            elif mode == "regex":
                pattern = self.regex_pattern.get().strip()
                if not pattern:
                    raise ValueError("Регулярное выражение не задано")
                files = sort_by_regex(files, pattern, reverse=reverse)

            self.result_document = merge_docx(files)

            messagebox.showinfo(
                "Успешно",
                f"Объединено файлов: {len(files)}"
            )

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def export(self):
        if not self.result_document:
            messagebox.showerror("Ошибка", "Сначала выполните объединение")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word files", "*.docx")],
        )

        if path:
            self.result_document.save(path)
            messagebox.showinfo("Готово", f"Файл сохранён:\n{path}")
