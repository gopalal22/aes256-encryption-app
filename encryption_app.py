import os
import base64
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


# ------------------------------
# AES-256 Functions
# ------------------------------

def generate_key():
    key = os.urandom(32)  # 256-bit key
    return base64.b64encode(key).decode()


def encrypt_file(input_file, key_b64):
    key = base64.b64decode(key_b64)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()

    with open(input_file, "rb") as f:
        plaintext = f.read()

    padded_plaintext = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    output_path = input_file + ".enc"

    with open(output_path, "wb") as f:
        f.write(iv + ciphertext)

    return output_path


def decrypt_file(input_file, key_b64):
    key = base64.b64decode(key_b64)

    with open(input_file, "rb") as f:
        data = f.read()

    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    output_path = input_file.replace(".enc", "_decrypted")

    with open(output_path, "wb") as f:
        f.write(plaintext)

    return output_path


# ------------------------------
# GUI Application
# ------------------------------

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AES-256 Encryption Tool")
        self.root.geometry("520x300")
        self.root.resizable(False, False)

        # File selection
        tk.Label(root, text="Selected File:", font=("Arial", 11)).pack(pady=5)
        self.file_entry = tk.Entry(root, width=60)
        self.file_entry.pack()
        tk.Button(root, text="Browse File", command=self.browse_file).pack(pady=5)

        # Key section
        tk.Label(root, text="AES-256 Key:", font=("Arial", 11)).pack()
        self.key_entry = tk.Entry(root, width=60)
        self.key_entry.pack()

        tk.Button(root, text="Generate Key", command=self.generate_key).pack(pady=5)

        # Action buttons
        tk.Button(root, text="Encrypt File", width=20, command=self.encrypt).pack(pady=8)
        tk.Button(root, text="Decrypt File", width=20, command=self.decrypt).pack(pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def generate_key(self):
        key = generate_key()
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, key)
        messagebox.showinfo("Key Generated", "A new AES-256 key has been generated.")

    def encrypt(self):
        file = self.file_entry.get()
        key = self.key_entry.get()

        if not file or not key:
            messagebox.showerror("Error", "Please select a file and enter a key.")
            return

        try:
            output = encrypt_file(file, key)
            messagebox.showinfo("Success", f"File encrypted!\nSaved as:\n{output}")
        except Exception as e:
            messagebox.showerror("Encryption Error", str(e))

    def decrypt(self):
        file = self.file_entry.get()
        key = self.key_entry.get()

        if not file or not key:
            messagebox.showerror("Error", "Please select a file and enter a key.")
            return

        try:
            output = decrypt_file(file, key)
            messagebox.showinfo("Success", f"File decrypted!\nSaved as:\n{output}")
        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))


# ------------------------------
# Run App
# ------------------------------

root = tk.Tk()
app = EncryptionApp(root)
root.mainloop()
