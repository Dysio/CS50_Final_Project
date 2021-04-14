import os
from flask import Flask, redirect, render_template, request, session
from helpers import directory_check, files_check

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
dir_path = r"D:\SONY\Nauka\EDX\Week_10_Final_Project\static\pdf"
app.config["PDF_UPLOADS"] = r"D:\SONY\Nauka\EDX\Week_10_Final_Project\static\pdf"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/merge", methods=["GET", "POST"])
def merge():

    if request.method == "POST":
        if request.files:
            directory_check(dir_path)
            print(files_check(dir_path))

            pdf = request.files["pdf"]
            print(pdf)

            pdf.save(os.path.join(app.config['PDF_UPLOADS'], pdf.filename))
            print("pdf saved")

            print(os.listdir(dir_path))

            if pdf.filename == '':
                flash('No selected file')
                return redirect(request.url)

            return redirect(request.url)

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