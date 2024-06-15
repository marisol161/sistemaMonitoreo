import tkinter as tk
from tkinter import filedialog
import socket
import os

class ClientApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Client")
        self.geometry("400x300")

        self.label = tk.Label(self, text="Client Application", font=("Arial", 14))
        self.label.pack(pady=10)

        self.label_ip = tk.Label(self, text="Server IP:")
        self.label_ip.pack(pady=5)

        self.entry_ip = tk.Entry(self)
        self.entry_ip.pack(pady=5)
        self.entry_ip.insert(tk.END, "127.0.0.1")  # Valor por defecto

        self.label_file = tk.Label(self, text="Selected File:")
        self.label_file.pack(pady=5)

        self.btn_select_file = tk.Button(self, text="Select File", command=self.select_file)
        self.btn_select_file.pack(pady=5)

        self.btn_send_file = tk.Button(self, text="Send File", command=self.send_file)
        self.btn_send_file.pack(pady=5)

        self.btn_receive_file = tk.Button(self, text="Receive File", command=self.receive_file)
        self.btn_receive_file.pack(pady=5)

        self.filename = None

    def select_file(self):
        self.filename = filedialog.askopenfilename()
        if self.filename:
            self.label_file.config(text="Selected File: " + os.path.basename(self.filename))
        else:
            self.label_file.config(text="No file selected")

    def send_file(self):
        if self.filename:
            server_address = (self.entry_ip.get(), 12121)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(server_address)

                # Envía el nombre del archivo al servidor
                filename = os.path.basename(self.filename)
                s.send(filename.encode())

                # Envía el contenido del archivo al servidor
                with open(self.filename, "rb") as file:
                    for data in file:
                        s.send(data)

                self.label.config(text="File sent successfully.")
        else:
            self.label.config(text="No file selected.")

    def receive_file(self):
        server_address = (self.entry_ip.get(), 12121)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(server_address)

            # Solicita el nombre del archivo al servidor
            filename = s.recv(1024).decode()
            if filename:
                # Recibe el contenido del archivo desde el servidor
                save_path = filedialog.asksaveasfilename(initialfile=filename)
                if save_path:
                    # Actualiza la etiqueta del nombre del archivo antes de guardar
                    self.label_file.config(text="Selected File: " + filename)
                    with open(save_path, "wb") as file:
                        while True:
                            data = s.recv(1024)
                            if not data:
                                break
                            file.write(data)
                    self.label.config(text="File received and saved successfully.")
                else:
                    self.label.config(text="File not saved.")
            else:
                self.label.config(text="No file received from server.")

if __name__ == "__main__":
    client_app = ClientApp()
    client_app.mainloop()
