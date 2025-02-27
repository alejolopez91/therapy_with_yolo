import tkinter as tk
import subprocess

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interactive Menu")
        self.geometry("1200x800")
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()
        main_menu = tk.Frame(self)
        main_menu.pack(expand=True)

        profile_button = tk.Button(main_menu, text="Profile View", command=self.profile_view)
        profile_button.pack(pady=10)

        dashboard_button = tk.Button(main_menu, text="Dashboard View", command=self.dashboard_view)
        dashboard_button.pack(pady=10)

        exercise_button = tk.Button(main_menu, text="Exercise View", command=self.exercise_view)
        exercise_button.pack(pady=10)

    def profile_view(self):
        self.clear_frame()
        profile_frame = tk.Frame(self)
        profile_frame.pack(expand=True)

        label = tk.Label(profile_frame, text="Profile View")
        label.pack(pady=10)

        back_button = tk.Button(profile_frame, text="Back to Main Menu", command=self.create_main_menu)
        back_button.pack(pady=10)

    def dashboard_view(self):
        self.clear_frame()
        dashboard_frame = tk.Frame(self)
        dashboard_frame.pack(expand=True)

        label = tk.Label(dashboard_frame, text="Dashboard View")
        label.pack(pady=10)

        back_button = tk.Button(dashboard_frame, text="Back to Main Menu", command=self.create_main_menu)
        back_button.pack(pady=10)

    def exercise_view(self):
        self.clear_frame()
        exercise_frame = tk.Frame(self)
        exercise_frame.pack(expand=True)

        label = tk.Label(exercise_frame, text="Exercise View")
        label.pack(pady=10)

        back_button = tk.Button(exercise_frame, text="Back to Main Menu", command=self.create_main_menu)
        back_button.pack(pady=10)
        # Run yolo-pose-estimation.py
        subprocess.Popen(["python", "yolo-pose-estimation.py"])

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()