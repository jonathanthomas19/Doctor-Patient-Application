import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry

current_doctor_id = None
current_patient_id = None

def clear_entry_fields():
    doctor_username_entry.delete(0, "end")
    doctor_password_entry.delete(0, "end")
    patient_username_entry.delete(0, "end")
    patient_password_entry.delete(0, "end")
    
def doctor_login():
    global current_doctor_id
    username = doctor_username_entry.get()
    password = doctor_password_entry.get()
    conn = sqlite3.connect('medical_app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctor_credentials WHERE username = ? AND password = ?", (username, password))
    doctor = cursor.fetchone()
    conn.close()
    if doctor:
        current_doctor_id = doctor[0]
        clear_entry_fields()
        open_doctor_app()
    else:
        messagebox.showerror("Login Error", "Invalid credentials for doctor.")
        clear_entry_fields()

def patient_login():
    global current_patient_id
    username = patient_username_entry.get()
    password = patient_password_entry.get()
    conn = sqlite3.connect('medical_app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient_credentials WHERE username = ? AND password = ?", (username, password))
    patient = cursor.fetchone()
    conn.close()
    if patient:
        current_patient_id = patient[0]
        clear_entry_fields()
        open_patient_app()
    else:
        messagebox.showerror("Login Error", "Invalid credentials for patient.")
        clear_entry_fields()

def open_doctor_app():
    doctor_window = tk.Toplevel(root)
    doctor_window.title("Doctor Application")
    doctor_window.geometry("800x600")
    notebook = ttk.Notebook(doctor_window)
    notebook.pack(fill="both", expand=True)

    def add_patient():
        name = add_name_entry.get()
        dob = add_dob_entry.get_date().strftime('%Y-%m-%d')
        gender = add_gender_var.get()
        doctor_id = add_doctorid_entry.get()
        try:
            conn = sqlite3.connect('medical_app.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO patients (name, dob, gender, doctor_id) VALUES (?, ?, ?, ?)", (name, dob, gender, doctor_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Patient details added successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))
        
    def view_patients():
        if current_doctor_id is not None:
            view_window = tk.Toplevel(root)
            view_window.title("View Patients")
            view_window.configure(bg="lightgray")
            try:
                conn = sqlite3.connect('medical_app.db')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM patients WHERE doctor_id=?", (current_doctor_id,))
                patients = cursor.fetchall()
                text_widget = tk.Text(view_window)
                text_widget.config(borderwidth=1, relief="solid")
                text_widget.pack()
                for patient in patients:
                    text_widget.insert(tk.END, f"Patient ID: {patient[0]}\n")
                    text_widget.insert(tk.END, f"Name: {patient[1]}\n")
                    text_widget.insert(tk.END, f"Age: {patient[2]}\n")
                    text_widget.insert(tk.END, f"Gender: {patient[3]}\n")
                    text_widget.insert(tk.END, f"Doctor ID: {patient[4]}\n")
                    text_widget.insert(tk.END, "\n")
                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "No doctor is currently logged in.")

    
    def search_patients():
        search_term = search_entry.get()
        conn = sqlite3.connect('medical_app.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM patients WHERE name LIKE ? OR patient_id = ? AND doctor_id = ?", ('%' + search_term + '%', search_term, current_doctor_id))
            patients = cursor.fetchall()
            if patients:
                search_results_window = tk.Toplevel(root)
                search_results_window.title("Search Results")
                text_widget = tk.Text(search_results_window)
                text_widget.pack()
                for patient in patients:
                    text_widget.insert(tk.END, f"Patient ID: {patient[0]}\n")
                    text_widget.insert(tk.END, f"Name: {patient[1]}\n")
                    text_widget.insert(tk.END, f"Age: {patient[2]}\n")
                    text_widget.insert(tk.END, f"Gender: {patient[3]}\n")
                    text_widget.insert(tk.END, f"Doctor ID: {patient[4]}\n")
                    text_widget.insert(tk.END, "\n")
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()
    
    def update_patient():
        try:
            patient_id = new_patient_id_entry.get()
            new_name = new_name_entry.get()
            new_dob = new_dob_entry.get_date().strftime('%Y-%m-%d')
            new_gender = new_gender_var.get()
            try:
                new_doctor_id = int(new_doctor_id_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid doctor ID. Please enter valid ID.")
            conn = sqlite3.connect('medical_app.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE patients SET name=?, dob=?, gender=?, doctor_id=? WHERE patient_id=?", (new_name, new_dob, new_gender, new_doctor_id, patient_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Patient details updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid patient ID or doctor ID. Please enter valid IDs.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))


    def view_doctors():
        conn = sqlite3.connect('medical_app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()
        text_widget = tk.Text(view_doctor)
        text_widget.pack()
        for doctor in doctors:
            text_widget.insert(tk.END, f"Doctor ID: {doctor[0]}\n")
            text_widget.insert(tk.END, f"Name: {doctor[1]}\n")
            text_widget.insert(tk.END, f"Specialization: {doctor[2]}\n")
            text_widget.insert(tk.END, "\n")
        conn.close()
    
    def submit_report():
        conn = sqlite3.connect('medical_app.db')
        cursor = conn.cursor()
        patient_id = patient_id_entry.get()
        doctor_id = doctor_id_entry.get()
        patient_name = patient_name_entry.get()
        report_date = report_date_entry.get()
        blood_pressure = blood_pressure_entry.get()
        pulse_rate = pulse_rate_entry.get()
        respiratory_rate = respiratory_rate_entry.get()
        body_temperature = body_temperature_entry.get()                                                                                                                                                                                                                                                                                         
        oxygen_saturation = oxygen_saturation_entry.get()
        head_exam = head_exam_entry.get("1.0", tk.END)
        chest_exam = chest_exam_entry.get("1.0", tk.END)
        abdominal_exam = abdominal_exam_entry.get("1.0", tk.END)
        extremities_exam = extremities_exam_entry.get("1.0", tk.END)
        assessment = assessment_text.get("1.0", tk.END)
        diagnosis = diagnosis_entry.get("1.0", tk.END)
        cursor.execute("INSERT INTO doctor_reports (patient_id, doctor_id, patient_name, report_date, blood_pressure, pulse_rate, respiratory_rate, body_temperature, oxygen_saturation, head_exam, chest_exam, abdominal_exam, extremities_exam, assessment, diagnosis) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (patient_id, doctor_id, patient_name, report_date, blood_pressure, pulse_rate, respiratory_rate, body_temperature, oxygen_saturation, head_exam, chest_exam, abdominal_exam, extremities_exam, assessment, diagnosis))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Patient Report submitted successfully!")
        patient_name_entry.delete(0, tk.END)
        doctor_id_entry.delete(0, tk.END)
        report_date_entry.delete(0, tk.END)
        blood_pressure_entry.delete(0, tk.END)
        pulse_rate_entry.delete(0, tk.END)
        respiratory_rate_entry.delete(0, tk.END)
        body_temperature_entry.delete(0, tk.END)
        oxygen_saturation_entry.delete(0, tk.END)
        head_exam_entry.delete("1.0", tk.END)
        chest_exam_entry.delete("1.0", tk.END)
        abdominal_exam_entry.delete("1.0", tk.END)
        extremities_exam_entry.delete("1.0", tk.END)
        assessment_text.delete("1.0", tk.END)
        diagnosis_entry.delete("1.0", tk.END)
    
    def search_patients():
        patient_id = report_search_entry.get()
        conn = sqlite3.connect('medical_app.db')
        cursor = conn.cursor()
        db_file = 'medical_app.db'
        try:
            cursor.execute("SELECT * FROM doctor_reports WHERE patient_id = ? AND doctor_id = ?", (patient_id, current_doctor_id))
            doctor_reports = cursor.fetchall()
            if not doctor_reports:
                report_text.set("No reports found for Patient ID: " + str(patient_id))
                return
            report_text.set("Patient Reports for Patient ID " + str(patient_id) + ":\n\n")
            for index, report in enumerate(doctor_reports, start=1):
                report_text.set(report_text.get() +
                f"Report ID: {report[0]}\n"
                f"Patient ID: {report[1]}\n"
                f"Patient Name: {report[2]}\n"
                f"Doctor ID: {report[3]}\n"
                f"Report Date: {report[4]}\n"
                f"Blood Pressure: {report[5]}\n"
                f"Pulse Rate: {report[6]}\n"
                f"Respiratory Rate: {report[7]}\n"
                f"Body Temperature: {report[8]}\n"
                f"Oxygen Saturation: {report[9]}\n"
                f"Head Exam:\n{report[10]}\n"
                f"Chest Exam:\n{report[11]}\n"
                f"Abdominal Exam:\n{report[12]}\n"
                f"Extremities Exam:\n{report[13]}\n"
                f"Assessment:\n{report[14]}\n"
               f"Diagnosis:\n{report[15]}\n\n")
        except sqlite3.Error as e:
            print("SQLite error:", e)
            return []
        finally:
            conn.close()
    

    # Tab 1: Add Patient
    add_patient_frame = ttk.Frame(notebook)
    notebook.add(add_patient_frame, text="Add Patient")
    entry_style = {"width": 22, "font": font_style}
    label_style = {"font": font_style}
    add_name_label = tk.Label(add_patient_frame, text="Name:", **label_style)
    add_name_label.grid(row=0, column=0, padx=10, pady=5)
    add_name_entry = tk.Entry(add_patient_frame, **entry_style)
    add_name_entry.grid(row=0, column=1, padx=10, pady=5)
    add_dob_label = tk.Label(add_patient_frame, text="DOB:", **label_style)
    add_dob_label.grid(row=1, column=0, padx=10, pady=5)
    add_dob_entry = DateEntry(add_patient_frame, background="darkblue", foreground="white", width = 21, font = font_style)
    add_dob_entry.grid(row=1, column=1, padx=10, pady=5)
    add_gender_label = tk.Label(add_patient_frame, text="Gender:", **label_style)
    add_gender_label.grid(row=2, column=0, padx=10, pady=5)
    add_gender_var = tk.StringVar()
    add_gender_var.set("Male")
    add_gender_combobox = ttk.Combobox(add_patient_frame, textvariable=add_gender_var, values=["Male", "Female", "Other"], state="readonly", width = 21, font =  font_style)
    add_gender_combobox.grid(row=2, column=1, padx=10, pady=5)
    add_doctorid_label = tk.Label(add_patient_frame, text="Doctor ID:", **label_style)
    add_doctorid_label.grid(row=3, column=0, padx=10, pady=5)
    add_doctorid_entry = tk.Entry(add_patient_frame, **entry_style)
    add_doctorid_entry.grid(row=3, column=1, padx=10, pady=5)
    add_button = tk.Button(add_patient_frame, text="Add Patient", command=add_patient, bg="blue", fg="white", font=font_style)
    add_button.grid(row=4, columnspan=2, padx=10, pady=10)
    
    # Tab 2: Search Patient
    search_patient = ttk.Frame(notebook)
    notebook.add(search_patient, text="Search Patients")
    search_label = tk.Label(search_patient, text="Search:", font=font_style)
    search_label.grid(row=0, column=0)
    search_entry = tk.Entry(search_patient, width=22, font=font_style)
    search_entry.grid(row=0, column=1)
    search_button = tk.Button(search_patient, text="Search", command=search_patients, bg="blue", fg="white", font=font_style)
    search_button.grid(row=0, column=2)
    
    # Tab 3: Update Patient
    update_patient_frame = ttk.Frame(notebook)
    notebook.add(update_patient_frame, text="Update Patient")
    new_patient_id_label = tk.Label(update_patient_frame, text="Patient ID:", **label_style)
    new_patient_id_label.grid(row=0, column=0, padx=10, pady=5)
    new_patient_id_entry = tk.Entry(update_patient_frame, **entry_style)
    new_patient_id_entry.grid(row=0, column=1, padx=10, pady=5)
    new_name_label = tk.Label(update_patient_frame, text="Name:", **label_style)
    new_name_label.grid(row=0, column=3, padx=10, pady=5)
    new_name_entry = tk.Entry(update_patient_frame, **entry_style)
    new_name_entry.grid(row=0, column=4, padx=10, pady=5)
    new_dob_label = tk.Label(update_patient_frame, text="DOB:", **label_style)
    new_dob_label.grid(row=1, column=0, padx=10, pady=5)
    new_dob_entry = DateEntry(update_patient_frame, background="darkblue", foreground="white", width = 21, font = font_style)
    new_dob_entry.grid(row=1, column=1, padx=10, pady=5)
    new_gender_label = tk.Label(update_patient_frame, text="Gender:", **label_style)
    new_gender_label.grid(row=1, column=3, padx=10, pady=5)
    new_gender_var = tk.StringVar()
    new_gender_var.set("Male")
    new_gender_combobox = ttk.Combobox(update_patient_frame, textvariable=new_gender_var, values=["Male", "Female", "Other"], state="readonly", width = 21, font = font_style)
    new_gender_combobox.grid(row=1, column=4, padx=10, pady=5)
    new_doctor_id_label = tk.Label(update_patient_frame, text="Doctor ID:", **label_style)
    new_doctor_id_label.grid(row=2, column=0, padx=10, pady=5)
    new_doctor_id_entry = tk.Entry(update_patient_frame, **entry_style)
    new_doctor_id_entry.grid(row=2, column=1, padx=10, pady=5)
    update_button = tk.Button(update_patient_frame, text="Update Patient", command=update_patient, bg="blue", fg="white", font=font_style)
    update_button.grid(row=4, column=4, padx=10, pady=10)

    # Tab 4: View Doctors
    view_doctor = tk.Frame(notebook)
    notebook.add(view_doctor, text="View Doctor")        
    view_doctors_button = tk.Button(view_doctor, text="View Doctors", command=view_doctors, bg="blue", fg="white", font=font_style)
    view_doctors_button.pack()

    # Tab 5: Add Patient Report
    report_doctors = ttk.Frame(notebook)
    notebook.add(report_doctors, text="Add Patient Report")
    patient_id_label = tk.Label(report_doctors, text="Patient ID:", font=font_style)
    patient_id_label.grid(row=0, column=0, padx=10, pady=5)
    patient_id_entry = tk.Entry(report_doctors, width=22, font=font_style)
    patient_id_entry.grid(row=0, column=1, padx=10, pady=5)
    doctor_id_label = tk.Label(report_doctors, text="Doctor ID:", font=font_style)
    doctor_id_label.grid(row=0, column=2, padx=10, pady=5)
    doctor_id_entry = tk.Entry(report_doctors, width=22, font=font_style)
    doctor_id_entry.grid(row=0, column=3, padx=10, pady=5)
    patient_name_label = tk.Label(report_doctors, text="Patient Name:", font=font_style)
    patient_name_label.grid(row=0, column=4, padx=10, pady=5)
    patient_name_entry = tk.Entry(report_doctors, width=22, font=font_style)
    patient_name_entry.grid(row=0, column=5, padx=10, pady=5)
    report_date_label = tk.Label(report_doctors, text="Report Date:", font=font_style)
    report_date_label.grid(row=1, column=0, padx=10, pady=5)
    report_date_entry = tk.Entry(report_doctors, width=22, font=font_style)
    report_date_entry.grid(row=1, column=1, padx=10, pady=5)
    blood_pressure_label = tk.Label(report_doctors, text="Blood Pressure:", font=font_style)
    blood_pressure_label.grid(row=1, column=2, padx=10, pady=5)
    blood_pressure_entry = tk.Entry(report_doctors, width=22, font=font_style)
    blood_pressure_entry.grid(row=1, column=3, padx=10, pady=5)
    pulse_rate_label = tk.Label(report_doctors, text="Pulse Rate:", font=font_style)
    pulse_rate_label.grid(row=1, column=4, padx=10, pady=5)
    pulse_rate_entry = tk.Entry(report_doctors, width=22, font=font_style)
    pulse_rate_entry.grid(row=1, column=5, padx=10, pady=5)
    respiratory_rate_label = tk.Label(report_doctors, text="Respiratory Rate:", font=font_style)
    respiratory_rate_label.grid(row=2, column=0, padx=10, pady=5)
    respiratory_rate_entry = tk.Entry(report_doctors, width=22, font=font_style)
    respiratory_rate_entry.grid(row=2, column=1, padx=10, pady=5)
    body_temperature_label = tk.Label(report_doctors, text="Body Temperature:", font=font_style)
    body_temperature_label.grid(row=2, column=2, padx=10, pady=5)
    body_temperature_entry = tk.Entry(report_doctors, width=22, font=font_style)
    body_temperature_entry.grid(row=2, column=3, padx=10, pady=5)
    oxygen_saturation_label = tk.Label(report_doctors, text="Oxygen Saturation:", font=font_style)
    oxygen_saturation_label.grid(row=2, column=4, padx=10, pady=5)
    oxygen_saturation_entry = tk.Entry(report_doctors, width=22, font=font_style)
    oxygen_saturation_entry.grid(row=2, column=5, padx=10, pady=5)
    head_exam_label = tk.Label(report_doctors, text="Head Exam:", font=font_style)
    head_exam_label.grid(row=3, column=0, padx=10, pady=5)
    head_exam_entry = tk.Text(report_doctors, height=4, width=30)
    head_exam_entry.grid(row=3, column=1, padx=10, pady=5)
    chest_exam_label = tk.Label(report_doctors, text="Chest Exam:", font=font_style)
    chest_exam_label.grid(row=3, column=2, padx=10, pady=5)
    chest_exam_entry = tk.Text(report_doctors, height=4, width=30)
    chest_exam_entry.grid(row=3, column=3, padx=10, pady=5)
    abdominal_exam_label = tk.Label(report_doctors, text="Abdominal Exam:", font=font_style)
    abdominal_exam_label.grid(row=3, column=4, padx=10, pady=5)
    abdominal_exam_entry = tk.Text(report_doctors, height=4, width=30)
    abdominal_exam_entry.grid(row=3, column=5, padx=10, pady=5)
    extremities_exam_label = tk.Label(report_doctors, text="Extremities Exam:", font=font_style)
    extremities_exam_label.grid(row=4, column=0, padx=10, pady=5)
    extremities_exam_entry = tk.Text(report_doctors, height=4, width=30)
    extremities_exam_entry.grid(row=4, column=1, padx=10, pady=5)
    assessment_text_label = tk.Label(report_doctors, text="Assessment:", font=font_style)
    assessment_text_label.grid(row=4, column=2, padx=10, pady=5)
    assessment_text = tk.Text(report_doctors, height=4, width=30)
    assessment_text.grid(row=4, column=3, padx=10, pady=5)
    diagnosis_entry_label = tk.Label(report_doctors, text="Diagnosis:", font=font_style)
    diagnosis_entry_label.grid(row=4, column=4, padx=10, pady=5)
    diagnosis_entry = tk.Text(report_doctors, height=4, width=30)
    diagnosis_entry.grid(row=4, column=5, padx=10, pady=5)
    submit_button = tk.Button(report_doctors, text="Submit Report", command=submit_report, bg="blue", fg="white", font=font_style)
    submit_button.grid(row=7, column=3, padx=10, pady=10)

    #Tab 6: View Patient Reports
    generate_report = ttk.Frame(notebook)
    notebook.add(generate_report, text="View Patient Reports")
    report_search_label = tk.Label(generate_report, text="Search:", font=font_style)
    report_search_label.pack()
    report_search_entry = tk.Entry(generate_report, width=22, font=font_style)
    report_search_entry.pack()
    report_search_button = tk.Button(generate_report, text="View Report", command=search_patients, bg="blue", fg="white", font=font_style)
    report_search_button.pack()
    report_text = tk.StringVar()
    report_label = tk.Label(generate_report, textvariable=report_text, justify=tk.LEFT)
    report_label.pack()

def open_patient_app():
    patient_window = tk.Toplevel(root)
    patient_window.title("Patient Application")
    patient_window.geometry("800x600")
    notebook = ttk.Notebook(patient_window)
    notebook.pack(fill="both", expand=True)

    def display_patient_details():
        patient_id = current_patient_id
        db_file = 'medical_app.db'
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
            patient = cursor.fetchone()
            if patient:
                dob = datetime.strptime(patient[2], '%Y-%m-%d').date()
                age = (datetime.now().date() - dob).days // 365
                patient_details_text.config(state='normal')
                patient_details_text.delete('1.0', 'end')
                patient_details_text.insert('1.0',
                                            f"Patient ID: {patient[0]}\n"
                                            f"Name: {patient[1]}\n"
                                            f"Date of Birth: {dob}\n"
                                            f"Age: {age} years\n"
                                            f"Gender: {patient[3]}\n"
                                            f"Doctor ID: {patient[4]}\n")
                patient_details_text.config(state='disabled')
            else:
                patient_details_text.config(state='normal')
                patient_details_text.delete('1.0', 'end')
                patient_details_text.insert('1.0', "Patient details not found.")
                patient_details_text.config(state='disabled')
            conn.close()
        except sqlite3.Error as e:
            patient_details_text.config(state='normal')
            patient_details_text.delete('1.0', 'end')
            patient_details_text.insert('1.0', "An error occurred while fetching patient details.")
            patient_details_text.config(state='disabled')
            print("SQLite error:", e)

    def view_doctors():
        conn = sqlite3.connect('medical_app.db')
        cursor = conn.cursor()
        specialization = specialization_entry.get()
        cursor.execute("SELECT * FROM doctors WHERE specialization LIKE ? OR doctor_id = ?", ('%' + specialization + '%',specialization,))
        doctors = cursor.fetchall()
        search_results_window = tk.Toplevel(root)
        search_results_window.title("Search Results")
        text_widget = tk.Text(search_results_window)
        text_widget.pack()
        for doctor in doctors:
            text_widget.insert(tk.END, f"Doctor ID: {doctor[0]}\n")
            text_widget.insert(tk.END, f"Name: {doctor[1]}\n")
            text_widget.insert(tk.END, f"Specialization: {doctor[2]}\n")
            text_widget.insert(tk.END, "\n")
        conn.close()
    
    def retrieve_doctor_reports(db_file, current_patient_id):
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doctor_reports WHERE patient_id=?", (current_patient_id,))
            reports = cursor.fetchall()
            conn.close()
            return reports
        except sqlite3.Error as e:
            print("SQLite error:", e)
            return []
    
    def display_reports():
        patient_id = current_patient_id
        db_file = 'medical_app.db'
        doctor_reports = retrieve_doctor_reports(db_file, patient_id)
        if not doctor_reports:
            report_text.set("No reports found for Patient ID: " + str(patient_id))
            return
        report_text.set("Patient Reports for Patient ID " + str(patient_id) + ":\n\n")
        for index, report in enumerate(doctor_reports, start=1):
            report_text.set(report_text.get() +
                            f"Report ID: {report[0]}\n"
                            f"Patient ID: {report[1]}\n"
                            f"Patient Name: {report[2]}\n"
                            f"Doctor ID: {report[3]}\n"
                            f"Report Date: {report[4]}\n"
                            f"Blood Pressure: {report[5]}\n"
                            f"Pulse Rate: {report[6]}\n"
                            f"Respiratory Rate: {report[7]}\n"
                            f"Body Temperature: {report[8]}\n"
                            f"Oxygen Saturation: {report[9]}\n"
                            f"Head Exam:\n{report[10]}\n"
                            f"Chest Exam:\n{report[11]}\n"
                            f"Abdominal Exam:\n{report[12]}\n"
                            f"Extremities Exam:\n{report[13]}\n"
                            f"Assessment:\n{report[14]}\n"
                            f"Diagnosis:\n{report[15]}\n\n")
    
    patient_details = tk.Frame(notebook, bg="#f5f5f5")
    notebook.add(patient_details, text="Your Info") 
    patient_details_text = tk.Text(patient_details, height=10, width=40)
    patient_details_text.pack(pady=20)
    patient_details_text.config(state='disabled')
    notebook.bind("<<NotebookTabChanged>>", lambda event: display_patient_details())
    display_details_button = tk.Button(patient_details, text="Refresh Details", command=display_patient_details, bg="blue", fg="white", font=font_style)
    display_details_button.pack()
    
    view_doctor = tk.Frame(notebook)
    notebook.add(view_doctor, text="View Doctor")
    specialization_label = tk.Label(view_doctor, text = "Search:", justify=tk.LEFT,font=font_style)
    specialization_label.pack()
    specialization_entry = tk.Entry(view_doctor, width=22, font=font_style)
    specialization_entry.pack()
    view_doctors_button = tk.Button(view_doctor, text="Search Doctors", command=view_doctors, bg="blue", fg="white", font=font_style)
    view_doctors_button.pack()
    
    generate_report = ttk.Frame(notebook)
    notebook.add(generate_report, text="Generate Report")
    report_text = tk.StringVar()
    report_label = tk.Label(generate_report, textvariable=report_text, justify=tk.LEFT)
    report_label.pack()
    retrieve_button = tk.Button(generate_report, text="Retrieve Reports", command=display_reports, bg="blue", fg="white", font=font_style)
    retrieve_button.pack()

root = tk.Tk()
root.title("Login Page")
root.geometry("800x600")

style = ttk.Style()
style.configure("TNotebook", background="#D3D3D3")
style.configure("TNotebook.Tab", font=("Helvetica", 12), padding=[10, 5])
root.rowconfigure(5, minsize=20)
style.configure("TEntry", padding=5, relief="flat", font=("Helvetica", 12))
style.map("TCombobox", fieldbackground=[("readonly", "white")])

font_style = ("Helvetica", 12)

# Doctor Login Form
doctor_frame = ttk.LabelFrame(root, text="Doctor Login")
doctor_frame.grid(row=0, column=0, padx=20, pady=20)

doctor_username_label = tk.Label(doctor_frame, text="Username:", font=font_style)
doctor_username_label.grid(row=0, column=0, padx=10, pady=5)

doctor_username_entry = tk.Entry(doctor_frame, font=font_style)
doctor_username_entry.grid(row=0, column=1, padx=10, pady=5)

doctor_password_label = tk.Label(doctor_frame, text="Password:", font=font_style)
doctor_password_label.grid(row=1, column=0, padx=10, pady=5)

doctor_password_entry = tk.Entry(doctor_frame, show="*", font=font_style)
doctor_password_entry.grid(row=1, column=1, padx=10, pady=5)

doctor_login_button = tk.Button(doctor_frame, text="Login", command=doctor_login, bg="#4CAF50", fg="white",font=font_style)
doctor_login_button.grid(row=2, columnspan=2, padx=10, pady=10)

# Patient Login Form
patient_frame = ttk.LabelFrame(root, text="Patient Login")
patient_frame.grid(row=0, column=1, padx=20, pady=20)

patient_username_label = tk.Label(patient_frame, text="Username:", font=font_style)
patient_username_label.grid(row=0, column=0, padx=10, pady=5)

patient_username_entry = tk.Entry(patient_frame, font=font_style)
patient_username_entry.grid(row=0, column=1, padx=10, pady=5)

patient_password_label = tk.Label(patient_frame, text="Password:", font=font_style)
patient_password_label.grid(row=1, column=0, padx=10, pady=5)

patient_password_entry = tk.Entry(patient_frame, show="*", font=font_style)
patient_password_entry.grid(row=1, column=1, padx=10, pady=5)

patient_login_button = tk.Button(patient_frame, text="Login", command=patient_login, bg="#2196F3", fg="white", font=font_style)
patient_login_button.grid(row=2, columnspan=2, padx=10, pady=10)

root.mainloop()
