import tkinter as tk
from tkinter import scrolledtext, messagebox

# read the file and get all student data
def load_students():
    students = []
    file = open("studentMarks.txt", "r")
    lines = file.readlines()  # grab every line
    file.close()
    
    # first line tells us how many students
    num_students = int(lines[0])
    
    # go through each student line
    for i in range(1, num_students + 1):
        parts = lines[i].strip().split(',')  # split by comma
        
        # grab each piece of info
        number = parts[0]
        name = parts[1]
        mark1 = int(parts[2])
        mark2 = int(parts[3])
        mark3 = int(parts[4])
        exam = int(parts[5])
        
        # calculate their total marks
        coursework = mark1 + mark2 + mark3  # add up 3 coursework marks
        total = coursework + exam           # add coursework + exam
        percentage = (total / 160) * 100    # out of 160 total marks
        
        # figure out their grade
        if percentage >= 70:
            grade = 'A'
        elif percentage >= 60:
            grade = 'B'
        elif percentage >= 50:
            grade = 'C'
        elif percentage >= 40:
            grade = 'D'
        else:
            grade = 'F'
        
        # store student info in a dictionary
        student = {
            'number': number,
            'name': name,
            'coursework': coursework,
            'exam': exam,
            'percentage': percentage,
            'grade': grade
        }
        students.append(student)  # add to our list
    
    return students

# display one student's info nicely
def show_student(student, output_box):
    output_box.insert(tk.END, f"Student Name: {student['name']}\n")
    output_box.insert(tk.END, f"Student Number: {student['number']}\n")
    output_box.insert(tk.END, f"Total Coursework: {student['coursework']}/60\n")
    output_box.insert(tk.END, f"Exam Mark: {student['exam']}/100\n")
    output_box.insert(tk.END, f"Overall Percentage: {student['percentage']:.2f}%\n")
    output_box.insert(tk.END, f"Grade: {student['grade']}\n")
    output_box.insert(tk.END, "-" * 50 + "\n\n")  # divider line

# when user clicks "View All Students" button
def view_all():
    output_box.delete(1.0, tk.END)  # clear the text box
    output_box.insert(tk.END, "ALL STUDENTS\n\n")
    
    # loop through and show each student
    for student in students:
        show_student(student, output_box)
    
    # calculate class average
    total_percentage = 0
    for student in students:
        total_percentage += student['percentage']
    average = total_percentage / len(students)
    
    # show summary at bottom
    output_box.insert(tk.END, f"Total Students: {len(students)}\n")
    output_box.insert(tk.END, f"Average Percentage: {average:.2f}%\n")

# when user clicks "View Individual" button
def view_individual():
    # create popup window for search
    search_window = tk.Toplevel(window)
    search_window.title("Find Student")
    search_window.geometry("300x120")
    
    tk.Label(search_window, text="Enter Student Number or Name:").pack(pady=10)
    entry = tk.Entry(search_window, width=30)
    entry.pack(pady=5)
    
    # when they click find button
    def find_student():
        search = entry.get()  # get what they typed
        found = None
        
        # search through all students
        for student in students:
            # check if number matches or name contains search text
            if search == student['number'] or search.lower() in student['name'].lower():
                found = student
                break  # stop searching once we find them
        
        if found:
            # show the student we found
            output_box.delete(1.0, tk.END)
            output_box.insert(tk.END, "STUDENT FOUND\n\n")
            show_student(found, output_box)
            search_window.destroy()  # close popup
        else:
            messagebox.showinfo("Error", "Student not found!")
    
    tk.Button(search_window, text="Find", command=find_student).pack(pady=5)

# when user clicks "Highest Score" button
def show_highest():
    # start with first student
    highest = students[0]
    
    # check everyone to find highest percentage
    for student in students:
        if student['percentage'] > highest['percentage']:
            highest = student
    
    # show the top student
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "HIGHEST SCORE\n\n")
    show_student(highest, output_box)

# when user clicks "Lowest Score" button
def show_lowest():
    # start with first student
    lowest = students[0]
    
    # check everyone to find lowest percentage
    for student in students:
        if student['percentage'] < lowest['percentage']:
            lowest = student
    
    # show the bottom student
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "LOWEST SCORE\n\n")
    show_student(lowest, output_box)

# load all students when app starts
students = load_students()

# create main window
window = tk.Tk()
window.title("Student Marks")
window.geometry("700x500")

# create 4 buttons at top
tk.Button(window, text="View All Students", command=view_all, width=20).pack(pady=5)
tk.Button(window, text="View Individual", command=view_individual, width=20).pack(pady=5)
tk.Button(window, text="Highest Score", command=show_highest, width=20).pack(pady=5)
tk.Button(window, text="Lowest Score", command=show_lowest, width=20).pack(pady=5)

# create big text box to show results
output_box = scrolledtext.ScrolledText(window, width=80, height=20)
output_box.pack(pady=10)

# start the app
window.mainloop()