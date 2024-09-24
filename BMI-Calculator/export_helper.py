import csv
from fpdf import FPDF
import sqlite3
from tkinter import filedialog,messagebox
from db_helper import get_bmi_records


def export_to_csv(user_id):
    records = get_bmi_records(user_id)
    if not records:
        messagebox.showinfo("No Data", "No BMI records found.")
        return

    # Use filedialog to ask the user where to save the CSV file
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    if file_path:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Weight", "Height", "BMI", "Category", "Date"])  # Headers
            for record in records:
                writer.writerow(record)
        messagebox.showinfo("Success", f"Data exported successfully to {file_path}")

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'BMI Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def export_to_pdf(user_id):
    records = get_bmi_records(user_id)

    # Create PDF document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add header
    pdf.cell(15, 10, 'ID', 1)
    pdf.cell(25, 10, 'Weight', 1)
    pdf.cell(25, 10, 'Height', 1)
    pdf.cell(25, 10, 'BMI', 1)
    pdf.cell(40, 10, 'Category', 1)
    pdf.cell(120, 10, 'Timestamp', 1)
    pdf.ln()

    # Add records
    for record in records:
        print(
            f"Debug: Exporting record - ID={record[0]}, Weight={record[2]}, Height={record[3]}, BMI={record[4]}, Category={record[5]}, Timestamp={record[6]}")
        pdf.cell(15, 10, str(record[0]), 1)  # ID
        pdf.cell(25, 10, f"{record[2]:.2f}", 1)  # Weight
        pdf.cell(25, 10, f"{record[3]:.2f}", 1)  # Height
        pdf.cell(25, 10, f"{record[4]:.2f}", 1)  # BMI
        pdf.cell(40, 10, str(record[5]), 1)  # Category
        pdf.cell(120, 10, str(record[6]), 1)  # Timestamp
        pdf.ln()

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf.output(file_path)