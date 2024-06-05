import random
import tkinter as tk
from socket import socket
from tkinter import Frame, Canvas, Button, Label, colorchooser, messagebox, font
import socket
import select
import datetime

ip_list = []


def vyberSlovo():
    words = ["auto", "dom", "pes", "skola", "hra", "kniha", "cesta", "hracka", "kava", "mesto",
             "les", "horska chata", "hracka", "jablko", "pocitac", "chlieb", "kolac", "jedlo",
             "hudba", "film", "rastlina", "stol", "okno", "dvere", "lopta", "hudba",
             "detska izba", "obchod", "trh", "obrazok", "fotografia", "krajina", "voda",
             "ocean", "rieka", "jazero", "plaz", "lod", "lietadlo", "vlak",
             "hory", "zima", "jesen", "jar", "leto", "mracno", "dazd",
             "sneh", "vietor", "mraz", "teplota", "krajina", "polnohospodarstvo", "lesnicstvo",
             "zvierata", "pes", "macka", "vtak", "ryba", "sliepka", "krava", "ovca", "koza",
             "konik", "zirafa", "lev", "tiger", "slon", "medved", "vlk", "cajka", "sova",
             "papagaj", "korytnacka", "krokodil", "hady", "zajac", "mys", "hadica", "motyl",
             "vcela", "mravce", "skorpion", "mravciar", "slon", "zirafa", "tiger", "jazvec",
             "gorila", "orangutan", "simpanz", "delfin", "velryba", "tucniak", "pingvin",
             "papagaj", "kanar", "holub", "sokol", "orol", "kondor", "sliepka", "kacica",
             "hus", "labut", "cajka", "sova", "straka", "kos", "vazka", "motyl", "chrobak",
             "komar", "osadka", "vcela", "medovacik", "pcela", "bumbar", "motylik", "hmyz",
             "krava", "dazd", "mraz", "vietor", "jesen", "zima", "zima", "jesen", "leto"]
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


class PaintApp:
    def __init__(self, parent, chat_window, timer_label, points_label, letter_label):
        self.parent = parent
        self.startButton = startButton
        self.ip_list = ip_list
        self.chat_window = chat_window
        self._address = chat_window._address
        self.timer_label = timer_label
        self.points_label = points_label
        self.letter_label = letter_label
        self.hodnota = vyberSlovo()
        self.hodnota2 = ciarky(self.hodnota)
        self.prevPoint = [0, 0]
        self.currentPoint = [0, 0]
        self.penColor = "black"
        self.stroke = 1
        self.timer_seconds = 60
        self.drawing_enabled = False
        self.setup_ui()
        self.timer_id = None
        self.round = 1
        self.total_rounds = 5
        self.points_per_round = 1000
        self.points_history = {}
        self.clicked_button = None

    def setup_ui(self):
        self.holder = Frame(self.parent, height=120, width=500, bg="dark gray", padx=100, pady=10)
        self.holder.pack(fill=tk.X, padx=5, pady=5)

        def change_button_bg(button, color):
            button.config(bg=color)

        def reset_button_bg():
            if self.clicked_button:
                self.clicked_button.config(bg="SystemButtonFace")

        pencilButton = Button(self.holder, text="Pero", height=1, width=12, command=self.pencil, font=("Montserrat", 9))
        pencilButton.grid(row=0, column=0)
        pencilButton.bind("<Button-1>", lambda event: (reset_button_bg(), change_button_bg(pencilButton, "#c4c4c4"), setattr(self, "clicked_button", pencilButton)))

        eraserButton = Button(self.holder, text="Guma", height=1, width=12, command=self.eraser, font=("Montserrat", 9))
        eraserButton.grid(row=0, column=1)
        eraserButton.bind("<Button-1>", lambda event: (reset_button_bg(), change_button_bg(eraserButton, "#c4c4c4"), setattr(self, "clicked_button", eraserButton)))

        colorButton = Button(self.holder, text="Vyber Farbu", height=1, width=12, command=self.colorChoice,font=("Montserrat", 9))
        colorButton.grid(row=0, column=2)
        colorButton.bind("<Button-1>", lambda event: (reset_button_bg(), change_button_bg(colorButton, "#c4c4c4"), setattr(self, "clicked_button", colorButton)))

        sizeiButton = Button(self.holder, text="Hrubka +", height=1, width=12, command=self.strokeI,
                             font=("Montserrat", 9))
        sizeiButton.grid(row=0, column=3)
        sizeiButton.bind("<Button-1>", lambda event: (reset_button_bg(), change_button_bg(sizeiButton, "#c4c4c4"), setattr(self, "clicked_button", sizeiButton)))

        sizedButton = Button(self.holder, text="Hrubka -", height=1, width=12, command=self.strokeD,
                             font=("Montserrat", 9))
        sizedButton.grid(row=0, column=4)
        sizedButton.bind("<Button-1>", lambda event: (reset_button_bg(), change_button_bg(sizedButton, "#c4c4c4"), setattr(self, "clicked_button", sizedButton)))

        clearButton = Button(self.holder, text="Vymazat", height=1, width=12, command=self.clearScreen,
                             font=("Montserrat", 9, "bold"), bg="red", fg="white")
        clearButton.grid(row=0, column=5)

        self.thicknessLabel = Label(self.holder, text=f"Hrubka: {self.stroke}", height=1, width=12)
        self.thicknessLabel.grid(row=0, column=6)

        # Add word label and button to choose a new word
        # self.word_label = Label(self.holder, text="Vybrané slovo: " + self.hodnota, font=("Arial", 14))
        # self.word_label.grid(row=1, column=0, columnspan=3, pady=10)

        # self.new_word_button = Button(self.holder, text="Vyber nové slovo", height=1, width=12, command=self.update_word)
        # self.new_word_button.grid(row=1, column=3, columnspan=3, pady=10)

        self.canvas = Canvas(self.parent, height=450, width=500, bg="white", cursor="pencil")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)

    def start_hra(self):
        self.startButton.destroy()
        self.vyber = "192.168.48.61"
        if self.vyber == self._address.get():
            self.drawing_enabled = False
            self.chat_window.guess_enabled = True
            self.timer_label.config(text="")
            # self.word_label.grid_remove()
            # self.new_word_button.grid_remove()
        else:
            self.drawing_enabled = True
            self.chat_window.guess_enabled = True
            self.start_delay()
            # self.word_label.grid_remove()

    def start_delay(self):
        self.drawing_enabled = False
        tk.messagebox.showinfo("Slovo", self.hodnota)
        self.timer_label.config(text="Čas: 60 s - Hra sa za chvíľu začne")
        self.parent.after(5000, self.start_timer)
        self.clearScreen()

    def start_timer(self):
        if self.timer_id is not None:
            self.parent.after_cancel(self.timer_id)
        print(self._address.get())
        self.drawing_enabled = True
        self.timer_seconds = 60
        self.update_timer_label()

    def update_timer_label(self):
        self.timer_label.config(text=f"Čas: {self.timer_seconds} s")
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

    def stop_timer(self):
        if self.timer_id is not None:
            self.parent.after_cancel(self.timer_id)
            self.timer_id = None

    def update_word(self):
        self.hodnota = vyberSlovo()
        self.hodnota2 = ciarky(self.hodnota)
        # self.word_label.config(text="Vybrané slovo: " + self.hodnota)
        self.letter_label.config(text="" + self.hodnota2)
        self.clearScreen()
        self.stop_timer()
        self.start_delay()
        self.round += 1
        if self.round > self.total_rounds:
            self.end_game()

    def end_game(self):
        winner, winner_points = self.determine_winner()
        messagebox.showinfo("Koniec hry", f"Vitaz: {winner} s {winner_points} bodmi!")

    def determine_winner(self):
        max_points = max(self.points_history.values())
        winner = [player for player, points in self.points_history.items() if points == max_points][0]
        return winner, max_points

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
        color = colorchooser.askcolor(title="Vyber farbu")
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

    def update_thickness_label(self):
        self.thicknessLabel.config(text=f"Hrubka: {self.stroke}")

class ChatWindow:

    def __init__(self, parent, paint_app):
        entry_font = font.Font(font=("Montserrat"))

        self.parent = parent
        self.ip_list = ip_list
        self.paint_app = paint_app
        self.frame = Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.guess_enabled = False
        self.body = 0

        self.listbox = tk.Listbox(self.frame, font=entry_font)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        input_frame = Frame(self.frame)
        input_frame.pack(fill=tk.X)

        self._address = tk.Entry(input_frame, font=entry_font)
        self._address.insert(0, '192.18.50.219')
        self._address.pack(side=tk.LEFT, padx=5, pady=5)
        self._address.config(width=11)

        self._message = tk.Entry(input_frame, font=entry_font)
        self._message.insert(0, '')
        self._message.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self._message.bind("<Return>", self.btn_pressed)

        self._btn_send = Button(input_frame, text="Odoslat", command=self.btn_pressed, font=("Montserrat", 9))
        self._btn_send.pack(side=tk.LEFT, padx=5, pady=5)

        self._btn_connect = Button(input_frame, text="Pripojit", command=self.btn_pressed2, font=("Montserrat", 9))
        self._btn_connect.pack(side=tk.LEFT, padx=5, pady=5)

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('0.0.0.0', 20000))
        self.periodic()

    def periodic(self):
        rx_ev, _, _ = select.select([self._sock], [], [], 0)
        if rx_ev:
            data, address = self._sock.recvfrom(200)
            if address[0] not in self.ip_list:
                self.ip_list.append(address[0])
            self.add_message(address[0], data.decode())
            entered_word = data.decode()
            if entered_word == self.paint_app.hodnota:
                self._message.delete(0, tk.END)
                self.body += 1
                points_label.config(text=self.body)
                tk.messagebox.showinfo(":)", "Uhadol" + " " + address[0])
                self.paint_app.update_word()
                self.paint_app.stop_timer()
                # self.paint_app.start_delay()
            print(data.decode())
        self.parent.after(1000, self.periodic)

    def add_message(self, address, message):
        if not self.guess_enabled:
            return
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.listbox.insert(tk.END, f"{timestamp} {address}: {message}")
        self.listbox.yview(tk.END)

    def btn_pressed(self, event=None):
        message = self._message.get().strip()
        address = self._address.get()
        if address and message:
            self._sock.sendto(message.encode(), (address, 20000))
            self.add_message(address, message)
            self._message.delete(0, tk.END)
            return
        self._message.delete(0, tk.END)

    def btn_pressed2(self, event=None):
        address = self._address.get()
        if address:
            self._sock.sendto(address.encode(), (address, 20000))
            self._message.delete(0, tk.END)
            return
        self._message.delete(0, tk.END)

    def start_guessing_after_delay(self):
        self.guess_enabled = True


def point_system(num_players, total_points):
    points = []
    remaining_points = total_points
    for i in range(1, num_players + 1):
        player_points = int(total_points * (1 / i))
        player_points = min(player_points, remaining_points)
        remaining_points -= player_points
        points.append(player_points)
    return points


total_points = 1000
num_players_connected = len(ip_list)
points_distribution = point_system(num_players_connected, total_points)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MultiApp - Paint and Chat")
    root.geometry("1400x650")

    header_frame = Frame(root, height=50, width=1100)
    header_frame.pack(fill=tk.X, padx=5, pady=5)

    timer_label = Label(header_frame, text="Čas: 60 s", font=("Montserrat", 15))
    timer_label.pack(side=tk.LEFT, padx=5, pady=5)

    letter_label = Label(header_frame, text=ciarky(vyberSlovo()), font=("Montserrat", 15))
    letter_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)

    points_label = Label(header_frame, text="0", font=("Montserrat", 15))
    points_label.pack(side=tk.RIGHT, padx=5, pady=5)

    startButton = Button(header_frame, text="START", height=1, width=12, font=("Montserrat", 15), bg="green", fg="white")
    startButton.pack(side=tk.RIGHT, padx=5, pady=5)

    body_frame = Frame(root, bg="dark gray")
    body_frame.pack(fill=tk.BOTH, expand=True)

    paint_frame = Frame(body_frame, width=550, bg="dark gray")
    paint_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    chat_frame = Frame(body_frame, width=550, bg="white")
    chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    chat_window = ChatWindow(chat_frame, None)  # Pass None for paint_app for now
    paint_app = PaintApp(paint_frame, chat_window, timer_label, points_label, letter_label)
    # Now chat_window is defined, so you can pass it to PaintApp
    startButton.config(command=paint_app.start_hra)

    chat_window.paint_app = paint_app

    root.resizable(False, False)
    root.mainloop()
