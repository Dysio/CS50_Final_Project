import os
import dotenv
import shutil

from flask import Flask, redirect, render_template, request, session, \
    send_file, send_from_directory, safe_join, abort, flash

from pathlib import Path
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import werkzeug

from helpers import apology, directory_check, files_delete, page_size_dict_func, split_pages_by_height, number_check

app = Flask(__name__)

# setting secret key
dotenv_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.debug = os.environ.get("DEBUG")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
dir_path_uploads = os.path.join(os.path.dirname(__file__), "static\pdf_uploads")
dir_path_downloads = os.path.join(os.path.dirname(__file__), "static\pdf_downloads")
app.config["PDF_UPLOADS"] = dir_path_uploads
app.config["PDF_DOWNLOADS"] = dir_path_downloads
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

    uploaded_pdfs = request.files.getlist("pdf")
    print(f"Pdfs: {uploaded_pdfs}")

    for pdf in uploaded_pdfs:
        if pdf.filename == '':
            print('No selected file')
            # flash("No selected file", "error")
            # return redirect(request.url)
            return "No selected file!"

        if allowed_extensions(pdf.filename):
            filename = werkzeug.utils.secure_filename(pdf.filename)

            pdf.save(os.path.join(app.config['PDF_UPLOADS'], filename))
            print(f"pdf {filename} saved")

        else:
            print("That file extension is not allowed")
            # return redirect(request.url)
            return "File extension not allowed"
    return 0


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/download")
def download_file():
    try:
        return send_from_directory(app.config['PDF_DOWNLOADS'], filename='Result.pdf', as_attachment=True,
                                   cache_timeout=0)
    except FileNotFoundError:
        abort(404)

@app.route("/download_all")
def download_all():
    shutil.make_archive('Result', 'zip', os.path.join(os.path.dirname(__file__), "static\pdf_downloads"))
    return send_file('Result.zip', mimetype='zip', attachment_filename='Result.zip', as_attachment=True,
                     cache_timeout=0)


@app.route("/merge", methods=["GET", "POST"])
def merge():

    if request.method == "POST":

        if request.files:
            if not files_prepare() == 0:
                return apology(files_prepare())

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
            flash("Files were merged succesfully", 'success')
            return redirect(request.url)

    return render_template('merge.html')


@app.route("/split", methods=['GET', 'POST'])
def split():
    if request.method == "POST":
        if not files_prepare() == 0:
            return apology(files_prepare())

        pages = request.form.get("pages")
        all_pages = request.form.get("allPagesCheck")
        print(f'pages: {pages}')
        print(f'all_pages: {all_pages}')

        input_pdf = PdfFileReader(str(os.path.join(dir_path_uploads, os.listdir(dir_path_uploads)[0])))
        pdf_writer = PdfFileWriter()
        iterator = 0
        num_of_pages = input_pdf.getNumPages()
        save_path = os.path.join(dir_path_downloads)

        if num_of_pages == 1:
            flash("Passed pdf file has one page and cannot be splitted", "error")
            return redirect(request.url)

        if all_pages == "on":
            print("All pages had to be split")
            # numeration of pages start from 1 to be more user friendly
            page_split = [i for i in range(1, num_of_pages)]
        else:
            try:
                page_split = list(set(int(i) for i in pages.split(',')))
                page_split.sort()
            except ValueError:
                flash("Passed numbers must be positive integers", "error")
                return redirect(request.url)
                # return apology("Number of pages must be positive integer")

        print(f"pages to split: {page_split}")

        if page_split[-1] != num_of_pages:
            page_split.append(num_of_pages)

        for num in page_split:
            if not number_check(num, num_of_pages) == 0:
                return apology(number_check(num, num_of_pages))

            for iterator in range(iterator, num_of_pages):
                page = input_pdf.getPage(iterator)
                pdf_writer.addPage(page)
                iterator += 1
                if iterator == num:
                    filename = f'Result{num}.pdf'
                    with Path(os.path.join(save_path), filename).open(mode="wb") as output_file:
                        pdf_writer.write(output_file)
                    pdf_writer = PdfFileWriter()
                    break

        flash("Files were splitted succesfully", 'success')
        return redirect(request.url)

    return render_template('split.html')


@app.route("/split_size", methods=["GET", "POST"])
def split_size():
    if request.method == "POST":
        if not files_prepare() == 0:
            return apology(files_prepare())

        for pdf in os.listdir(dir_path_uploads):
            split_pages_by_height(str(os.path.join(app.config['PDF_UPLOADS'], pdf)),
                                  page_size_dict_func(str(os.path.join(app.config['PDF_UPLOADS'], pdf))),
                                  output_path=str(os.path.join(app.config['PDF_DOWNLOADS'])))

        flash("Files were splitted succesfully", 'success')
        return redirect(request.url)

    return render_template('split_size.html')

@app.route("/rotate", methods=["GET", "POST"])
def rotate():
    if request.method == "POST":
        if not files_prepare() == 0:
            return apology(files_prepare())

        try:
            if request.form.get("pages90"):
                pages90 = list(set([int(i) for i in request.form.get("pages90").split(',')]))
            else:
                pages90 = []
            if request.form.get("pages180"):
                pages180 = list(set([int(i) for i in request.form.get("pages180").split(',')]))
            else:
                pages180 = []
            if request.form.get("pages270"):
                pages270 = list(set([int(i) for i in request.form.get("pages270").split(',')]))
            else:
                pages270 = []
        except ValueError:
            return apology("Number of pages must be positive integer")

        if pages90 == [] and pages180 == [] and pages270 == []:
            return redirect(request.url)

        pdf_reader = PdfFileReader(os.path.join(dir_path_uploads, os.listdir(dir_path_uploads)[0]))
        pdf_writer = PdfFileWriter()
        num_of_pages = pdf_reader.getNumPages()
        filename = os.listdir(dir_path_uploads)[0].split('.')[0] + "_rotated.pdf"

        for page_num in range(1, num_of_pages + 1):
            if page_num in pages90:
                page = pdf_reader.getPage(page_num - 1).rotateClockwise(90)
            elif page_num in pages180:
                page = pdf_reader.getPage(page_num - 1).rotateClockwise(180)
            elif page_num in pages270:
                page = pdf_reader.getPage(page_num - 1).rotateClockwise(270)
            else:
                page = pdf_reader.getPage(page_num - 1)
            pdf_writer.addPage(page)

        with open(dir_path_downloads + '\\' + filename, 'wb') as fh:
            pdf_writer.write(fh)

        pdf_reader.stream.close()

        print(f"pages90: {pages90} \npages180: {pages180} \npages270: {pages270}")

        flash("Files were rotated succesfully", 'success')
        return redirect(request.url)

    return render_template('rotate.html')

if __name__ == '__main__':
    app.run(debug="True")