import tkinter as tk
from tkinter import messagebox
import random

# keep track of player's score
score = 0
# how many questions answered so far
question_count = 0
# the two numbers in the math problem
num1 = 0
num2 = 0
# either + or -
operation = ''
# which difficulty level (1, 2, or 3)
difficulty = 0
# how many times they tried current question (0 or 1)
attempt = 0
# the input box where user types answer
answer_box = None

# show the main menu with difficulty options
def displayMenu():
    # clear everything on screen
    for widget in window.winfo_children():
        widget.destroy()
    
    tk.Label(window, text="DIFFICULTY LEVEL", font=("Arial", 16)).pack(pady=20)
    tk.Button(window, text="1. Easy", width=20, command=easyLevel).pack(pady=5)
    
    tk.Button(window, text="2. Moderate", width=20, command=moderateLevel).pack(pady=5)
    tk.Button(window, text="3. Advanced", width=20, command=advancedLevel).pack(pady=5)

# if they pick easy mode
def easyLevel():
    global difficulty
    difficulty = 1
    startQuiz()

# if they pick moderate mode
def moderateLevel():
    global difficulty
    difficulty = 2
    startQuiz()

# if they pick advanced mode
def advancedLevel():
    global difficulty
    difficulty = 3
    startQuiz()

# get random number between min and max
def randomInt(minimum, maximum):
    return random.randint(minimum, maximum)

# randomly pick + or - operation
def decideOperation():
    choice = random.randint(0, 1)
    if choice == 0:
        return '+'
    else:
        return '-'

# start fresh quiz
def startQuiz():
    global score, question_count
    score = 0           # reset score to zero
    question_count = 0  # start from question 1
    displayProblem()    # show first question

# show a math problem on screen
def displayProblem():
    global num1, num2, operation, question_count, attempt, answer_box
    
    # if we did 10 questions, show final results
    if question_count == 10:
        displayResults()
        return
    
    # clear screen
    for widget in window.winfo_children():
        widget.destroy()
    
    # generate numbers based on difficulty
    if difficulty == 1:
        # easy: single digit numbers (0-9)
        num1 = randomInt(0, 9)
        num2 = randomInt(0, 9)
    if difficulty == 2:
        # moderate: two digit numbers (10-99)
        num1 = randomInt(10, 99)
        num2 = randomInt(10, 99)
    if difficulty == 3:
        # advanced: four digit numbers (1000-9999)
        num1 = randomInt(1000, 9999)
        num2 = randomInt(1000, 9999)
    
    # pick random operation
    operation = decideOperation()
    # reset attempts for new question
    attempt = 0
    
    # show question number and current score
    tk.Label(window, text="Question " + str(question_count + 1) + " of 10").pack(pady=10)
    tk.Label(window, text="Score: " + str(score)).pack(pady=5)
    # show the math problem
    tk.Label(window, text=str(num1) + " " + operation + " " + str(num2) + " =", font=("Arial", 18)).pack(pady=20)
    
    # create answer box and put cursor in it
    answer_box = tk.Entry(window, font=("Arial", 14), width=15)
    answer_box.pack(pady=10)
    answer_box.focus()
    tk.Button(window, text="Submit Answer", command=checkAnswer).pack(pady=10)

# when user clicks submit button
def checkAnswer():
    isCorrect(answer_box.get())

# check if answer is right or wrong
def isCorrect(answer):
    global score, question_count, attempt
    
    # calculate correct answer
    if operation == '+':
        correct_answer = num1 + num2
    else:
        correct_answer = num1 - num2
    
    # make sure they typed something
    if answer == '':
        messagebox.showerror("Error", "Please enter a number!")
        return
    
    user_ans = int(answer)
    
    # if they got it right
    if user_ans == correct_answer:
        if attempt == 0:
            # first try = 10 points
            score = score + 10
            messagebox.showinfo("Correct!", "+10 points")
        else:
            # second try = 5 points
            score = score + 5
            messagebox.showinfo("Correct!", "+5 points")
        question_count = question_count + 1  # move to next question
        displayProblem()
    else:
        # if they got it wrong
        attempt = attempt + 1
        if attempt == 1:
            # first wrong attempt - let them try again
            messagebox.showwarning("Wrong", "Try again!")
            displayProblem()
        else:
            # second wrong attempt - show answer and move on
            messagebox.showwarning("Wrong", "Correct answer was " + str(correct_answer))
            question_count = question_count + 1
            displayProblem()

# show final results after 10 questions
def displayResults():
    # clear screen
    for widget in window.winfo_children():
        widget.destroy()
    
    # figure out grade based on score
    if score >= 90:
        grade = "A+"
    if score >= 80 and score < 90:
        grade = "A"
    if score >= 70 and score < 80:
        grade = "B"
    if score >= 60 and score < 70:
        grade = "C"
    if score >= 50 and score < 60:
        grade = "D"
    if score < 50:
        grade = "F"
    
    # show results
    tk.Label(window, text="Quiz Complete!", font=("Arial", 18)).pack(pady=20)
    tk.Label(window, text="Final Score: " + str(score) + " / 100", font=("Arial", 16)).pack(pady=10)
    tk.Label(window, text="Grade: " + grade, font=("Arial", 16)).pack(pady=10)
    tk.Button(window, text="Play Again", width=15, command=displayMenu).pack(pady=10)
    tk.Button(window, text="Exit", width=15, command=window.quit).pack(pady=5)

# create the window
window = tk.Tk()
window.title("Arithmetic Quiz")
window.geometry("400x350")
# show menu first
displayMenu()
# run the app
window.mainloop()