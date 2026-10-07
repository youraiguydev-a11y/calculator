from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None

    if request.method == "POST":
        num1 = request.form.get("num1")
        num2 = request.form.get("num2")
        choice = request.form.get("choice")

        try:
            num1 = float(num1)
            num2 = float(num2)

            if choice == "+":
                result = num1 + num2
            elif choice == "-":
                result = num1 - num2
            elif choice == "*":
                result = num1 * num2
            elif choice == "/":
                if num2 == 0:
                    result = "Cannot divide by zero"
                else:
                    result = num1 / num2
            else:
                result = "Invalid operation"

        except:
            result = "Please enter valid numbers"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
