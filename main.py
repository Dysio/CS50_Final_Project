from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return "<h1>About Page</h1>"