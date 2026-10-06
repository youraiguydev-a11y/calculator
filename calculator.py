import tkinter as tk

def calculate():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        choice = operation.get()

        if choice == "+":
            result.config(text=f"Result: {num1 + num2}")

        elif choice == "-":
            result.config(text=f"Result: {num1 - num2}")

        elif choice == "*":
            result.config(text=f"Result: {num1 * num2}")

        elif choice == "/":
            if num2 == 0:
                result.config(text="Cannot divide by zero")
            else:
                result.config(text=f"Result: {num1 / num2}")

        else:
            result.config(text="Invalid choice")

    except:
        result.config(text="Invalid number")


window = tk.Tk()
window.title("My Calculator")
window.geometry("350x450")
window.configure(bg="#1e1e1e")


title = tk.Label(
    window,
    text="CALCULATOR",
    font=("Arial", 24, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title.pack(pady=20)


entry1 = tk.Entry(
    window,
    font=("Arial", 18),
    justify="center"
)
entry1.pack(pady=10)


entry2 = tk.Entry(
    window,
    font=("Arial", 18),
    justify="center"
)
entry2.pack(pady=10)


operation = tk.StringVar()


button_frame = tk.Frame(window, bg="#1e1e1e")
button_frame.pack(pady=20)


operations = ["+", "-", "*", "/"]

for op in operations:
    button = tk.Radiobutton(
        button_frame,
        text=op,
        variable=operation,
        value=op,
        font=("Arial", 16),
        width=3
    )
    button.pack(side="left", padx=5)


calculate_button = tk.Button(
    window,
    text="Calculate",
    command=calculate,
    font=("Arial", 16, "bold"),
    width=15,
    height=2
)

calculate_button.pack(pady=20)


result = tk.Label(
    window,
    text="Result:",
    font=("Arial", 18),
    bg="#1e1e1e",
    fg="white"
)

result.pack(pady=15)


window.mainloop()