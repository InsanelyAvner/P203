import socket
from threading import Thread
from tkinter import *

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")


class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=400)
        self.pls = Label(self.login, text="Please login to continue",
                         justify=CENTER, font="Helvetica 14 bold")
        self.pls.place(relheight=.15, relx=.2, rely=.07)

        self.labelName = Label(self.login, text="Name: ", font="Helvetica 12")
        self.labelName.place(relheight=.2, relx=.1, rely=.2)

        self.entryName = Entry(self.login, font="Helvetica 14")
        self.entryName.place(relwidth=.4, relheight=.12, relx=.35, rely=.2)
        self.entryName.focus()

        self.go = Button(self.login, text="Go", font="Helvetica 14 bold",
                         command=lambda: self.goahead(self.entryName.get()))
        self.go.place(relx=0.4, rely=0.55)

        self.Window.mainloop()


    def layout(self,name):
        self.name=name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,height=False)
        self.Window.configure(width=470,height=550,bg="#ffffff")
        
        self.labelHead = Label(self.Window, text=self.name, 
        font="Helvetica 13 bold",
        bg="#17202A",
        fg="#eaecee",
        pady=5  )
        self.labelHead.place(relwidth=1)
        
        self.line = Label(self.Window, width=450, bg="#ABB2B9")
        self.line.place(relwidth=1, rely=.07, relheight=.012)

        self.textCons=Text(self.Window, width=20, height=2,
        font="Helvetica 14 ",
        bg="#17202A",
        fg="#eaecee",
        pady=5 ,
        padx=5      )

        self.textCons.place(relheight=.745, relwidth=1, rely=.08)

        self.labelBottom=Label(self.Window,bg="#abb2b9",height=80)
        self.labelBottom.place(relwidth=1,rely=.825)

        self.entryMsg=Entry(self.labelBottom,bg="#2c3e50",fg="#eaecee",font="Helveitca 12")
        self.entryMsg.place(relwidth=.74,relheight=.06,rely=.008,relx=.011)
        
        self.entryMsg.focus()

        self.buttonMsg=Button(self.labelBottom, text="Send", font="Helvetica 10 bold",
         width=20,bg = "#ABB2B9",command= lambda:self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=.77, rely=.008, relwidth=.22, relheight=.06)
        self.textCons.config(cursor="arrow")

        scrollbar=Scrollbar(self.textCons)
        scrollbar.place(relheight=1,relx=.974)
        scrollbar.config(command=self.textCons.yview)

    def sendButton(self,msg): 
        self.textCons.config(state=DISABLED)  
        self.msg=msg
        self.entryMsg.delete(0,END)  
        snd=Thread(target=self.write)
        snd.start()


    def show_message(self,message):
        self.textCons.config(state=NORMAL) 
        self.textCons.insert(END,message+"\n\n")  
        self.textCons.config(state=DISABLED)
        self.textCons.see(END) 

    def goahead(self, name):
        self.login.destroy()
        #self.name = name
        self.layout(name)

        rcv = Thread(target=self.receive)
        rcv.start()

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.show_message(message)
            except:
                print("An error occured!")
                client.close()
                break

   

    def write(self):
        self.textCons.config(state=DISABLED)
       
        while True:
            message = (f'{self.name}: {self.msg}')
            client.send(message.encode('utf-8'))
            self.show_message(message)
            break

g = GUI()
