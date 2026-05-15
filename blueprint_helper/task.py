from abc import ABC, abstractmethod

class Task(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def on_run(self) -> None:
        pass

__tasks = []

def register(task: Task) -> int:
    __tasks.append(task)
    return len(__tasks) - 1

def unregister(task_id: int) -> bool:
    try:
        del __tasks[task_id]
        return True
    except IndexError:
        return False

def execute_all() -> None:
    for task in __tasks:
        task.on_run()