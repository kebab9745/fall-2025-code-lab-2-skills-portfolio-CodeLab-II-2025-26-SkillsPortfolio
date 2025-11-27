import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Student Manager")
root.geometry("400x600")
root.config(bg="#C0E4FB")
root.iconbitmap("person copy.ico")

# total to percentage
def percentage(total):
    return (total / 160) * 100

# assigns a grade to a percentage
def grading(percent):
    if percent >= 70:
        return "A"
    elif percent >= 60:
        return "B"
    elif percent >= 50:
        return "C"
    elif percent >= 40:
        return "D"
    else:
        return "F"

# load student data
def student_data():
    students = []
    try:
        with open("studentMarks.txt", "r") as file:
            lines = file.readlines() # reads lines to a list

            student_count = int(lines[0].strip()) # first line of txt file (1o) will be the student count

            for line in lines[1:student_count+1]:
                part = line.strip().split(",") # separates lines by comma
                code = part[0]
                name = part[1]
                cm1 = int(part[2]) # to integer
                cm2 = int(part[3])
                cm3 = int(part[4])
                exam = int(part[5])

                # calculation
                total = cm1 + cm2 + cm3 + exam
                percent = percentage(total)
                grade = grading(percent)

                # dictionary to store data of students
                students.append({
                    "code": code,
                    "name": name,
                    "cm1": cm1,
                    "cm2": cm2,
                    "cm3": cm3,
                    "exam": exam,
                    "total": total,
                    "percent": percent,
                    "grade": grade
                })
    except FileNotFoundError:
        messagebox.showerror("Error", "studentMarks.txt not found.")
    return students

students = student_data()

# save the changes to the txt file
def save_to_file():
    with open("studentMarks.txt", "w") as file:
        file.write(str(len(students)) + "\n")
        for s in students:
            file.write(f"{s['code']},{s['name']},{s['cm1']},{s['cm2']},{s['cm3']},{s['exam']}\n")

# format for student details
def student_details(s):
    return (
        f"Student Name: {s['name']}\n"
        f"Student Code: {s['code']}\n"
        f"Total Coursework: {s['cm1'] + s['cm2'] + s['cm3']}\n"
        f"Exam Mark: {s['exam']}\n"
        f"Overall Percentage: {s['percent']:.2f}%\n"
        f"Grade: {s['grade']}\n"
        f"{'-'*40}\n"
    )

# searching student code
def search_student():
    code = entry_code.get().strip() # input
    if code == "":
        messagebox.showwarning("Input Error", "Please enter a valid code.") # msg box
        return

    for s in students:
        if s["code"] == code:
            output.delete("1.0", tk.END)
            output.insert(tk.END, student_details(s))
            return
        
    messagebox.showinfo("Not Found", "Oops, no student with that code.")

# clears the output then replaces with all the student data
def all_students():
    output.delete("1.0", tk.END)
    for s in students:
        output.insert(tk.END, student_details(s))

    # calculation for class average percent
    avg = sum(s["percent"] for s in students) / len(students)
    output.insert(tk.END, f"Total Students: {len(students)}\n")
    output.insert(tk.END, f"Average Percentage: {avg:.2f}%\n")

# highest score
def highest_score():
    highest = max(students, key=lambda x: x["total"])
    output.delete("1.0", tk.END)
    output.insert(tk.END, "Student with Highest Score:\n")
    output.insert(tk.END, student_details(highest))

# lowest score
def lowest_score():
    lowest = min(students, key=lambda x: x["total"])
    output.delete("1.0", tk.END)
    output.insert(tk.END, "Student with Lowest Score:\n")
    output.insert(tk.END, student_details(lowest))

# pop up window for adding new students
def add_student_window():
    win = tk.Toplevel(root)
    win.title("Add Student")
    win.geometry("300x300")

    labels = ["Code", "Name", "Coursework 1", "Coursework 2", "Coursework 3", "Exam"]
    entries = {}

    for text in labels:
        tk.Label(win, text=text).pack()
        entries[text] = tk.Entry(win)
        entries[text].pack()

    def add_student():
        try:
            code = entries["Code"].get().strip()
            name = entries["Name"].get().strip()
            cm1 = int(entries["Coursework 1"].get())
            cm2 = int(entries["Coursework 2"].get())
            cm3 = int(entries["Coursework 3"].get())
            exam = int(entries["Exam"].get())

            total = cm1 + cm2 + cm3 + exam
            percent = percentage(total)
            grade = grading(percent)

            students.append({
                "code": code,
                "name": name,
                "cm1": cm1,
                "cm2": cm2,
                "cm3": cm3,
                "exam": exam,
                "total": total,
                "percent": percent,
                "grade": grade
            })

            save_to_file()
            messagebox.showinfo("Success", "Student added.")
            win.destroy()

        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers.")

    tk.Button(win, text="Add", command=add_student).pack(pady=10)

# pop up window for updating student records
def update_student_window():
    win = tk.Toplevel(root)
    win.title("Update Student")
    win.geometry("300x350")

    tk.Label(win, text="Enter Student Code:").pack()
    code_entry = tk.Entry(win)
    code_entry.pack()

    frame_fields = tk.Frame(win)
    entries = {}

    def load_student():
        code = code_entry.get().strip()
        for s in students:
            if s["code"] == code:

                frame_fields.pack(pady=10)
                for widget in frame_fields.winfo_children():
                    widget.destroy()

                fields = ["name", "cm1", "cm2", "cm3", "exam"]
                for f in fields:
                    tk.Label(frame_fields, text=f"New {f.capitalize()}:").pack()
                    e = tk.Entry(frame_fields)
                    e.insert(0, str(s[f]))
                    e.pack()
                    entries[f] = e

                # save changes to file
                def save_updates():
                    try:
                        s["name"] = entries["name"].get()
                        s["cm1"] = int(entries["cm1"].get())
                        s["cm2"] = int(entries["cm2"].get())
                        s["cm3"] = int(entries["cm3"].get())
                        s["exam"] = int(entries["exam"].get())

                        s["total"] = s["cm1"] + s["cm2"] + s["cm3"] + s["exam"]
                        s["percent"] = percentage(s["total"])
                        s["grade"] = grading(s["percent"])

                        save_to_file()
                        messagebox.showinfo("Success", "Record updated.")
                        win.destroy()

                    except ValueError:
                        messagebox.showerror("Error", "Invalid input.")

                tk.Button(frame_fields, text="Save Changes", command=save_updates).pack(pady=10)
                return

        messagebox.showerror("Error", "Student not found.")

    tk.Button(win, text="Load Student", command=load_student).pack(pady=10)

# pop up window for deleting a student record
def delete_student_window():
    win = tk.Toplevel(root)
    win.title("Delete Student")
    win.geometry("250x150")

    tk.Label(win, text="Enter Student Code to Delete:").pack()
    entry = tk.Entry(win)
    entry.pack()

    def delete():
        code = entry.get().strip()
        for s in students:
            if s["code"] == code:
                students.remove(s)
                save_to_file()
                messagebox.showinfo("Success", "Student deleted.")
                win.destroy()
                return
        messagebox.showerror("Error", "Student not found.")

    tk.Button(win, text="Delete", command=delete).pack(pady=10)

# pop up window for sorting students record
def sort_students_window():
    win = tk.Toplevel(root)
    win.title("Sort Students")
    win.geometry("250x150")

    tk.Label(win, text="Sort by Overall Percentage:").pack(pady=5)

    # ascending
    def sort_ascending():
        students.sort(key=lambda x: x["percent"])
        all_students()
        win.destroy()

    # descending
    def sort_descending():
        students.sort(key=lambda x: x["percent"], reverse=True)
        all_students()
        win.destroy()

    tk.Button(win, text="Ascending", width=15, command=sort_ascending).pack(pady=5)
    tk.Button(win, text="Descending", width=15, command=sort_descending).pack(pady=5)

# search bar + container row
search_frame = tk.Frame(root, bg="#9ED5F7")
search_frame.pack(pady=10)

tk.Label(search_frame, bg="#9ED5F7", text="Student Code:").pack(side=tk.LEFT, padx=5) # label

# input for student code
entry_code = tk.Entry(search_frame, width=15)
entry_code.pack(side=tk.LEFT, padx=5)

#search button beside the input
tk.Button(search_frame, text="Search", bg="#9ED5F7", command=search_student).pack(side=tk.LEFT, padx=5)

# buttons below input and search button
tk.Button(root, text="Show All Students", width=20, bg="#9ED5F7", command=all_students).pack(pady=4)
tk.Button(root, text="Highest Mark", width=20, bg="#9ED5F7", command=highest_score).pack(pady=4)
tk.Button(root, text="Lowest Mark", width=20, bg="#9ED5F7", command=lowest_score).pack(pady=4)
tk.Button(root, text="Add Student", width=20, bg="#9ED5F7", command=add_student_window).pack(pady=4)
tk.Button(root, text="Update Student", width=20, bg="#9ED5F7", command=update_student_window).pack(pady=4)
tk.Button(root, text="Delete Student", width=20, bg="#9ED5F7", command=delete_student_window).pack(pady=4)
tk.Button(root, text="Sort Students", width=20, bg="#9ED5F7", command=sort_students_window).pack(pady=4)

output = tk.Text(root, width=60, height=20)
output.pack(padx=10, pady=10)

root.mainloop()