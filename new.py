import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox

# Database connection configuration
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Vishal@123',  # Replace with your MySQL password
            database='education'  # Assuming 'education' database already exists
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

def create_tables(connection):
    queries = [
        """CREATE TABLE IF NOT EXISTS `instructors` (
                `instructor_id` INTEGER PRIMARY KEY AUTO_INCREMENT, 
                `instructor_name` VARCHAR(255) NOT NULL,
                `email` VARCHAR(255),
                `phone` VARCHAR(255),
                `bio` TEXT
            )""",
        """CREATE TABLE IF NOT EXISTS `course` (
                `course_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `course_name` VARCHAR(255) NOT NULL,
                `description` TEXT,
                `credit_hours` INTEGER,
                `instructor_id` INTEGER,
                FOREIGN KEY (`instructor_id`) REFERENCES `instructors` (`instructor_id`) ON DELETE CASCADE
            )""",
        """CREATE TABLE IF NOT EXISTS `students` (
                `student_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `student_name` VARCHAR(255) NOT NULL,
                `email` VARCHAR(255),
                `phone` VARCHAR(255)
            )""",
        """CREATE TABLE IF NOT EXISTS `enrolments` (
                `enrolment_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `course_id` INTEGER,
                `student_id` INTEGER,
                `enrolment_date` DATE,
                `completion_status` ENUM('enrolled', 'completed'),
                FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE CASCADE,
                FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE
            )""",
        """CREATE TABLE IF NOT EXISTS `assessments` (
                `assessment_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `course_id` INTEGER,
                `assessment_name` VARCHAR(255) NOT NULL,
                `max_score` INTEGER,
                `given_by` INTEGER,
                `given_to` INTEGER,
                FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE CASCADE,
                FOREIGN KEY (`given_by`) REFERENCES `instructors` (`instructor_id`) ON DELETE CASCADE,
                FOREIGN KEY (`given_to`) REFERENCES `students` (`student_id`) ON DELETE CASCADE
            )""",
        """CREATE TABLE IF NOT EXISTS `backup_instructors` (
                `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `instructor_id` INTEGER,
                `instructor_name` VARCHAR(255) NOT NULL,
                `email` VARCHAR(255),
                `phone` VARCHAR(255),
                `bio` TEXT,
                `operation` ENUM('DELETE') DEFAULT 'DELETE'
            )""",
        """CREATE TABLE IF NOT EXISTS `backup_course` (
                `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `course_id` INTEGER,
                `course_name` VARCHAR(255) NOT NULL,
                `description` TEXT,
                `credit_hours` INTEGER,
                `instructor_id` INTEGER,
                `operation` ENUM('DELETE') DEFAULT 'DELETE'
            )""",
        """CREATE TABLE IF NOT EXISTS `backup_students` (
                `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `student_id` INTEGER,
                `student_name` VARCHAR(255) NOT NULL,
                `email` VARCHAR(255),
                `phone` VARCHAR(255),
                `operation` ENUM('DELETE') DEFAULT 'DELETE'
            )""",
        """CREATE TABLE IF NOT EXISTS `backup_assessments` (
                `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `assessment_id` INTEGER,
                `course_id` INTEGER,
                `assessment_name` VARCHAR(255) NOT NULL,
                `max_score` INTEGER,
                `given_by` INTEGER,
                `given_to` INTEGER,
                `operation` ENUM('DELETE') DEFAULT 'DELETE'
            )"""
    ]
    try:
        cursor = connection.cursor()
        for query in queries:
            cursor.execute(query)
        connection.commit()
        print("Tables created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: '{err}'")

# Function to insert a new instructor into the database
def insert_instructor(connection, name, email, phone, bio):
    cursor = connection.cursor()
    try:
        query = "INSERT INTO instructors (instructor_name, email, phone, bio) VALUES (%s, %s, %s, %s)"
        values = (name, email, phone, bio)
        cursor.execute(query, values)
        connection.commit()
        print("Instructor inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting instructor: {err}")

# Function to insert a new course into the database
def insert_course(connection, name, description, credit_hours, instructor_id):
    cursor = connection.cursor()
    try:
        query = "INSERT INTO course (course_name, description, credit_hours, instructor_id) VALUES (%s, %s, %s, %s)"
        values = (name, description, credit_hours, instructor_id)
        cursor.execute(query, values)
        connection.commit()
        print("Course inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting course: {err}")

# Function to insert a new student into the database
def insert_student(connection, name, email, phone):
    cursor = connection.cursor()
    try:
        query = "INSERT INTO students (student_name, email, phone) VALUES (%s, %s, %s)"
        values = (name, email, phone)
        cursor.execute(query, values)
        connection.commit()
        print("Student inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting student: {err}")

# Function to delete an instructor from the database
def delete_instructor(connection, instructor_id):
    cursor = connection.cursor()
    try:
        # Retrieve instructor details before deleting
        cursor.execute("SELECT * FROM instructors WHERE instructor_id = %s", (instructor_id,))
        instructor_data = cursor.fetchone()
        
        if instructor_data:
            # Insert into backup table
            query = "INSERT INTO backup_instructors (instructor_id, instructor_name, email, phone, bio) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, instructor_data)
        
        # Delete instructor from main table
        cursor.execute("DELETE FROM instructors WHERE instructor_id = %s", (instructor_id,))
        connection.commit()
        
        print(f"Instructor with ID {instructor_id} deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error deleting instructor: {err}")

# Function to delete a course from the database
def delete_course(connection, course_id):
    cursor = connection.cursor()
    try:
        # Retrieve course details before deleting
        cursor.execute("SELECT * FROM course WHERE course_id = %s", (course_id,))
        course_data = cursor.fetchone()

        if course_data:
            # Insert into backup table
            query = "INSERT INTO backup_course (course_id, course_name, description, credit_hours, instructor_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, course_data)

        # Delete course from main table
        cursor.execute("DELETE FROM course WHERE course_id = %s", (course_id,))
        connection.commit()

        print(f"Course with ID {course_id} deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error deleting course: {err}")

# Function to delete a student from the database
def delete_student(connection, student_id):
    cursor = connection.cursor()
    try:
        # Retrieve student details before deleting
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student_data = cursor.fetchone()

        if student_data:
            # Insert into backup table
            query = "INSERT INTO backup_students (student_id, student_name, email, phone) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, student_data)

        # Delete student from main table
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        connection.commit()

        print(f"Student with ID {student_id} deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error deleting student: {err}")

def view_table(connection, table_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as err:
        print(f"Error viewing {table_name}: {err}")
        return []

# Function to display all deleted items from the backup tables
def display_deleted_items(connection):
    cursor = connection.cursor()
    deleted_items = {}

    try:
        # Retrieve deleted instructors
        cursor.execute("SELECT * FROM backup_instructors")
        deleted_items['instructors'] = cursor.fetchall()

        # Retrieve deleted courses
        cursor.execute("SELECT * FROM backup_course")
        deleted_items['courses'] = cursor.fetchall()

        # Retrieve deleted students
        cursor.execute("SELECT * FROM backup_students")
        deleted_items['students'] = cursor.fetchall()

        return deleted_items
    except mysql.connector.Error as err:
        print(f"Error displaying deleted items: {err}")
        return {}

# Tkinter GUI Application
class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Educational Institution Database")
        self.connection = create_connection()
        create_tables(self.connection)
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)
        
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_student_tab()
        self.create_deleted_tab()

    def create_instructor_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Instructors")

        ttk.Label(tab, text="Instructor Name").grid(row=0, column=0, padx=10, pady=10)
        self.instructor_name_entry = ttk.Entry(tab)
        self.instructor_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(tab, text="Email").grid(row=1, column=0, padx=10, pady=10)
        self.instructor_email_entry = ttk.Entry(tab)
        self.instructor_email_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(tab, text="Phone").grid(row=2, column=0, padx=10, pady=10)
        self.instructor_phone_entry = ttk.Entry(tab)
        self.instructor_phone_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(tab, text="Bio").grid(row=3, column=0, padx=10, pady=10)
        self.instructor_bio_entry = ttk.Entry(tab)
        self.instructor_bio_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Button(tab, text="Add Instructor", command=self.add_instructor).grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Label(tab, text="Instructor ID").grid(row=5, column=0, padx=10, pady=10)
        self.delete_instructor_id_entry = ttk.Entry(tab)
        self.delete_instructor_id_entry.grid(row=5, column=1, padx=10, pady=10)
        
        ttk.Button(tab, text="Delete Instructor", command=self.delete_instructor).grid(row=6, column=0, columnspan=2, pady=10)

    def create_course_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Courses")

        ttk.Label(tab, text="Course Name").grid(row=0, column=0, padx=10, pady=10)
        self.course_name_entry = ttk.Entry(tab)
        self.course_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(tab, text="Description").grid(row=1, column=0, padx=10, pady=10)
        self.course_description_entry = ttk.Entry(tab)
        self.course_description_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(tab, text="Credit Hours").grid(row=2, column=0, padx=10, pady=10)
        self.course_credit_hours_entry = ttk.Entry(tab)
        self.course_credit_hours_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(tab, text="Instructor ID").grid(row=3, column=0, padx=10, pady=10)
        self.course_instructor_id_entry = ttk.Entry(tab)
        self.course_instructor_id_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Button(tab, text="Add Course", command=self.add_course).grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Label(tab, text="Course ID").grid(row=5, column=0, padx=10, pady=10)
        self.delete_course_id_entry = ttk.Entry(tab)
        self.delete_course_id_entry.grid(row=5, column=1, padx=10, pady=10)
        
        ttk.Button(tab, text="Delete Course", command=self.delete_course).grid(row=6, column=0, columnspan=2, pady=10)

    def create_student_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Students")

        ttk.Label(tab, text="Student Name").grid(row=0, column=0, padx=10, pady=10)
        self.student_name_entry = ttk.Entry(tab)
        self.student_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(tab, text="Email").grid(row=1, column=0, padx=10, pady=10)
        self.student_email_entry = ttk.Entry(tab)
        self.student_email_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(tab, text="Phone").grid(row=2, column=0, padx=10, pady=10)
        self.student_phone_entry = ttk.Entry(tab)
        self.student_phone_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(tab, text="Add Student", command=self.add_student).grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Label(tab, text="Student ID").grid(row=4, column=0, padx=10, pady=10)
        self.delete_student_id_entry = ttk.Entry(tab)
        self.delete_student_id_entry.grid(row=4, column=1, padx=10, pady=10)
        
        ttk.Button(tab, text="Delete Student", command=self.delete_student).grid(row=5, column=0, columnspan=2, pady=10)

    def create_deleted_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Deleted Items")

        self.deleted_text = tk.Text(tab, height=15, width=70)
        self.deleted_text.grid(row=0, column=0, padx=10, pady=10)

        ttk.Button(tab, text="Show Deleted Items", command=self.show_deleted_items).grid(row=1, column=0, pady=10)

    def add_instructor(self):
        name = self.instructor_name_entry.get()
        email = self.instructor_email_entry.get()
        phone = self.instructor_phone_entry.get()
        bio = self.instructor_bio_entry.get()
        insert_instructor(self.connection, name, email, phone, bio)

    def add_course(self):
        name = self.course_name_entry.get()
        description = self.course_description_entry.get()
        credit_hours = self.course_credit_hours_entry.get()
        instructor_id = self.course_instructor_id_entry.get()
        insert_course(self.connection, name, description, credit_hours, instructor_id)

    def add_student(self):
        name = self.student_name_entry.get()
        email = self.student_email_entry.get()
        phone = self.student_phone_entry.get()
        insert_student(self.connection, name, email, phone)

    def delete_instructor(self):
        instructor_id = self.delete_instructor_id_entry.get()
        if instructor_id:
            delete_instructor(self.connection, instructor_id)
        else:
            messagebox.showerror("Error", "Please enter Instructor ID")

    def delete_course(self):
        course_id = self.delete_course_id_entry.get()
        if course_id:
            delete_course(self.connection, course_id)
        else:
            messagebox.showerror("Error", "Please enter Course ID")

    def delete_student(self):
        student_id = self.delete_student_id_entry.get()
        if student_id:
            delete_student(self.connection, student_id)
        else:
            messagebox.showerror("Error", "Please enter Student ID")

    def show_deleted_items(self):
        deleted_items = display_deleted_items(self.connection)
        self.deleted_text.delete(1.0, tk.END)
        for category, items in deleted_items.items():
            self.deleted_text.insert(tk.END, f"{category.capitalize()}:\n")
            for item in items:
                self.deleted_text.insert(tk.END, f"{item}\n")
            self.deleted_text.insert(tk.END, "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
