from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/merge")
def merge():
    return render_template('merge.html')

@app.route("/split")
def split():
    return render_template('split.html')

@app.route("/split_size")
def split_size():
    return render_template('split_size.html')

@app.route("/rotate")
def rotate():
    return render_template('rotate.html')

if __name__ == '__main__':
    app.run(debug="True")