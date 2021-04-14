import os
from flask import Flask, redirect, render_template, request, session
from helpers import directory_check, files_check
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
dir_path = r"D:\SONY\Nauka\EDX\Week_10_Final_Project\static\pdf"
app.config["PDF_UPLOADS"] = r"D:\SONY\Nauka\EDX\Week_10_Final_Project\static\pdf"
app.config["ALLOWED_PDF_EXTENSIONS"] = ["PDF"]


def allowed_extensions(filename):
    """Function check if extension is allowed"""
    if not "." in filename:
        return False

    ext = filename.split(".")[-1]

    if ext.upper() in app.config["ALLOWED_PDF_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/merge", methods=["GET", "POST"])
def merge():

    if request.method == "POST":
        if request.files:
            directory_check(dir_path)
            files_check(dir_path)

            pdf = request.files["pdf"]
            print(pdf)

            if pdf.filename == '':
                print('No selected file')
                return redirect(request.url)

            if allowed_extensions(pdf.filename):
                filename = secure_filename(pdf.filename)

                pdf.save(os.path.join(app.config['PDF_UPLOADS'], filename))
                print("pdf saved")

                return redirect(request.url)

            else:
                print("That file extension is not allowed")
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