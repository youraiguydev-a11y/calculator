from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calculator():

    result = ""

    if request.method == "POST":

        num1_text = request.form.get("num1", "")
        num2_text = request.form.get("num2", "")
        choice = request.form.get("choice", "")

        if num1_text == "" or num2_text == "" or choice == "":
            result = "Invalid"

        else:
            num1 = float(num1_text)
            num2 = float(num2_text)

            if choice == "+":
                result = num1 + num2

            elif choice == "-":
                result = num1 - num2

            elif choice == "*":
                result = num1 * num2

            elif choice == "/":
                if num2 == 0:
                    result = "Error"
                else:
                    result = num1 / num2

            else:
                result = "Invalid"

            if isinstance(result, float) and result == int(result):
                result = int(result)

    return render_template("index.html", result=result)


app.run(debug=True)
