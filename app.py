from flask import Flask, render_template, request, session
import random
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # change this later for security

@app.route("/", methods=["GET", "POST"])
def home():
    # Initialize game
    if "number" not in session:
        session["number"] = random.randint(1, 100)
        session["attempts"] = 0

    message = ""
    attempts = session.get("attempts", 0)
    message_class = ""

    if request.method == "POST":
        guess_input = request.form.get("guess")

        if not guess_input:
            message = "Please enter a number."
            message_class = "error"
        else:
            try:
                guess = int(guess_input)
                session["attempts"] += 1
                attempts = session["attempts"]

                if guess == session["number"]:
                    message = f"🎉 You successfully guessed the number in {attempts} turns!"
                    message_class = "success"
                    session.pop("number")
                    session.pop("attempts")

                elif guess > session["number"]:
                    message = "The selected number is smaller"
                    message_class = "hint"

                else:
                    message = "The selected number is greater"
                    message_class = "hint"

            except ValueError:
                message = "Enter a valid number!"
                message_class = "error"

    return render_template(
        "index.html",
        message=message,
        attempts=attempts,
        message_class=message_class
    )

# ✅ Required for Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)