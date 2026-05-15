from blueprint_helper.interface import App
from blueprint_helper import task

def main():
    app = App()
    
    def tick():
        task.execute_all()
        app.after(50, tick)
    
    tick()
    app.mainloop()

if __name__ == "__main__":
    main()