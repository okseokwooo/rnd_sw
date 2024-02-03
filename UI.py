from tkinter import *

def Interface():
    window = Tk()
    window.geometry("500x300")
    window.title("Interpark Ticketing Program")
    object_frame = Frame(window)
    object_frame.pack()

    id_label = Label(object_frame, text="ID")
    id_label.grid(row=1, column=0)
    id_entry = Entry(object_frame, width=40)
    id_entry.grid(row=1, column=1)
    pw_label = Label(object_frame, text="Password")
    pw_label.grid(row=2, column=0)
    pw_entry = Entry(object_frame, show="*", width=40)
    pw_entry.grid(row=2, column=1)
    showcode_label = Label(object_frame, text="Show code")
    showcode_label.grid(row=4, column=0)
    showcode_entry = Entry(object_frame, width=40)
    showcode_entry.grid(row=4, column=1)
    calender_ladel = Label(object_frame, text="Month")
    calender_ladel.grid(row=6, column=0)
    calender_entry = Entry(object_frame, width=40)
    calender_entry.grid(row=6, column=1)
    date_label = Label(object_frame, text="Date")
    date_label.grid(row=7, column=0)
    date_entry = Entry(object_frame, width=40)
    date_entry.grid(row=7, column=1)
    round_label = Label(object_frame, text="Round")
    round_label.grid(row=8, column=0)
    round_entry = Entry(object_frame, width=40)
    round_entry.grid(row=8, column=1)
    seat_label = Label(object_frame, text="Seat")
    seat_label.grid(row=9, column=0)
    seat_entry = Entry(object_frame, width=40)
    seat_entry.grid(row=9, column=1)
    birth_label = Label(object_frame, text="Birth")
    birth_label.grid(row=11, column=0)
    birth_entry = Entry(object_frame, width=40, show='*')
    birth_entry.grid(row=11, column=1)
    bank_var = IntVar(value=0)
    bank_check = Checkbutton(object_frame, text='무통장', variable=bank_var)
    bank_check.grid(row=12, column=0)
    kakao_var = IntVar(value=0)
    kakao_check = Checkbutton(object_frame, text='카카오', variable=kakao_var)
    kakao_check.grid(row=12, column=1)
    test2_button = Button(object_frame, text="Commit", width=15, height=2)  #,command= // test로 뺴둠
    test2_button.grid(row=13, column=1)
    mainloop()
