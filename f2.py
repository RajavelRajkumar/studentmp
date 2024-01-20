import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class StudentRegistrationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("A.V.V.M COLLEGE")
        
        # Set GUI size to utilize maximum screen space
        self.root.geometry('{}x{}+0+0'.format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))

        # Create database and tables
        self.create_database()

        # Create GUI
        self.create_main_page()

    def create_database(self):
        self.connection = sqlite3.connect('student_data.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reg_no TEXT,
                name TEXT,
                tamil INTEGER,
                english INTEGER,
                maths INTEGER,
                science INTEGER,
                social_science INTEGER
            )
        ''')

        self.connection.commit()

    def create_main_page(self):
        self.main_frame = tk.Frame(self.root, bg="#000000")
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.btn_student = tk.Button(self.main_frame, text="Student Login", command=self.show_student_login, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.btn_student.grid(row=0, column=0, padx=10, pady=10)

        self.btn_admin = tk.Button(self.main_frame, text="Admin Login", command=self.show_admin_login, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.btn_admin.grid(row=0, column=1, padx=10, pady=10)

    def show_student_login(self):
        # Destroy main frame and create student login GUI
        self.main_frame.destroy()
        self.create_student_login()

    def show_admin_login(self):
        # Destroy main frame and create admin login GUI
        self.main_frame.destroy()
        self.create_admin_login()

    def create_student_login(self):
        self.login_frame = tk.Frame(self.root, bg="#000000")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Add student login components
        # Example: username="student", password="student_password"
        self.label_username = tk.Label(self.login_frame, text="Username:", font=("Arial", 12), bg="#FFD700")
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_username = tk.Entry(self.login_frame, font=("Arial", 12))
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)

        self.label_password = tk.Label(self.login_frame, text="Password:", font=("Arial", 12), bg="#FFD700")
        self.label_password.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_password = tk.Entry(self.login_frame, show="*", font=("Arial", 12))
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.btn_login = tk.Button(self.login_frame, text="Login", command=self.verify_student_login, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=10)

    def verify_student_login(self):
        # For simplicity, consider successful login for any non-empty username and password
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username and password:
            # Destroy login frame and create student search page GUI
            self.login_frame.destroy()
            self.create_student_search_page()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

    def create_student_search_page(self):
        self.search_frame = tk.Frame(self.root, bg="#000000")
        self.search_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.label_reg_no_search = tk.Label(self.search_frame, text="Student Reg No:", font=("Arial", 12), bg="#FFD700")
        self.label_reg_no_search.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_reg_no_search = tk.Entry(self.search_frame, font=("Arial", 12))
        self.entry_reg_no_search.grid(row=0, column=1, padx=10, pady=10)

        self.label_name_search = tk.Label(self.search_frame, text="Student Name:", font=("Arial", 12), bg="#FFD700")
        self.label_name_search.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_name_search = tk.Entry(self.search_frame, font=("Arial", 12))
        self.entry_name_search.grid(row=1, column=1, padx=10, pady=10)

        self.btn_retrieve = tk.Button(self.search_frame, text="Retrieve Data", command=self.retrieve_student_data, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.btn_retrieve.grid(row=2, column=0, columnspan=2, pady=10)

    def retrieve_student_data(self):
        reg_no_search = self.entry_reg_no_search.get()
        name_search = self.entry_name_search.get()

        if not reg_no_search and not name_search:
            messagebox.showerror("Error", "Please enter Reg No or Name for search.")
            return

        self.cursor.execute('''
            SELECT * FROM students WHERE reg_no=? OR name=?
            ''', (reg_no_search, name_search))

        result = self.cursor.fetchall()

        if result:
            self.display_retrieved_data(result)
        else:
            messagebox.showinfo("No Data", "No data found for the given criteria.")

    def display_retrieved_data(self, data):
        display_window = tk.Toplevel(self.root)
        display_window.title("Retrieved Data")

        # Create a treeview (table) to display the data
        tree = ttk.Treeview(display_window)
        tree["columns"] = ("ID", "Reg No", "Name", "Tamil", "English", "Maths", "Science", "Social Science")
        tree.heading("#0", text="Index")
        tree.column("#0", width=50)
        tree.heading("ID", text="ID")
        tree.column("ID", width=50)
        tree.heading("Reg No", text="Reg No")
        tree.column("Reg No", width=100)
        tree.heading("Name", text="Name")
        tree.column("Name", width=150)
        tree.heading("Tamil", text="Tamil")
        tree.column("Tamil", width=80)
        tree.heading("English", text="English")
        tree.column("English", width=80)
        tree.heading("Maths", text="Maths")
        tree.column("Maths", width=80)
        tree.heading("Science", text="Science")
        tree.column("Science", width=80)
        tree.heading("Social Science", text="Social Science")
        tree.column("Social Science", width=100)

        for i, row in enumerate(data):
            tree.insert("", i, values=row)

        tree.pack(expand=True, fill="both")
    def create_admin_login(self):
        self.login_frame = tk.Frame(self.root, bg="#000000")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Add admin login components
        # Example: username="admin", password="admin_password"
        self.label_username = tk.Label(self.login_frame, text="Username:", font=("Arial", 12), bg="#FFD700")
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_username = tk.Entry(self.login_frame, font=("Arial", 12))
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)

        self.label_password = tk.Label(self.login_frame, text="Password:", font=("Arial", 12), bg="#FFD700")
        self.label_password.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_password = tk.Entry(self.login_frame, show="*", font=("Arial", 12))
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.btn_login = tk.Button(self.login_frame, text="Login", command=self.verify_admin_login, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=10)

    def verify_admin_login(self):
        # For simplicity, consider successful login for any non-empty username and password
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "admin":
            # Destroy login frame and create admin GUI
            self.login_frame.destroy()
            self.create_admin_gui()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

    def create_admin_gui(self):
        self.admin_frame = tk.Frame(self.root, bg="#000000")
        self.admin_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Add admin GUI components
        # You can use similar code as the one used in the student GUI
        # Add entry widgets for ID, Reg No, Name, Marklist, etc.
        # Add buttons for updating, clearing, submitting, and deleting data
        # Also, add entry widgets for searching data

        # Example components:
        self.label_id = tk.Label(self.admin_frame, text="Student ID:", font=("Arial", 12), bg="#FFD700")
        self.label_id.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_id = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.entry_id.grid(row=0, column=1, padx=10, pady=10)

        self.label_reg_no = tk.Label(self.admin_frame, text="Student Reg No:", font=("Arial", 12), bg="#FFD700")
        self.label_reg_no.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_reg_no = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.entry_reg_no.grid(row=1, column=1, padx=10, pady=10)

        self.label_name = tk.Label(self.admin_frame, text="Student Name:", font=("Arial", 12), bg="#FFD700")
        self.label_name.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.entry_name = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.entry_name.grid(row=2, column=1, padx=10, pady=10)

        self.label_marklist = tk.Label(self.admin_frame, text="Marklist", font=("Arial", 16, "bold"), bg="#FFD700")
        self.label_marklist.grid(row=3, column=0, columnspan=2, pady=10)

        self.label_tamil = tk.Label(self.admin_frame, text="Tamil:", font=("Arial", 12), bg="#FFD700")
        self.label_tamil.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.entry_tamil = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.entry_tamil.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.label_english = tk.Label(self.admin_frame, text="English:", font=("Arial", 12), bg="#FFD700")
        self.label_english.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.entry_english = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.entry_english.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        self.label_maths = tk.Label(self.admin_frame, text="Maths:", font=("Arial", 12), bg="#FFD700")
        self.label_maths.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        self.entry_maths = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.entry_maths.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        self.label_science = tk.Label(self.admin_frame, text="Science:", font=("Arial", 12), bg="#FFD700")
        self.label_science.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        self.entry_science = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.entry_science.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        self.label_social_science = tk.Label(self.admin_frame, text="Social Science:", font=("Arial", 12), bg="#FFD700")
        self.label_social_science.grid(row=8, column=0, padx=10, pady=5, sticky="w")

        self.entry_social_science = tk.Entry(self.admin_frame, font=("Arial", 12))
        self.entry_social_science.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        self.btn_calculate = tk.Button(self.admin_frame, text="Calculate Grades", command=self.calculate_grades, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.btn_calculate.grid(row=9, column=0, columnspan=4, pady=10)

        self.label_total = tk.Label(self.admin_frame, text="Total Marks:", font=("Arial", 12), bg="#FFD700")
        self.label_total.grid(row=10, column=0, padx=10, pady=10, sticky="w")

        self.label_total_value = tk.Label(self.admin_frame, text="", font=("Arial", 12, "bold"))
        self.label_total_value.grid(row=10, column=1, padx=10, pady=10)

        self.label_grade = tk.Label(self.admin_frame, text="Grade:", font=("Arial", 12), bg="#FFD700")
        self.label_grade.grid(row=11, column=0, padx=10, pady=10, sticky="w")

        self.label_grade_value = tk.Label(self.admin_frame, text="", font=("Arial", 12, "bold"))
        self.label_grade_value.grid(row=11, column=1, padx=10, pady=10)

        

        self.btn_submit = tk.Button(self.admin_frame, text="Submit", command=self.submit_data, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.btn_submit.grid(row=12, column=1, pady=10)

        self.btn_clear = tk.Button(self.admin_frame, text="Clear", command=self.clear_fields, bg="#FF0000", fg="white", font=("Arial", 12))
        self.btn_clear.grid(row=13, column=0, columnspan=2, pady=10)

    def calculate_grades(self):
        try:
            tamil = int(self.entry_tamil.get())
            english = int(self.entry_english.get())
            maths = int(self.entry_maths.get())
            science = int(self.entry_science.get())
            social_science = int(self.entry_social_science.get())

            total_marks = tamil + english + maths + science + social_science
            self.label_total_value.config(text=str(total_marks))

            average_marks = total_marks / 5

            if average_marks >= 90:
                grade = "O"
            elif average_marks >= 80:
                grade = "A"
            elif average_marks >= 70:
                grade = "B"
            elif average_marks >= 60:
                grade = "C"
            elif average_marks >= 50:
                grade = "D"
            else:
                grade = "Fail"

            self.label_grade_value.config(text=grade)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid marks for all subjects.")

    

    def submit_data(self):
        try:
            student_name = self.entry_name.get()
            reg_no = self.entry_reg_no.get()

            if not student_name:
                messagebox.showerror("Error", "Please enter student name.")
                return

            tamil = int(self.entry_tamil.get())
            english = int(self.entry_english.get())
            maths = int(self.entry_maths.get())
            science = int(self.entry_science.get())
            social_science = int(self.entry_social_science.get())

            total_marks = tamil + english + maths + science + social_science

            self.cursor.execute('''
                INSERT INTO students (reg_no, name, tamil, english, maths, science, social_science)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (reg_no, student_name, tamil, english, maths, science, social_science))

            self.connection.commit()

            messagebox.showinfo("Success", "Data saved successfully.")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid marks for all subjects.")

    def clear_fields(self):
        self.entry_id.delete(0, tk.END)
        self.entry_reg_no.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_tamil.delete(0, tk.END)
        self.entry_english.delete(0, tk.END)
        self.entry_maths.delete(0, tk.END)
        self.entry_science.delete(0, tk.END)
        self.entry_social_science.delete(0, tk.END)
        self.label_total_value.config(text="")
        self.label_grade_value.config(text="")

    def run(self):
        self.root.mainloop()

# Main driver code
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRegistrationSystem(root)
    root.mainloop()

