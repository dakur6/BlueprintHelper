from __future__ import annotations
import tkinter
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from blueprint_helper.interface.app import App

class View(tkinter.Frame, ABC):
    def __init__(self, parent: tkinter.Misc, controller: App):
        super().__init__(parent, bg="#f0f0f0")
        self._controller = controller
        self._labels = {}
        self._buttons = {}
        self.setup()

    @abstractmethod
    def setup(self) -> None:
        pass

    def get_controller(self) -> App:
        return self._controller