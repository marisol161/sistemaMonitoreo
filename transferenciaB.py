import tkinter as tk
from tkinter import messagebox, filedialog
import time
import datetime
from socket import *
import time
import _thread

LARGE_FONT= ("Verdana", 12)
after_id = None  # Variable para almacenar el identificador del temporizador

def my_server(show_1, HOST, PORT, file_path, file_data):
    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    tcpTimeSrvrSock = socket(AF_INET,SOCK_STREAM)
    tcpTimeSrvrSock.bind(ADDR)
    tcpTimeSrvrSock.listen(5)
    currentDT = datetime.datetime.now()

    while True:
        show_1.insert(tk.END,"waiting for connection...\n")
        tcpTimeClientSock, addr = tcpTimeSrvrSock.accept()

        show_1.insert(tk.END,"connected {}\n".format(addr))

        # Envía el nombre del archivo
        tcpTimeClientSock.send(file_path.encode())

        # Espera un momento antes de enviar los datos del archivo
        time.sleep(0.1)

        # Envía el contenido del archivo
        tcpTimeClientSock.send(file_data)

        # Envía un mensaje de confirmación al cliente
        tcpTimeClientSock.send(b"File sent")

        tcpTimeClientSock.close()

class Page(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        l_title=tk.Label(self, text="Server Software",
                         font="Arial,12")
        l_title.grid(row=0,column=0,columnspan=3, sticky="NSEW",padx=30,pady=30)

        label_username = tk.Label(self, text="Username")
        label_password = tk.Label(self, text="Password")

        entry_username = tk.Entry(self,show="*")

        entry_password = tk.Entry(self, show="*")

        label_username.grid(row=2, column=0, sticky='NSEW',padx=10,pady=10)
        label_password.grid(row=3, column=0, sticky='NSEW',padx=10,pady=10)
        entry_username.grid(row=2, column=1,sticky='NSEW',padx=10,pady=10)
        entry_password.grid(row=3, column=1,sticky='NSEW',padx=10,pady=10)

        checkbox = tk.Checkbutton(self, text="Keep me logged in")
        checkbox.grid(row=4, column=1,sticky='NSEW',padx=10,pady=10)

        logbtn = tk.Button(self, text="Login", bg="BlACK", fg="White",command=lambda: login_btn_clicked())
        logbtn.grid(row=5, column=1,sticky='NSEW', padx=10, pady=10)

        def login_btn_clicked():
            # print("Clicked")
            username = entry_username.get()
            password = entry_password.get()

            if len(username) and len(password) > 2:
                # print(username, password)

                if username == "admin" and password == "admin":
                    controller.show_frame(PageOne)
                # display a ,essage if username and password is incorrect!
                else:
                    messagebox.showinfo("Invalid username or password ! ")

            else:
                messagebox.showinfo("Enter Username and Password")


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        flag = True

        clock = tk.Label(self, font=('times', 18, 'bold'), bg='green',fg="white")
        clock.grid(row=0,column=2, sticky="NSNESWSE",padx=8,pady=8)

        def tick():
            time2=time.strftime('%H:%M:%S')
            clock.config(text=time2)
            clock.after(200,tick)
        tick()

        label = tk.Label(self, text="Server Software ", font="Arial,16",bg="black",fg="White")
        label.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        l_host=tk.Label(self,text="Enter Host NAME")
        l_host.grid(row=1, column=0, padx=8, pady=8, sticky="NSNESWSE")

        e_host=tk.Entry(self)
        e_host.grid(row=1, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        e_host.insert(tk.END,'127.0.0.1')  # Cambio de la dirección IP a localhost

        l_port=tk.Label(self,text="Enter Port")
        l_port.grid(row=2, column=0, padx=8, pady=8, sticky="NSNESWSE")

        e_port=tk.Entry(self)
        e_port.grid(row=2, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        e_port.insert(tk.END,12121)

        message_label=tk.Label(self,text="Client Message",font=("Arial,12"))
        message_label.grid(row=3,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")


        scrollbar_y = tk.Scrollbar(self)
        scrollbar_y.grid(row=4, column=3,rowspan=6)

        show_1=tk.Text(self,height=8, width=35, yscrollcommand=scrollbar_y.set,
                       bg="Grey",fg="White")
        show_1.grid(row=4, column=0,rowspan=3,columnspan=3,sticky="NSEW")

        b_connect=tk.Button(self,text=" Connect",command=lambda: connect())
        b_connect.grid(row=14,column=0,padx=10,pady=10,sticky="nsew")

        b_disconnect=tk.Button(self,text=" disconnect",command=lambda: disconnec())
        b_disconnect.grid(row=14,column=1,padx=10,pady=10,sticky="nsew")


        def runner():
            global after_id
            global secs
            secs += 1
            if secs % 2 == 0:  # every other second
                e_host_v=e_host.get()
                e_port_v=int(e_port.get())

            #after_id = self.after(1000, runner)  # check again in 1 second

        def connect():
            # CONNECT COM PORT
            e_host_v=e_host.get()
            e_port_v=int(e_port.get())

            # Abre un cuadro de diálogo para seleccionar un archivo
            file_path = filedialog.askopenfilename()

            if file_path:
                # Abre y lee el archivo seleccionado
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                # Envía el nombre del archivo y su contenido al cliente
                _thread.start_new_thread(my_server, (show_1, e_host_v, e_port_v, file_path, file_data))
            else:
                show_1.insert(tk.END, "No file selected\n")

        def disconnec():
            global after_id
            if after_id:
                self.after_cancel(after_id)
                after_id = None

app = Page()
app.mainloop()
