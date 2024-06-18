import json
import random
import tkinter as tk
from socket import socket
from tkinter import Frame, Canvas, Button, Label, colorchooser, messagebox
import select
import datetime
import tkinter.font as tkFont
import socket


ip_list = []
ip_list2 = {}
vyber = "192.168.48.61"
nekreslim = False


def vyberSlovo():
    words = ["auto", "dom", "pes", "skola", "hra", "kniha", "cesta", "hracka", "kava", "mesto",
             "les", "horska chata", "hracka", "jablko", "pocitac", "chlieb", "kolac", "jedlo",
             "hudba", "film", "rastlina", "stol", "okno", "dvere", "lopta", "hudba",
             "detska izba", "obchod", "trh", "obrazok", "fotografia", "krajina", "voda",
             "ocean", "rieka", "jazero", "plaz", "lod", "lietadlo", "vlak",
             "hory", "zima", "jesen", "jar", "leto", "mracno", "dazd",
             "sneh", "vietor", "mraz", "teplota", "krajina", "polnohospodarstvo", "lesnicstvo",
             "zvierata", "pes", "macka", "ryba", "krava", "ovca", "koza",
             "konik", "zirafa", "lev", "tiger", "slon", "medved", "vlk", "sova",
             "korytnacka", "krokodil", "hady", "mys", "hadica", "motyl",
             "vcela", "mravce", "skorpion", "mravciar", "slon", "zirafa", "tiger", "jazvec",
             "gorila", "orangutan", "simpanz", "delfin", "velryba", "tucniak", "pingvin",
             "papagaj", "kanar", "holub", "sokol", "orol", "kondor", "sliepka",
             "kos", "vazka", "motyl", "chrobak", "koza bobkov", "ujo to je mercedes",
             "komar", "osadka", "vcela", "medovacik", "pcela", "bumbar", "motylik", "hmyz",
             "krava", "dazd", "mraz", "vietor", "jesen", "zima", "jesen", "leto"]

    current_word = random.choice(words)
    return current_word


def ciarky(slovo):
    pismena = ""
    for i in range(len(slovo)):
        pismena += " _"
    return pismena


def ciarky_premena(hodnota, hodnota2):
    dlzka = len(hodnota)
    novy = list(hodnota2.replace(" ", ""))
    while True:
        vyber = random.randint(0, dlzka - 1)
        if novy[vyber] == "_":
            novy[vyber] = hodnota[vyber]
            break
    return " ".join(novy)


def is_ip_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False


def is_color_dark(color):
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return luminance < 128


class PaintApp:
    def __init__(self, parent, chat_window, timer_label, points_label, letter_label):
        self.parent = parent
        self.startButton = startButton
        self.ip_list = ip_list
        self.vyber = vyber
        self.chat_window = chat_window
        self.timer_label = timer_label
        self.points_label = points_label
        self.letter_label = letter_label
        self.hodnota = vyberSlovo()
        self.hodnota2 = ciarky(self.hodnota)
        self.prevPoint = [0, 0]
        self.currentPoint = [0, 0]
        self.penColor = "black"
        self.stroke = 5
        self.timer_seconds = 60
        self.drawing_enabled = False
        self.setup_ui()
        self.timer_id = None
        self.clicked_button = None

    def setup_ui(self):
        self.holder = Frame(self.parent, height=120, width=500, bg="dark gray", padx=100, pady=10)
        self.holder.pack(fill=tk.X, padx=5, pady=5)

        def change_button_bg(button, color):
            button.config(bg=color)

        def reset_button_bg():
            if self.clicked_button:
                self.clicked_button.config(bg="SystemButtonFace")

        pencilButton = Button(self.holder, text="Pero", height=1, width=12, command=self.pencil, font=("Helvetica", 13))
        pencilButton.grid(row=0, column=0)
        pencilButton.bind("<Button-1>", lambda event: (reset_button_bg(), change_button_bg(pencilButton, "#c4c4c4"), setattr(self, "clicked_button", pencilButton)))

        eraserButton = Button(self.holder, text="Guma", height=1, width=12, command=self.eraser, font=("Helvetica", 13))
        eraserButton.grid(row=0, column=1)
        eraserButton.bind("<Button-1>", lambda event: (reset_button_bg(), change_button_bg(eraserButton, "#c4c4c4"), setattr(self, "clicked_button", eraserButton)))

        self.colorButton = Button(self.holder, text="Vyber Farbu", height=1, width=12, command=self.colorChoice, font=("Helvetica", 13))
        self.colorButton.grid(row=0, column=2)
        self.colorButton.bind("<Button-1>", lambda event: (reset_button_bg(), change_button_bg(self.colorButton, "#c4c4c4"), setattr(self, "clicked_button", self.colorButton)))

        sizeiButton = Button(self.holder, text="Hrubka +", height=1, width=12, command=self.strokeI, font=("Helvetica", 13))
        sizeiButton.grid(row=0, column=3)
        sizeiButton.bind("<Button-1>", lambda event: (reset_button_bg(), change_button_bg(sizeiButton, "#c4c4c4"), setattr(self, "clicked_button", sizeiButton)))

        sizedButton = Button(self.holder, text="Hrubka -", height=1, width=12, command=self.strokeD, font=("Helvetica", 13))
        sizedButton.grid(row=0, column=4)
        sizedButton.bind("<Button-1>", lambda event: (reset_button_bg(), change_button_bg(sizedButton, "#c4c4c4"), setattr(self, "clicked_button", sizedButton)))

        clearButton = Button(self.holder, text="Vymazat", height=1, width=12, command=self.clearScreen, bg="red", fg="white", font=("Helvetica", 13))
        clearButton.grid(row=0, column=5)

        self.thicknessLabel = Label(self.holder, text=f"Hrubka: {self.stroke}", height=1, width=12, font=("Helvetica", 13))
        self.thicknessLabel.grid(row=0, column=6)

        self.canvas = Canvas(self.parent, height=450, width=500, bg="white", cursor="pencil")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.hadane_slovo_label = tk.Label(hadane_slovo, text="")
        self.hadane_slovo_label.pack(padx=20, pady=20)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)

    def start_hra(self):
        if is_ip_connected():
            self.startButton.destroy()
            if nekreslim:
                self.drawing_enabled = False
                self.chat_window.guess_enabled = True
                self.timer_label.config(text="", font=("Helvetica", 20))
            else:
                self.drawing_enabled = True
                self.chat_window.guess_enabled = True
                self.start_delay()

            ##self.chat_window.hide_name_entry()
        else:
            messagebox.showerror("Error", "Pripojenie k internetu zlyhalo.")

    def start_delay(self):
        self.drawing_enabled = False
        self.hadane_slovo_label.config(text=self.hodnota)
        #tk.messagebox.showinfo("Slovo", self.hodnota)
        self.timer_label.config(text="Čas: 60 s - Hra sa za chvíľu začne", font=("Helvetica", 20))
        self.parent.after(5000, self.start_timer)
        self.clearScreen()

    def start_timer(self):
        if self.timer_id is not None:
            self.parent.after_cancel(self.timer_id)
        self.drawing_enabled = True
        self.timer_seconds = 60
        self.update_timer_label()

    def check_internet_connection(self):
        if is_ip_connected():
            # Internet connection is established
            self.drawing_enabled = True
            self.start_delay()
            self.update_word()
            print("Internet connection reestablished.")
        else:
            # Internet connection is still not established, retry after a delay
            self.parent.after(5000, self.check_internet_connection)

    def update_timer_label(self):
        self.timer_label.config(text=f"Čas: {self.timer_seconds} s", font=("Helvetica", 20))

        if is_ip_connected():
            if self.timer_seconds > 0:
                self.timer_seconds -= 1
                if self.timer_seconds == 39 or self.timer_seconds == 19:
                    self.hodnota2 = ciarky_premena(self.hodnota, self.hodnota2)
                    self.letter_label.config(text=self.hodnota2)
                self.timer_id = self.parent.after(1000, self.update_timer_label)
            else:
                self.timer_id = None
                messagebox.showinfo("Koniec času", "Čas vypršal!")
                self.start_delay()
                self.update_word()
                if self.timer_seconds == 39 or self.timer_seconds == 19:
                    self.hodnota2 = ciarky_premena(self.hodnota, self.hodnota2)
                    self.letter_label.config(text=self.hodnota2)
        else:
            messagebox.showerror("Error", "Pripojenie k internetu zlyhalo.")
            self.drawing_enabled = False
            self.check_internet_connection()

    def stop_timer(self):
        if self.timer_id is not None:
            self.parent.after_cancel(self.timer_id)
            self.timer_id = None

    def update_word(self):
        self.hodnota = vyberSlovo()
        self.hodnota2 = ciarky(self.hodnota)
        self.letter_label.config(text="" + self.hodnota2, font=("Helvetica", 20))
        self.clearScreen()
        self.stop_timer()
        self.start_delay()

    def strokeI(self):
        if self.stroke != 10:
            self.stroke += 1
        self.update_thickness_label()

    def strokeD(self):
        if self.stroke != 1:
            self.stroke -= 1
        self.update_thickness_label()

    def pencil(self):
        self.penColor = "black"
        self.canvas.config(cursor="pencil")

    def eraser(self):
        self.penColor = "white"
        self.canvas.config(cursor="crosshair")

    def colorChoice(self):
        self.penColor = colorchooser.askcolor(color=self.penColor)[1]
        self.colorButton.config(bg=self.penColor)
        self.colorButton.config(fg="white" if is_color_dark(self.penColor) else "black")

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

    def update_thickness_label(self):
        self.thicknessLabel.config(text=f"Hrubka: {self.stroke}", font=("Helvetica", 13))

class ChatWindow:

    def __init__(self, parent, paint_app):
        self.parent = parent
        self.vyber = vyber
        self.ip_list = []
        self.ip_name_map = {}
        self.paint_app = paint_app
        self.frame = Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.guess_enabled = False

        self.listbox_font = tkFont.Font(family="Helvetica", size=14)

        self.listbox = tk.Listbox(self.frame, font=self.listbox_font)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        input_frame = Frame(self.frame)
        input_frame.pack(fill=tk.X)

        self._message_name = tk.Entry(input_frame)
        self._message_name.insert(0, "Tvoje meno")
        self._message_name.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self._message_name.config(width=11, font=("Helvetica", 13))

        self._message = tk.Entry(input_frame)
        self._message.insert(0, '')
        self._message.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self._message.bind("<Return>", self.btn_pressed)
        self._message.config(width=11, font=("Helvetica", 13))

        self._btn_send = Button(input_frame, text="Odoslat", command=self.btn_pressed, font=("Helvetica", 13))
        self._btn_send.pack(side=tk.LEFT, padx=5, pady=5)

        self._btn_connect = Button(input_frame, text="Pripojit", command=self.btn_pressed2, font=("Helvetica", 13))
        self._btn_connect.pack(side=tk.LEFT, padx=5, pady=5)

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('0.0.0.0', 20000))
        self.periodic()

    def hide_name_entry(self):
        self._message_name.pack_forget()

    def periodic(self):
        rx_ev, _, _ = select.select([self._sock], [], [], 0)
        if rx_ev:
            data, addr = self._sock.recvfrom(200)
            ip_address = addr[0]
            if ip_address not in self.ip_list:
                self.ip_list.append(ip_address)
                print(f"New IP address added: {ip_address}")

            try:
                message_data = json.loads(data.decode())
                name = message_data.get("name", ip_address)
                message = message_data.get("message", "")
            except json.JSONDecodeError:
                name = ip_address
                message = data.decode()

            self.add_message(name, message)

            if message == self.paint_app.hodnota:
                self._message.delete(0, tk.END)
                messagebox.showinfo(":)", f"Uhadol {name}")
                self.paint_app.update_word()
                self.paint_app.stop_timer()
            print(f"Data decoded: {data.decode()}")
        self.parent.after(1000, self.periodic)

    def add_message(self, name, message):
        if not self.guess_enabled:
            return
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.listbox.insert(tk.END, f"{timestamp} {name}: {message}")
        self.listbox.yview(tk.END)

    def btn_pressed(self, event=None):
        message = self._message.get().strip()
        address = self.vyber
        name = self._message_name.get()
        if address and message and name:
            message_data = {
                "name": name,
                "message": message,
            }
            self._sock.sendto(json.dumps(message_data).encode(), (address, 20000))
            self.add_message(name, message)
            self._message.delete(0, tk.END)
            return
        self._message.delete(0, tk.END)

    def btn_pressed2(self, event=None):
        address = self.vyber
        name = self._message_name.get()
        if address and name:
            self.ip_name_map[address] = name  # Update the dictionary with the name
            print(f"Mapping added: {address} -> {name}")
            self._message.delete(0, tk.END)
            return
        self._message.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hadaj.oi")
    root.geometry("1600x800")

    if not nekreslim:
        master = tk.Tk()
        master.title("Tabulka")
        master.geometry("600x500")

        hadane_slovo = tk.Tk()
        hadane_slovo.title("Slovo")
        hadane_slovo.geometry("200x100")

    else:
        hadane_slovo = None

    header_frame = Frame(root, height=50, width=1100)
    header_frame.pack(fill=tk.X, padx=5, pady=5)

    timer_label = Label(header_frame, text="Čas: 60 s", font=("Helvetica", 20))
    timer_label.pack(side=tk.LEFT, padx=5, pady=5)

    letter_label = Label(header_frame, text=ciarky(vyberSlovo()), font=("Helvetica", 20))
    letter_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)

    points_label = Label(header_frame, text="0", font=("Helvetica", 20))
    points_label.pack(side=tk.RIGHT, padx=5, pady=5)

    startButton = Button(header_frame, text="START", height=1, width=12, bg="green", fg="white", font=("Helvetica", 15))
    startButton.pack(side=tk.RIGHT, padx=5, pady=5)

    body_frame = Frame(root, bg="dark gray")
    body_frame.pack(fill=tk.BOTH, expand=True)

    paint_frame = Frame(body_frame, width=550, bg="dark gray")
    paint_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    chat_frame = Frame(body_frame, width=550, bg="white")
    chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    chat_window = ChatWindow(chat_frame, None)
    paint_app = PaintApp(paint_frame, chat_window, timer_label, points_label, letter_label)
    startButton.config(command=paint_app.start_hra)

    chat_window.paint_app = paint_app

    if not nekreslim:
        master.resizable(False, False)
        master.mainloop()
        hadane_slovo.resizable(False, False)
        hadane_slovo.mainloop()

    root.resizable(False, False)
    root.mainloop()
