import tkinter
from tkinter import ttk
from blueprint_helper.interface.views.view import View

LABEL_HEADER = "header"
BUTTON_OPTIMIZE = "optimize"
BUTTON_MERGE = "merge"

class MainView(View):
    def setup(self):
        center_frame = tkinter.Frame(self, bg="#f0f0f0")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tkinter.Label(
            center_frame, 
            text="Sprocket Blueprint Helper", 
            font=("Arial", 24, "bold"), 
            bg="#f0f0f0"
        ).pack(pady=(0, 30))

        ttk.Button(
            center_frame, 
            text="Оптимизировать", 
            style="BigButton.TButton", 
            cursor="hand2",
            command=lambda: self._controller.show_view("OptimizeView")
        ).pack(fill=tkinter.X, pady=10)

        ttk.Button(
            center_frame, 
            text="Объединить", 
            style="BigButton.TButton",
            cursor="hand2",
            command=lambda: self._controller.show_view("OptimizeView")
        ).pack(fill=tkinter.X, pady=10)