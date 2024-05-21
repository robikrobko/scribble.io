import random
import tkinter as tk
from tkinter import Frame, Canvas, Button, Label, colorchooser, messagebox
import socket
import select
import datetime

def vyberSlovo():
    words = ["auto", "dom", "strom", "kvet", "pes", "macka", "slon", "lod", "hracka", "ryba"]
    current_word = random.choice(words)
    return current_word

class PaintApp:
    def __init__(self, parent, chat_window):
        self.parent = parent
        self.chat_window = chat_window
        self.prevPoint = [0, 0]
        self.currentPoint = [0, 0]
        self.penColor = "black"
        self.stroke = 1
        self.current_word = vyberSlovo()
        self.timer_seconds = 60
        self.drawing_enabled = False
        self.setup_ui()
        self.timer_id = None

    def setup_ui(self):
        self.holder = Frame(self.parent, height=120, width=500, bg="white", padx=100, pady=10)
        self.holder.pack(fill=tk.X, padx=5, pady=5)

        pencilButton = Button(self.holder, text="Pero", height=1, width=12, command=self.pencil)
        pencilButton.grid(row=0, column=0)

        eraserButton = Button(self.holder, text="Guma", height=1, width=12, command=self.eraser)
        eraserButton.grid(row=0, column=1)

        colorButton = Button(self.holder, text="Vyber Farbu", height=1, width=12, command=self.colorChoice)
        colorButton.grid(row=0, column=2)

        sizeiButton = Button(self.holder, text="Hrubka +", height=1, width=12, command=self.strokeI)
        sizeiButton.grid(row=0, column=3)

        sizedButton = Button(self.holder, text="Hrubka -", height=1, width=12, command=self.strokeD)
        sizedButton.grid(row=0, column=4)

        clearButton = Button(self.holder, text="Vymazat", height=1, width=12, command=self.clearScreen)
        clearButton.grid(row=0, column=5)

        # Add word label and button to choose a new word
        self.word_label = Label(self.holder, text="Vybrané slovo: " + self.current_word, font=("Arial", 14))
        self.word_label.grid(row=1, column=0, columnspan=3, pady=10)

        new_word_button = Button(self.holder, text="Vyber nové slovo", height=1, width=12, command=self.update_word)
        new_word_button.grid(row=1, column=3, columnspan=3, pady=10)

        self.timer_label = Label(self.holder, text="Čas: 60 s", font=("Arial", 14))
        self.timer_label.grid(row=2, column=0, columnspan=6, pady=10)

        self.canvas = Canvas(self.parent, height=450, width=500, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)

        self.start_delay()

    def start_delay(self):
        self.timer_label.config(text="Čas: 60 s - Hra sa za chvíľu začne")
        self.parent.after(5000, self.start_timer)
        self.clearScreen()
        self.drawing_enabled = False
        self.chat_window.guess_enabled = False

    def start_timer(self):
        if self.timer_id is not None:
            self.parent.after_cancel(self.timer_id)
        self.chat_window.guess_enabled = True
        self.drawing_enabled = True
        self.timer_seconds = 60
        self.update_timer_label()

    def update_timer_label(self):
        self.timer_label.config(text=f"Čas: {self.timer_seconds} s")
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_id = self.parent.after(1000, self.update_timer_label)
        else:
            self.timer_id = None
            messagebox.showinfo("Koniec času", "Čas vypršal!")
            self.start_delay()

    def stop_timer(self):
        if self.timer_id is not None:
            self.parent.after_cancel(self.timer_id)
            self.timer_id = None

    def update_word(self):
        self.current_word = vyberSlovo()
        self.word_label.config(text="Vybrané slovo: " + self.current_word)
        self.clearScreen()
        self.stop_timer()
        self.start_delay()

    def strokeI(self):
        if self.stroke != 10:
            self.stroke += 1

    def strokeD(self):
        if self.stroke != 1:
            self.stroke -= 1

    def pencil(self):
        self.penColor = "black"

    def eraser(self):
        self.penColor = "white"

    def colorChoice(self):
        color = colorchooser.askcolor(title="Select a Color")
        if color[1]:
            self.penColor = color[1]

    def paint(self, event):
        if not self.drawing_enabled:
            return
        x = event.x
        y = event.y
        self.currentPoint = [x, y]

        if self.prevPoint != [0, 0]:
            self.canvas.create_line(
                self.prevPoint[0],
                self.prevPoint[1],
                self.currentPoint[0],
                self.currentPoint[1],
                fill=self.penColor,
                width=self.stroke,
            )

        self.prevPoint = self.currentPoint

        if event.type == "5":
            self.prevPoint = [0, 0]

    def clearScreen(self):
        self.canvas.delete("all")

class ChatWindow:
    def __init__(self, parent, paint_app):
        self.parent = parent
        self.paint_app = paint_app
        self.frame = Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.guess_enabled = False

        self.listbox = tk.Listbox(self.frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        input_frame = Frame(self.frame)
        input_frame.pack(fill=tk.X)

        self._address = tk.Entry(input_frame)
        self._address.insert(0, '127.0.0.1')
        self._address.pack(side=tk.LEFT, padx=5, pady=5)
        self._address.config(width=12)

        self._message = tk.Entry(input_frame)
        self._message.insert(0, '')
        self._message.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self._message.bind("<Return>", self.btn_pressed)

        self._btn_send = Button(input_frame, text="Odoslat", command=self.btn_pressed)
        self._btn_send.pack(side=tk.LEFT, padx=5, pady=5)

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('0.0.0.0', 20000))

        self.periodic()

    def periodic(self):
        rx_ev, _, _ = select.select([self._sock], [], [], 0)
        if rx_ev:
            data, address = self._sock.recvfrom(200)
            if self.guess_enabled:
                self.add_message(address[0], data.decode())
        self.parent.after(1000, self.periodic)

    def add_message(self, address, message):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.listbox.insert(tk.END, f"{timestamp} {address}: {message}")
        self.listbox.yview(tk.END)

    def btn_pressed(self, event=None):
        message = self._message.get().strip()
        address = self._address.get()
        if address and message:
            entered_word = message
            if entered_word == self.paint_app.current_word:
                self._message.delete(0, tk.END)
                messagebox.showinfo(":)", "Uhadol si!")
                self.paint_app.update_word()
                self.paint_app.stop_timer()
                self.paint_app.start_delay()
            else:
                self._sock.sendto(message.encode(), (address, 20000))
                self._message.delete(0, tk.END)
                return
            self._message.delete(0, tk.END)

    def start_guessing_after_delay(self):
        self.guess_enabled = True


if __name__ == "__main__":
    root = tk.Tk()
    root.title("MultiApp - Paint and Chat")
    root.geometry("1100x650")

    header_frame = Frame(root, height=50, width=1100)
    header_frame.pack(fill=tk.X, padx=5, pady=5)

    points_label = Label(header_frame, text="100 BODOV", font=("Arial", 20))
    points_label.pack(side=tk.RIGHT, padx=5, pady=5)

    body_frame = Frame(root)
    body_frame.pack(fill=tk.BOTH, expand=True)

    paint_frame = Frame(body_frame, width=550, bg="gray")
    paint_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    chat_frame = Frame(body_frame, width=550, bg="white")
    chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    chat_window = ChatWindow(chat_frame, None)  # Pass None for paint_app for now
    paint_app = PaintApp(paint_frame, chat_window)  # Now chat_window is defined, so you can pass it to PaintApp
    chat_window.paint_app = paint_app

    root.mainloop()
