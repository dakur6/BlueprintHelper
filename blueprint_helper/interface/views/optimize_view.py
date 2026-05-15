import tkinter
from tkinter import ttk
from typing import List
from blueprint_helper.interface.views.view import View

LABEL_HEADER = "header"
LABEL_SELECT_PATH = "select_path"
BUTTON_BACK = "back"


class OptimizeView(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._files: List[str] = []

    def setup(self):
        top_panel = tkinter.Frame(self, bg="#f0f0f0")
        top_panel.pack(fill=tkinter.X, padx=40, pady=10)

        self.content = tkinter.Frame(self, bg='white')
        self.content.pack(fill='both', expand=True, padx=40, pady=(0, 20))

        self.files_frame = tkinter.Frame(self.content, bg='white')
        self.files_frame.pack(fill='both', expand=True)

        tkinter.Label(
            top_panel,
            text="Оптимизировать модель",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        ).pack(expand=True)
        tkinter.Label(
            self.files_frame,
            text="Перетащите .blueprint файл сюда\nили нажмите, чтобы выбрать",
            font=("Arial", 16),
            bg='white',
            fg='gray',
            justify='center'
        ).pack(expand=True)

        ttk.Button(
            top_panel,
            text="Назад",
            command=lambda: self._controller.show_view("MainView")
        ).pack(side=tkinter.LEFT)