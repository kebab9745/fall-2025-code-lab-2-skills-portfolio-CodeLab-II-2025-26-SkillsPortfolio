import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Student Manager")
root.geometry("400x500")
root.config(bg="#C0E4FB")
root.iconbitmap("person.ico")
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


# search bar + container row
search_frame = tk.Frame(root, bg="#9ED5F7")
search_frame.pack(pady=10)

tk.Label(search_frame, bg="#9ED5F7", text="Student Code:").pack(side=tk.LEFT, padx=5) # label

# input for student code
entry_code = tk.Entry(search_frame, width=15)
entry_code.pack(side=tk.LEFT, padx=5)

#search button beside the input
tk.Button(search_frame, text="Search", bg="#9ED5F7", command=search_student).pack(side=tk.LEFT, padx=5)

# three buttons below input and search button
tk.Button(root, text="Show All Students", width=20, bg="#9ED5F7", command=all_students).pack(pady=4)
tk.Button(root, text="Highest Mark", width=20, bg="#9ED5F7", command=highest_score).pack(pady=4)
tk.Button(root, text="Lowest Mark", width=20, bg="#9ED5F7", command=lowest_score).pack(pady=4)

# box where the student data is displayed
output = tk.Text(root, width=60, height=20)
output.pack(padx=10, pady=10)

root.mainloop()