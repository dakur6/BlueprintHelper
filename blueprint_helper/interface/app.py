import tkinter
import webbrowser
from tkinter import ttk
from blueprint_helper.interface.views import View, MainView, OptimizeView

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.__views = {}

        self.title("Sprocket Blueprint Helper")
        self.geometry("800x600")
        self.state('zoomed')

        self.style = ttk.Style()
        self.style.configure("BigButton.TButton", font=("Arial", 16, "bold"), padding=20)
        self.style.configure("Footer.TLabel", font=("Arial", 9), foreground="gray")

        container = tkinter.Frame(self)
        container.pack(fill=tkinter.BOTH, expand=True)

        self.content = tkinter.Frame(container, bg="#f0f0f0")
        self.content.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=(10, 0))

        ttk.Separator(container, orient='horizontal').pack(fill=tkinter.X, padx=10, pady=(10, 0))

        self.footer = tkinter.Frame(container, bg="#e8e8e8", height=40)
        self.footer.pack(fill=tkinter.X, padx=10, pady=10)
        self.footer.pack_propagate(False)

        github_label = tkinter.Label(
            self.footer, 
            text="GitHub", 
            font=("Arial", 9),
            bg="#e8e8e8",
            fg="gray",
            cursor="hand2"
        )
        github_label.pack(side=tkinter.LEFT, padx=10)
        github_label.bind("<Button-1>", lambda event: webbrowser.open("https://github.com/dakur6/BlueprintHelper"))
        github_label.bind("<Enter>", lambda event: github_label.config(fg="#404040"))
        github_label.bind("<Leave>", lambda event: github_label.config(fg="gray"))

        version_label = tkinter.Label(
            self.footer, 
            text="Версия 0.1.0 beta",
            font=("Arial", 9),
            bg="#e8e8e8",
            fg="gray",
            cursor="hand2"
        )
        version_label.pack(side=tkinter.RIGHT, padx=10)
        version_label.bind("<Button-1>", lambda event: webbrowser.open("https://github.com/dakur6/BlueprintHelper/releases"))
        version_label.bind("<Enter>", lambda event: version_label.config(fg="#404040"))
        version_label.bind("<Leave>", lambda event: version_label.config(fg="gray"))

        self.register_view(MainView.__name__, MainView(self.content, self))
        self.register_view(OptimizeView.__name__, OptimizeView(self.content, self))

        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.show_view("MainView")

    def register_view(self, name: str, view: View) -> None:
        if name in self.__views:
            raise ValueError(f"Попытка зарегистрировать новое представление на зарегистрированное название '{name}'")
        self.__views[name] = view
        view.grid(row=0, column=0, sticky="nsew")


    def show_view(self, view_name):
        if not view_name in self.__views:
            raise ValueError(f"Некорректное название view: '{view_name}'")
        self.__views[view_name].tkraise()