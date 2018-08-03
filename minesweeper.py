import tkinter as tk
from random import randint
from os.path import join
from PIL import ImageTk, Image

LARGE_FONT = ("Verdana", 12) # font's family is Verdana, font's size is 12

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Minesweeper")
        self.geometry("300x300")

        #frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.frames = {}
        self.container = container
        for F in (StartPage, game,customGame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, name, row=None, col=None, mines_count=None):
        frame = self.frames[name]
        if mines_count:
            frame.make_table(row, col, mines_count=mines_count)
        elif row:
            frame.make_table(row, col)
        if name == StartPage:
            try:
                app.geometry("300x300+50+50")
            except:
                pass
        if name == customGame:
            try:
                app.geometry("200x100+50+50")
            except:
                pass

        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        height,width = (10,15)
        button8in8   = tk.Button(self, text='8*8\n10mines',   command = lambda : controller.show_frame(game, row=8 , col=8),  height=height, width=width)
        button16in16 = tk.Button(self, text='16*16\n40mines', command = lambda : controller.show_frame(game, row=16, col=16), height=height, width=width)
        button30in16 = tk.Button(self, text='30*16\n99mines', command = lambda : controller.show_frame(game, row=16, col=30), height=height, width=width)
        buttonCustom = tk.Button(self, text='custome',command = lambda : controller.show_frame(customGame), height=height, width=width)

        button8in8.grid(row=0, column=0)
        button16in16.grid(row=0, column=1)
        button30in16.grid(row=1, column=0)
        buttonCustom.grid(row=1, column=1)


class game(tk.Frame):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)
        self.container = container
        self.is_loser = False
        self.width , self.height = (20,20)
        self.click_counter = 0
        self.blank = ImageTk.PhotoImage(Image.open(join(data_path,"blank.jpeg")).resize((self.height,self.width),Image.ANTIALIAS))# tk.PhotoImage(file="data/blank.jpeg")
        self.bomb = ImageTk.PhotoImage(Image.open(join(data_path,"bomb.jpg")).resize((self.height,self.width),Image.ANTIALIAS)) #tk.PhotoImage(file="data/bomb.jpg")
        self.restart_image = ImageTk.PhotoImage(Image.open(join(data_path,"repeat.jpg")).resize((self.height,self.width),Image.ANTIALIAS))
        self.home_image = ImageTk.PhotoImage(Image.open(join(data_path,"home.jpg")).resize((self.height,self.width),Image.ANTIALIAS))
        self.play_image = ImageTk.PhotoImage(Image.open(join(data_path,"play.jpg")).resize((self.height,self.width),Image.ANTIALIAS))
        self.pause_image = ImageTk.PhotoImage(Image.open(join(data_path,"pause.jpg")).resize((self.height,self.width),Image.ANTIALIAS))
        self.flag_image = ImageTk.PhotoImage(Image.open(join(data_path,"flag.jpg")).resize((self.height,self.width),Image.ANTIALIAS))
        self.pause = 1 #if 1 then count elif -1 then stop
        self.numbers = []
        self.flaged_cells = []
        for i in range(9):
            self.numbers.append(ImageTk.PhotoImage(Image.open(join(data_path,str(i) + ".png")).resize((self.height,self.width),Image.ANTIALIAS)))# tk.PhotoImage("data/"+str(i)+".png"))
        self.time_number = "0"*4

    def count_time(self):
        if self.pause == 1:
            sec = int(self.time_number[-2:])+1
            min = int(self.time_number[:2])
            self.time_number = ("0"+str(min+sec//60))[-2:] + ("0"+str(sec%60))[-2:]
            for i in range(4):
                self.time[i].config(text=self.time_number[i])
        app.after(1000,self.count_time)

    def time_controler_press(self):
        self.pause *= -1
        if self.pause == 1:
            self.time_controler.config(image=self.pause_image)
        else:
            self.time_controler.config(image=self.play_image)

    def make_table(self, row, col, mines_count=0):
        if mines_count == 0:
            if row == 8 and col==8:
                mines_count = 10
            elif row == 16 and col==16:
                mines_count = 40
            elif row == 16 and col==30:
                mines_count = 99
            else:
                mines_count = int(row*col/2)
        self.mines_count = mines_count
        offset = 6
        app.geometry(str(col*(offset+self.width))+"x"+str((row+2)*(offset+self.height)))
        self.time_controler = tk.Button(self,image=self.pause_image,command = self.time_controler_press)
        self.time_controler.grid(row=0,column=0)
        ###
        self.time = []
        for i in range(4):
            tmp = tk.Label(self,text = "0")
            tmp.grid(row = 0,column=col//2-2+i)
            self.time.append(tmp)
        self.count_time()
        ###
        self.flag_counter = tk.Label(self,text=mines_count)
        self.flag_counter.grid(row=0,column=col-1)
        self.max_click = row*col-mines_count
        self.buttons = {}
        mines_place = []
        while len(mines_place) < mines_count:
            tmp = [randint(0,row-1),randint(0,col-1)]
            if not tmp in mines_place:
                mines_place.append(tmp)
        for i in range(row):
            for j in range(col):
                button = tk.Button(self, command =lambda i=i,j=j: self.button_down(i,j), image=self.blank, height = self.height, width=self.width)
                button.bind("<Button-3>",lambda arg,i=i,j=j: self.right_click(i,j))
                button.grid(row = i+1,column = j)
                if not [i,j] in mines_place:
                    neighbor_mines = 0
                    for t0 in (-1,0,1):
                        for t1 in (-1,0,1):
                            if [i+t0, j+t1] in mines_place:
                                neighbor_mines += 1
                    self.buttons.update({(i, j):[button, neighbor_mines,False]})
                else:
                    self.buttons.update({(i,j):[button, None]})
        self.restart_button = tk.Button(self, command = lambda : self.container.show_frame(game, row=row, col=col),image=self.restart_image)
        self.restart_button.grid(row=row+2,column=col//2)
        self.home_button = tk.Button(self, command = self.home_button_press,image=self.home_image)
        self.home_button.grid(row=row+2,column=col//2-1)
    def home_button_press(self):
        for b in self.buttons:
            self.buttons[b][0].grid_forget()
        for b in [self.restart_button,self.home_button,self.flag_counter]:
            b.grid_forget()
        for b in self.time:
            b.grid_forget()
        self.container.show_frame(StartPage)
    def button_down(self,row,col):
        if self.pause == -1 or self.is_loser:
            return
        button = self.buttons[(row,col)]
        if button[1] == None:
            button[0].config(image=self.bomb)
            loser_window = loser(tk.Toplevel(self.container))
            print("loser")
            self.is_loser = True
        else:
            button[0].config(image=self.numbers[button[1]])
            if not button[2]:
                self.click_counter += 1
                button[2] = True
                if self.click_counter == self.max_click:
                    winner_window = winner(tk.Toplevel(self.container))
                    print("winner")
                if button[1] == 0:
                    for i in (-1,0,1):
                        for j in (-1,0,1):
                            try:
                                self.button_down(row+i,col+j)
                            except:
                                pass
    def right_click(self,row,col):
        tmp = (row,col)
        button = self.buttons[tmp]
        if (len(button) == 3 and button[2]) or self.is_loser:
            return
        if not tmp in self.flaged_cells:
            if self.mines_count == len(self.flaged_cells):
                return
            self.buttons[tmp][0].config(image=self.flag_image)
            self.flaged_cells.append(tmp)
        else:
            self.buttons[tmp][0].config(image=self.blank)
            self.flaged_cells.pop(self.flaged_cells.index(tmp))
        self.flag_counter.config(text=self.mines_count - len(self.flaged_cells))
class loser:
    def __init__(self, master):
        #self.master = master
        frame = tk.Frame(master)
        label_loser = tk.Label(frame, text = "U lost the game :)", font = LARGE_FONT)
        label_loser.pack()
        quitButton = tk.Button(frame, text = 'Quit', width = 25, command = self.close_windows)
        quitButton.pack()
        frame.pack()
    def close_windows(self):
        app.destroy()

class winner:
    def __init__(self, master):
        #self.master = master
        frame = tk.Frame(master)
        label_loser = tk.Label(frame, text = "U win the game =)", font = LARGE_FONT)
        label_loser.pack()
        quitButton = tk.Button(frame, text = 'Quit', width = 25, command = self.close_windows)
        quitButton.pack()
        frame.pack()
    def close_windows(self):
        app.destroy()

class customGame(tk.Frame):
    def __init__(self, parent,container):
        tk.Frame.__init__(self,parent)
        self.container = container
        width_label = tk.Label(self,text="Width: ")
        width_label.grid(row = 0,column=0)
        self.width_value = tk.StringVar()
        width_text = tk.Entry(self, width=2, textvariable=self.width_value)
        width_text.grid(row=0, column=1)
        width_text.focus_set()
        self.width_value.trace('w',lambda *arg :self.text_change(var=self.width_value))

        height_label = tk.Label(self,text="Hieght: ")
        height_label.grid(row=1,column=0)
        self.height_value = tk.StringVar()
        height_text = tk.Entry(self,width=2, textvariable=self.height_value)
        height_text.grid(row=1,column=1)
        self.height_value.trace('w',lambda *arg:self.text_change(var=self.height_value))

        mineCount_label = tk.Label(self,text="number of mines: ")
        mineCount_label.grid(row=2,column=0)
        self.mineCount_value = tk.StringVar()
        mineCount_text = tk.Entry(self,width=2, textvariable=self.mineCount_value)
        mineCount_text.grid(row=2,column=1)
        self.mineCount_value.trace('w',lambda *arg:self.text_change(var=self.mineCount_value))

        submit_button = tk.Button(self,text="Start",command=self.start)
        submit_button.grid(row=3,column=1)
    def text_change(self,var):
        var.set(str2int(var.get()))
    def start(self):
        try:
            self.container.show_frame(game,row=int(self.width_value.get()),col=int(self.height_value.get()),mines_count=int(self.mineCount_value.get()))
        except:
            pass
def str2int(string):
    ans = 0
    for i in string:
        try:
            if ans > 9:
                break
            ans = ans*10 + int(i)
        except:
            pass
    if ans != 0:
        return ans
    else:
        return ""
data_path = "data"
app = MainWindow()
app.mainloop()
