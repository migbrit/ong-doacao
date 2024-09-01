import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class DonationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Doações")
        self.create_widgets()

    def create_widgets(self):
        self.donor_label = tk.Label(self.root, text="Nome do Doador")
        self.donor_label.grid(row=0, column=0, padx=10, pady=5)
        self.donor_entry = tk.Entry(self.root)
        self.donor_entry.grid(row=0, column=1, padx=10, pady=5)

        self.item_label = tk.Label(self.root, text="Item")
        self.item_label.grid(row=1, column=0, padx=10, pady=5)
        self.item_entry = tk.Entry(self.root)
        self.item_entry.grid(row=1, column=1, padx=10, pady=5)

        self.quantity_label = tk.Label(self.root, text="Quantidade")
        self.quantity_label.grid(row=2, column=0, padx=10, pady=5)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=5)

        self.submit_button = tk.Button(self.root, text="Registrar Doação", command=self.submit_donation)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.view_button = tk.Button(self.root, text="Ver Relatórios", command=self.view_reports)
        self.view_button.grid(row=4, column=0, columnspan=2, pady=10)

    def submit_donation(self):
        donor = self.donor_entry.get()
        item = self.item_entry.get()
        quantity = self.quantity_entry.get()
        date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        if not donor or not item or not quantity:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")
            return

        conn = sqlite3.connect('donations.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO donations (donor_name, item, quantity, date)
            VALUES (?, ?, ?, ?)
        ''', (donor, item, quantity, date))
        conn.commit()
        conn.close()

        self.donor_entry.delete(0, tk.END)
        self.item_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

        messagebox.showinfo("Sucesso", "Doação registrada com sucesso!")

    def view_reports(self):
        conn = sqlite3.connect('donations.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM donations')
        rows = cursor.fetchall()
        conn.close()

        report_window = tk.Toplevel(self.root)
        report_window.title("Relatórios de Doações")

        report_text = tk.Text(report_window, width=80, height=20)
        report_text.pack()

        for row in rows:
            report_text.insert(tk.END, f"ID: {row[0]}, Doador: {row[1]}, Item: {row[2]}, Qtd: {row[3]}, Data: {row[4]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = DonationApp(root)
    root.mainloop()
