import tkinter as tk
import pynput as pn
from pynput import keyboard, mouse

class appTest():
    def __init__(self):
        self.file = open('MACRO_INP.txt','w')
        self.mouse_x_y = (0,0)
        self.tk = tk.Tk()
        self.tk.config(bg='black')
        self.tk.geometry("500x500")
        self.tk.title('MACROni')
        self.b1image = tk.PhotoImage(file="record_button_2.png")
        self.b2image = tk.PhotoImage(file="view_cntrl_btn_2.png")
        self.b3image = tk.PhotoImage(file="mouse_button.png")
        self.b1 = tk.Button(self.tk,text='Record inputs',command=self.record,image=self.b1image,borderwidth=2,bg='#ff008c',activebackground='#00b2ff')
        self.b2 = tk.Button(self.tk,text='View Controls',command=self.controls, image = self.b2image,borderwidth=2,bg='#ff008c',activebackground='#00b2ff')
        self.b3 = tk.Button(self.tk,text='Record mouse inputs', command=self.mouse,image = self.b3image, borderwidth=2, bg='#ff008c',activebackground='#00b2ff')
        self.key_listener = pn.keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.mouse_listener = pn.mouse.Listener(on_move=self.on_move,on_click=self.on_click)
        self.inp_ct = 0
        self.key = []
        self.top = None
        self.TpLbl = None
        self.y = -30
        self.trccol = 0
        self.scroll = None
        self.tk.protocol("WM_DELETE_WINDOW", self.on_close)

    def baseBuild(self):
        self.b1.pack()
        self.b1.place(relx=.5,rely=.25,anchor='center')
        self.b2.pack()
        self.b2.place(relx=.5, rely=.5, anchor='center')
        self.b3.pack()
        self.b3.place(relx=.5, rely=.75, anchor='center')
        self.tk.mainloop()

    def record(self):
        self.top = tk.Toplevel(self.tk,bg='black')
        self.top.title('key_tracker')
        self.top.geometry("300x500")
        if self.mouse_listener.running:
            self.mouse_listener.stop()
        if not self.key_listener.running:
            self.key_listener.start()


    def controls(self):
        self.top = tk.Toplevel(self.tk,bg='black')
        self.top.title('controls_view')
        self.top.geometry("300x500")

    def mouse(self):
        self.top = tk.Toplevel(self.tk,bg='black')
        self.top.title('mouse_tracker')
        self.top.overrideredirect(True)
        self.top.wm_attributes("-transparentcolor", "black")
        self.top.attributes("-topmost",True)
        self.top.geometry("100x100")
        self.TpLbl = tk.Label(self.top, bg='#ff008c', fg='#00b2ff', bd=5, borderwidth=3, relief='groove',font=24)
        self.TpLbl.pack()
        self.TpLbl.place(relx=.1, rely=.2)
        if self.key_listener.running:
            self.key_listener.stop()
        if not self.mouse_listener.running:
            self.mouse_listener.start()


    def on_close(self):
        self.file.flush()
        try:
            self.top.destroy()
        except:
            self.tk.destroy()

    def on_press(self, key):
        if key == keyboard.Key.esc:
            print('esc_press')
            if self.key_listener.running:
                self.key_listener.stop()
                print('key_list_stop')
                return False
            elif self.mouse_listener.running:
                print('mouse_list_stop')
                self.mouse_listener.stop()
                return False
            else:
                print('LOGIC_ERROR')
                return True
        self.key.append(key)
        self.inp_ct += 1
        self.file.write(str(key) + '\n')

    def on_release(self, key):
        self.trccol += 1
        self.y += 30
        if self.y >= self.tk.winfo_height():
            self.scroll = tk.Scrollbar(self.top)
            self.scroll.pack()
            self.scroll.place(relx=.9,rely=.4)
        if self.trccol % 2 == 0:
            self.TpLbl = tk.Label(self.top, bg='#ff008c',fg='#00b2ff', bd=5,borderwidth=3,relief='groove')
        else:
            self.TpLbl = tk.Label(self.top, bg='#00b2ff',fg='#ff008c', bd=5,borderwidth=3,relief='groove')
        self.TpLbl.pack()
        self.TpLbl.place(x=10, y=self.y)
        self.TpLbl.config(text=self.key)
        self.TpLbl.update()
        print('inputs held : ' + str(self.inp_ct), self.key)
        self.inp_ct = 0
        self.key = []

    def on_move(self,x,y):
        self.mouse_x_y = (x,y)
        self.TpLbl.config(text=self.mouse_x_y)
        self.top.geometry("+%s+%s" % (x,y))
        self.TpLbl.update()

    def on_click(self,x,y,button,pressed):
        self.file.write(str(button) + ' ' + str((x,y)) + '\n')
        if pressed:
            self.TpLbl.config(text='Click!')
        else:
            pass

    def play(self):
        pass

test = appTest()
test.baseBuild()