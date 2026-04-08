from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for sessions

@app.route("/", methods=["GET", "POST"])
def home():
    if "number" not in session:
        session["number"] = random.randint(1, 100)
        session["attempts"] = 0

    message = ""
    attempts = session.get("attempts", 0)
    message_class = ""

    if request.method == "POST":
        guess = request.form.get("guess")

        if not guess:
            message = "Please enter a number."
            message_class = "error"
        else:
            try:
                guess = int(guess)
                session["attempts"] += 1
                attempts = session["attempts"]

                if guess == session["number"]:
                    message = f"🎉 Correct! You guessed it in {attempts} attempts."
                    message_class = "success"
                    session.pop("number")
                    session.pop("attempts")
                elif guess > session["number"]:
                    message = "Too high! Try a smaller number."
                    message_class = "hint"
                else:
                    message = "Too low! Try a bigger number."
                    message_class = "hint"

            except ValueError:
                message = "Enter a valid number."
                message_class = "error"

    return render_template(
        "index.html",
        message=message,
        attempts=attempts,
        message_class=message_class
    )

if __name__ == "__main__":
    app.run(debug=True)