# gui.py

import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import networking
import encryption


class ChatApp(tk.Tk):
    def __init__(self, host, port, key_manager):
        super().__init__()
        self.title("Secure Chat App")
        self.geometry("600x300")

        self.host = host
        self.port = port
        self.key_manager = key_manager

        # Message display area
        self.messages = scrolledtext.ScrolledText(self, state='disabled', height=10)
        self.messages.grid(row=0, column=0, columnspan=2)

        # Text input
        self.input_user = tk.StringVar()
        self.input_field = tk.Entry(self, text=self.input_user)
        self.input_field.grid(row=1, column=0)

        # Send button
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1)

        # Start a thread for the server to listen to incoming messages
        self.server_thread = Thread(target=self.run_server)
        self.server_thread.start()

        self.client_socket = networking.start_client(host, port, self.on_message_received)

    def send_message(self):
        message = self.input_user.get()
        if message:
            # Display the original message
            self.display_message(f"Original Message: {message}", "Sender")

            # Encrypt the message
            encrypted_message = encryption.encrypt_message(message, self.key_manager.key)
            # Display the encrypted message
            self.display_message(f"Encrypted Message: {encrypted_message}", "Sender")

            # Send the encrypted message through the client socket
            self.client_socket.sendall(encrypted_message)

            # Clear the input field
            self.input_user.set('')

    def on_message_received(self, encrypted_message):
        # Decrypt and display message
        decrypted_message = encryption.decrypt_message(encrypted_message, self.key_manager.key)
        # Display the encrypted message
        self.display_message(f"Encrypted Message: {encrypted_message}", "Receiver")
        # Display the decrypted message
        self.display_message(f"Decrypted Message: {decrypted_message}", "Receiver")

    def display_message(self, message, sender):
        self.messages.configure(state='normal')
        self.messages.insert(tk.END, f"{sender}: {message}\n")
        self.messages.configure(state='disabled')

    def run_server(self):
        networking.start_server(self.host, self.port, self.on_message_received)


# Example usage
if __name__ == "__main__":
    from key_management import KeyManager

    key_manager = KeyManager("SecurePassword")
    app = ChatApp("localhost", 12345, key_manager)
    app.mainloop()
