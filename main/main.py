import tkinter as tk
from tkinter import messagebox as mb
import pynput as pn
from pynput import keyboard, mouse

class appTest():
    def __init__(self):
        self.file = open('MACRO_INP.txt',"w")
        self.mouse_x_y = (None,None)
        self.tk = tk.Tk()
        self.tk.config(bg='black')
        self.tk.geometry("500x500")
        self.tk.title('MACROni')
        self.b1image = tk.PhotoImage(file="record_button_2.png")
        self.b2image = tk.PhotoImage(file="view_recording.png")
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
        self.x = 10
        self.trccol = 0
        self.scroll = None
        self.btn = None
        self.text = None
        self.inp1 = None
        self.inp2 = None
        self.inp3 = None
        self.tk.protocol("WM_DELETE_WINDOW", self.on_close)
        self.m_player = pn.mouse.Controller()
        self.k_player = pn.keyboard.Controller()
        self.lbl2 = None

    def baseBuild(self):
        self.b1.pack()
        self.b1.place(relx=.5,rely=.25,anchor='center')
        self.b2.pack()
        self.b2.place(relx=.5, rely=.5, anchor='center')
        self.b3.pack()
        self.b3.place(relx=.5, rely=.75, anchor='center')
        self.tk.mainloop()

    def record(self):
        self.file = open('MACRO_INP.txt', 'w')
        if self.mouse_listener.running or self.key_listener.running: #redundant code, fix later
            mb.showwarning(title='[NO]',message='One at a time, please.')
        else:
            self.x = 10
            self.y = -30
            self.top = tk.Toplevel(self.tk,bg='black')
            self.top.protocol("WM_DELETE_WINDOW", self.on_close_key)
            self.top.title('key_tracker')
            self.top.geometry("300x500")
            if not self.key_listener.running:
                self.key_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
                self.key_listener.start()
                print('new_key_list_started')

    def controls(self):
        if self.mouse_listener.running or self.key_listener.running:
            mb.showwarning(title='[SUPER_NO]',message='Please stay on the recording tab.')
        else:
            self.top = tk.Toplevel(self.tk,bg='black')
            self.top.title('controls_view')
            self.top.geometry("300x500")
            self.text = tk.Text(self.top,bg='#00b2ff',fg='#ff008c', bd=5,borderwidth=3,relief='groove',height=25,width=33)
            self.text.pack()
            self.text.place(relx=.05,rely=.05)
            self.file = open('MACRO_INP.txt','r')
            self.text.insert('0.0',str(self.file.read()))
            self.btn = tk.Button(self.top,bg='#ff008c',fg='#00b2ff', bd=5,borderwidth=3,relief='groove',text='Confirm inputs?', command=self.play)
            self.btn.pack()
            self.btn.place(relx=.35,rely=.9)

    def mouse(self):
        self.file = open('MACRO_INP.txt', 'w')
        if self.key_listener.running:
            mb.showwarning(title='[NO]',message='One at a time, please.')
        elif self.mouse_listener.running:
            mb.showwarning(title='[OOPS]',message='Please close the mouse recording by closing the original window.')
        else:
            self.top = tk.Toplevel(self.tk,bg='black')
            self.top.title('mouse_tracker')
            self.top.overrideredirect(True)
            self.top.wm_attributes("-transparentcolor", "black")
            self.top.attributes("-topmost",True)
            self.top.geometry("100x100")
            self.TpLbl = tk.Label(self.top, bg='#ff008c', fg='#00b2ff', bd=5, borderwidth=3, relief='groove',font=24)
            self.TpLbl.pack()
            self.TpLbl.place(relx=.1, rely=.1)
            if self.key_listener.running: #redundant code, fix later
                self.key_listener.stop()
            if not self.mouse_listener.running:
                self.mouse_listener = mouse.Listener(on_move=self.on_move,on_click=self.on_click)
                self.mouse_listener.start()
                print('new_mouse_list_started')

    def on_close(self):
        if self.mouse_listener.running:
            self.mouse_listener.stop()
            self.top.destroy()
        else:
            self.file.flush()
            self.tk.destroy()

    def on_close_key(self):
        if self.key_listener.running:
            mb.showwarning(title='WARNING',message="Please press [ESC] before you close this window to end this recording.")
        else:
            self.file.flush()
            self.top.destroy()

    def on_press(self, key):
        if key == keyboard.Key.esc:
            print('esc_press')
            if self.key_listener.running:
                self.key_listener.stop()
                self.mouse_listener.stop()
                print('Listeners_killed')
                self.file.flush()
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
            self.y = 0
            self.x += 30
        if self.trccol % 2 == 0:
            self.TpLbl = tk.Label(self.top, bg='#ff008c',fg='#00b2ff', bd=5,borderwidth=3,relief='groove')
        else:
            self.TpLbl = tk.Label(self.top, bg='#00b2ff',fg='#ff008c', bd=5,borderwidth=3,relief='groove')
        self.TpLbl.pack()
        self.TpLbl.place(x=self.x, y=self.y)
        self.TpLbl.config(text=self.key)
        self.TpLbl.update()
        print('inputs held : ' + str(self.inp_ct), self.key)
        self.inp_ct = 0
        self.key = []

    def on_move(self,x,y):
        self.mouse_x_y = (x,y)
        self.TpLbl.config(text=self.mouse_x_y)
        self.top.wm_geometry("+%s+%s" % (x,y))
        self.TpLbl.update()

    def on_click(self,x,y,button,pressed):
        self.file.write(str(button) + ' ' + str((x,y)) + '\n')
        if pressed:
            self.TpLbl.config(text='Click!')
        else:
            pass

    def play(self):
        self.file = open('MACRO_INP.txt','w')
        self.file.write(self.text.get("0.0","end-1c"))
        self.file.close()
        self.tk.destroy()
        self.tk = tk.Tk()
        self.tk.configure(bg='black')
        self.tk.title("[HotKey_Set_v2.0001]")
        self.TpLbl = tk.Label(self.tk,bg='#00b2ff',fg='#ff008c', bd=5,borderwidth=3,relief='groove',text='First HotKey:',font=18)
        self.TpLbl.grid(row = 0, column = 0,pady=5,padx=2)
        self.inp1 = tk.Entry(self.tk,bg='#ff008c',fg='#00b2ff',borderwidth=5,relief="groove")
        self.inp1.grid(row=0,column=1,pady=2,padx=2)
        self.lbl2 = tk.Label(self.tk,bg='#00b2ff',fg='#ff008c', bd=5,borderwidth=3,relief='groove',text='Second HotKey:',font=18)
        self.lbl2.grid(row=1,column=0,pady=5,padx=2)
        self.inp2 = tk.Entry(self.tk,bg='#ff008c',fg='#00b2ff',borderwidth=5,relief="groove")
        self.inp2.grid(row=1,column=1,pady=2,padx=2)

test = appTest()
test.baseBuild()