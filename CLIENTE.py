import socket
import threading
import tkinter as tk

SERVER = '192.168.0.193'  
PORT = 12345

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Local")

        self.username_label = tk.Label(root, text="Digite seu nome de usuário:")
        self.username_label.pack()

        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.message_frame = tk.Frame(root)
        self.message_frame.pack()

        self.message_label = tk.Label(self.message_frame, text="Digite sua mensagem:")
        self.message_label.pack(side=tk.LEFT)

        self.message_entry = tk.Entry(self.message_frame)
        self.message_entry.pack(side=tk.LEFT)
        self.message_entry.bind("<Return>", self.send_on_enter)  # Evento Enter

        self.send_button = tk.Button(self.message_frame, text="Enviar", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        self.chat_text = tk.Text(root)
        self.chat_text.pack()

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))

        self.receive_thread = threading.Thread(target=self.receive_message)
        self.receive_thread.start()

    def send_message(self, event=None):  # Adicionamos event=None para permitir chamadas sem eventos
        username = self.username_entry.get()
        message = self.message_entry.get()

        # Adiciona a mensagem no chat do remetente
        self.chat_text.insert(tk.END, f"Você: {message}\n")
        self.chat_text.see(tk.END)  # Rolagem automática para a nova mensagem

        message = f'{len(message)}:{username}:{message}'
        self.client.send(message.encode('utf-8'))
        self.message_entry.delete(0, tk.END)  # Limpa o campo de entrada após o envio

    def receive_message(self):
        while True:
            try:
                msg = self.client.recv(1024).decode('utf-8')
                self.chat_text.insert(tk.END, msg + '\n')
            except Exception as e:
                print(f"[ERRO] Ocorreu um erro: {e}")
                break

    def send_on_enter(self, event):
        self.send_message()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
