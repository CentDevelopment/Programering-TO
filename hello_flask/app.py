from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        first_name = request.form["firstname"]
        last_name = request.form["lastname"]
        date = request.form["date"]
        confirmation = request.form.get("confirm", False)
        
        # Print the submitted data to the terminal
        print(first_name)
        print(last_name)
        print(date)
        print(confirmation)

        return redirect(url_for("home"))

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
