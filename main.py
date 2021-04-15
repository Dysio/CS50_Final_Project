import os
from flask import Flask, redirect, render_template, request, session
from helpers import directory_check, files_check
from werkzeug.utils import secure_filename

from PyPDF2 import PdfFileMerger

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
dir_path_uploads = r"D:\SONY\Nauka\EDX\Week_10_Final_Project\static\pdf_uploads"
dir_path_downloads = r"D:\SONY\Nauka\EDX\Week_10_Final_Project\static\pdf_downloads"
app.config["PDF_UPLOADS"] = r"D:\SONY\Nauka\EDX\Week_10_Final_Project\static\pdf_uploads"
app.config["PDF_DOWNLOADS"] = r"D:\SONY\Nauka\EDX\Week_10_Final_Project\static\pdf_downloads"
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
            directory_check(dir_path_uploads)
            directory_check(dir_path_downloads)
            files_check(dir_path_uploads)
            files_check(dir_path_downloads)

            uploaded_pdfs = request.files.getlist("pdf")
            print(f"Pdfs: {uploaded_pdfs}")

            for pdf in uploaded_pdfs:
                if pdf.filename == '':
                    print('No selected file')
                    return redirect(request.url)

                if allowed_extensions(pdf.filename):
                    filename = secure_filename(pdf.filename)

                    pdf.save(os.path.join(app.config['PDF_UPLOADS'], filename))
                    print(f"pdf {filename} saved")

                    # return redirect(request.url)

                else:
                    print("That file extension is not allowed")
                    return redirect(request.url)

            # Merging pdfs
            pdf_merger = PdfFileMerger()
            for pdf in os.listdir(dir_path_uploads):
                # print(pdf)
                # print(os.path.join(app.config['PDF_UPLOADS'], pdf))
                # pdf_merger.append(str(pdf))
                pdf_merger.append(str(os.path.join(app.config['PDF_UPLOADS'], pdf)))

            file_path = str(os.path.join(app.config['PDF_DOWNLOADS'], "Merged.pdf"))
            with open(file_path, 'wb') as output_file:
                pdf_merger.write(output_file)

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