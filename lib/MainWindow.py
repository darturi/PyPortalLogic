import os
import tkinter as tk


class MainWindow(tk.Frame):
    window_title = "PortalLogic"
    window_geometry = "600x200"
    accent_color = "#8a2be2"
    main_foreground = "white"
    light_grey = "#f0f0f0"

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.parent.title(MainWindow.window_title)
        self.parent.geometry(MainWindow.window_geometry)

        # Hello Message
        self.title = tk.Label(self.parent, text="Hello Jordan!", font=("Arial", 20, "bold"))
        self.title.pack(side=tk.TOP, padx=10)

        # Link Input Point
        prompt = tk.StringVar()
        prompt.set("Enter Spotify playlist link here")

        self.input = tk.Entry(self.parent, textvariable=prompt)
        self.input.pack(fill="x", expand=False)

        self.input.bind("<FocusIn>", (lambda event: prompt.set('') if self.input.get() == 'Enter Spotify playlist link here' else None))

        # Button to execute
        self.new_note = tk.Button(self.parent, text="Translate Playlist", font=("Arial", 12),
                                  bg=MainWindow.accent_color, fg=MainWindow.accent_color, width=15)
        self.new_note.pack(side=tk.BOTTOM, padx=10, pady=10)





def demo():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    demo()