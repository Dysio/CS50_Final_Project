import os
from flask import Flask, redirect, render_template, request, session, \
    send_file, send_from_directory, safe_join, abort
from flask_caching import Cache

from PyPDF2 import PdfFileMerger
import werkzeug

from helpers import directory_check, files_delete


app = Flask(__name__)

cache = Cache()
cache.init_app(app)

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

def files_prepare():

        directory_check(dir_path_uploads)
        directory_check(dir_path_downloads)
        files_delete(dir_path_uploads)
        files_delete(dir_path_downloads)

        cache.clear()

        uploaded_pdfs = request.files.getlist("pdf")
        print(f"Pdfs: {uploaded_pdfs}")

        for pdf in uploaded_pdfs:
            if pdf.filename == '':
                print('No selected file')
                return redirect(request.url)

            if allowed_extensions(pdf.filename):
                filename = werkzeug.utils.secure_filename(pdf.filename)

                pdf.save(os.path.join(app.config['PDF_UPLOADS'], filename))
                print(f"pdf {filename} saved")

            else:
                print("That file extension is not allowed")
                return redirect(request.url)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/download")
def download_file():
    # os.listdir(app.config["PDF_DOWNLOADS"])
    try:
        return send_from_directory(app.config['PDF_DOWNLOADS'], filename='Result.pdf', as_attachment=True,
                                   cache_timeout=0)
    except FileNotFoundError:
        abort(404)

@app.route("/merge", methods=["GET", "POST"])
def merge():

    if request.method == "POST":

        if request.files:
            files_prepare()

            # Merging pdfs
            pdf_merger = PdfFileMerger()
            for pdf in os.listdir(dir_path_uploads):
                pdf_merger.append(str(os.path.join(app.config['PDF_UPLOADS'], pdf)), import_bookmarks=False)

            merged_filename = "Result.pdf"
            file_path = str(os.path.join(app.config['PDF_DOWNLOADS'], merged_filename))
            with open(file_path, 'wb') as output_file:
                pdf_merger.write(output_file)

            pdf_merger.close()

            print(os.listdir(app.config["PDF_DOWNLOADS"]))
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