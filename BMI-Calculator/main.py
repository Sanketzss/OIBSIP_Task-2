import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import matplotlib.pyplot as plt
from db_helper import init_db, insert_bmi_record, get_bmi_records
from auth import login_user, register_user
from export_helper import export_to_csv, export_to_pdf
from unit_conversion import pounds_to_kg, feet_inches_to_meters

class LoginApp:
    def __init__(self, master):
        self.master = master
        master.title("Login/Register")
        master.geometry("300x200")

        self.label_username = tk.Label(master, text="Username:")
        self.label_username.grid(row=0, column=0, padx=10, pady=10)
        self.entry_username = tk.Entry(master)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)

        self.label_password = tk.Label(master, text="Password:")
        self.label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.button_login = tk.Button(master, text="Login", command=self.login)
        self.button_login.grid(row=2, column=0, padx=10, pady=10)

        self.button_register = tk.Button(master, text="Register", command=self.register)
        self.button_register.grid(row=2, column=1, padx=10, pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        user_id = login_user(username, password)
        if user_id:
            self.master.withdraw()  # Close the login window
            self.open_bmi_calculator(user_id)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if register_user(username, password):
            messagebox.showinfo("Success", "Registration successful. You can now log in.")
        else:
            messagebox.showerror("Error", "Registration failed. Try a different username.")

    def open_bmi_calculator(self, user_id):
        bmi_calculator_window = tk.Toplevel(self.master)
        BMICalculatorApp(bmi_calculator_window, user_id)

class BMICalculatorApp:
    def __init__(self, master, user_id):
        self.user_id = user_id
        self.master = master
        master.title("BMI Calculator")
        master.geometry("400x300")

        self.unit_var = tk.StringVar(value="Metric")
        self.unit_label = tk.Label(master, text="Choose Unit:")
        self.unit_label.grid(row=0, column=0, padx=10, pady=10)
        self.unit_menu = ttk.Combobox(master, textvariable=self.unit_var, values=["Metric", "Imperial"])
        self.unit_menu.grid(row=0, column=1, padx=10, pady=10)
        self.unit_menu.bind("<<ComboboxSelected>>", lambda event: self.convert_units(self.unit_var.get()))

        # Input fields for weight and height
        self.label_weight = tk.Label(master, text="Weight (kg):")
        self.label_weight.grid(row=1, column=0, padx=10, pady=10)
        self.entry_weight = tk.Entry(master)
        self.entry_weight.grid(row=1, column=1, padx=10, pady=10)

        self.label_height = tk.Label(master, text="Height (m):")
        self.label_height.grid(row=2, column=0, padx=10, pady=10)
        self.entry_height = tk.Entry(master)
        self.entry_height.grid(row=2, column=1, padx=10, pady=10)

        # Button for BMI calculation
        self.button_calculate = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi)
        self.button_calculate.grid(row=3, column=0, columnspan=2, pady=10)

        # Label to display results
        self.label_result = tk.Label(master, text="")
        self.label_result.grid(row=4, column=0, columnspan=2, pady=10)

        # Buttons for exporting data and visualizing BMI history
        self.button_export_csv = tk.Button(master, text="Export to CSV", command=lambda: export_to_csv(self.user_id))
        self.button_export_csv.grid(row=5, column=0, pady=10)

        self.button_export_pdf = tk.Button(master, text="Export to PDF", command=lambda: export_to_pdf(self.user_id))
        self.button_export_pdf.grid(row=5, column=1, pady=10)

        self.button_visualize = tk.Button(master, text="Visualize BMI History", command=self.visualize_bmi_history)
        self.button_visualize.grid(row=6, column=0, columnspan=2, pady=10)

    def calculate_bmi(self):
        try:
            # Get the weight and height from the input fields
            weight = float(self.entry_weight.get())
            height = float(self.entry_height.get())

            # Debugging print statement to ensure values are correct
            print(f"Initial weight: {weight}, Initial height: {height}")

            # Convert units if needed (from Imperial to Metric)
            if self.unit_var.get() == "Imperial":
                weight = pounds_to_kg(weight)  # Convert from pounds to kilograms
                height = feet_inches_to_meters(height, 0)  # Assuming feet only, no inches entered

            # Debugging print statement after conversion
            print(f"Converted weight: {weight}, Converted height: {height}")

            # Calculate BMI using the formula: weight (kg) / height (m)^2
            bmi = weight / (height ** 2)
            category = self.get_bmi_category(bmi)

            # Display the result
            self.label_result.config(text=f"BMI: {bmi:.2f} ({category})")

            # Debugging print to ensure correct BMI calculation
            print(f"Calculated BMI: {bmi}, Category: {category}")

            # Save the BMI record
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_bmi_record(self.user_id, weight, height, bmi, category, timestamp)

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
        except ZeroDivisionError:
            messagebox.showerror("Error", "Height cannot be zero.")

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def convert_units(self, unit):
        """Adjust labels based on selected unit."""
        if unit == "Imperial":
            self.label_weight.config(text="Weight (lbs):")
            self.label_height.config(text="Height (ft):")
        else:
            self.label_weight.config(text="Weight (kg):")
            self.label_height.config(text="Height (m):")

    def visualize_bmi_history(self):
        records = get_bmi_records(self.user_id)
        if not records:
            messagebox.showinfo("No Data", "No BMI records found.")
            return

        dates = [record[6] for record in records]
        bmi_values = [record[4] for record in records]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, bmi_values, marker='o')
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.title("BMI History")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()
