from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Import resume generator
from utils.ai import generate_resume


@app.route("/", methods=["GET", "POST"])
def index():
    resume = None

    if request.method == "POST":
        user_prompt = request.form.get("user_prompt")

        if user_prompt:
            try:
                resume = generate_resume(user_prompt)
            except Exception as e:
                print("Error generating resume:", e)
                resume = "<p style='color:red;'>Error generating resume</p>"

    return render_template("index.html", resume=resume)


if __name__ == "__main__":
    app.run(debug=True)