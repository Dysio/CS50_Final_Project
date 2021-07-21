import os

from PyPDF2 import PdfFileReader, PdfFileWriter
from flask import render_template

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def directory_check(dir_path):
    """Function check if directory exist if not it will create it"""

    if os.path.isdir(dir_path):
        print("Directory exist")
        return True
    else:
        dir_name = dir_path.split('\\')[-1]
        print(f"Created directory = {dir_name}")
        os.mkdir(dir_path)

    return True

def files_delete(dir_path):
    """Cleans passed directory"""

    print(dir_path)
    if len(os.listdir(dir_path)) == 0:
        print("Directory is empty")
        return True
    else:
        for file in os.listdir(dir_path):
            print(f"file {file} removed")
            file = os.path.join(dir_path, file)
            os.remove(file)

        return "Directory cleaned"

def number_check(number, num_of_pages):
    """Simple check if passed argument is positive integer smaller than
    total number of pages."""

    if type(number) is not int:
        return "You have to pass positive integer"
    if number > num_of_pages:
        return "Number out of range"
    if number <= 0:
        return "Number must be positive integer"
    return 0

def page_size_dict_func(path):
    """Function creates a dictionary with info on page sizes.
    Keys are page height format i.e. "A4","A3","297"
    values are pages number from file."""

    pdf = PdfFileReader(open(path, 'rb'))
    number_of_pages = pdf.getNumPages()
    page_dim_dict = {}
    page_size_dict = {}
    for num in range(number_of_pages):
        page_height = int(float(pdf.getPage(num).mediaBox.getHeight())*0.352)
        page_width = int(float(pdf.getPage(num).mediaBox.getWidth())*0.352)
        page_dim_dict[num] = [int(float(pdf.getPage(num).mediaBox.getHeight())*0.352),
                              int(float(pdf.getPage(num).mediaBox.getWidth())*0.352)]
        if page_height <= 298 and page_width <= 210:
            try:
                page_size_dict["A4"].append(num+1)
            except KeyError:
                page_size_dict["A4"] = [num+1]
        elif page_height <= 298 and page_width <= 420:
            try:
                page_size_dict["A3"].append(num+1)
            except KeyError:
                page_size_dict["A3"] = [num+1]
        elif page_height <= 297:
            try:
                page_size_dict["297"].append(num+1)
            except KeyError:
                page_size_dict["297"] = [num+1]
        elif page_height <= 420:
            try:
                page_size_dict["420"].append(num+1)
            except KeyError:
                page_size_dict["420"] = [num+1]
        elif page_height <= 610:
            try:
                page_size_dict["610"].append(num+1)
            except KeyError:
                page_size_dict["610"] = [num+1]
        else:
            try:
                page_size_dict["big"].append(num+1)
            except KeyError:
                page_size_dict["big"] = [num+1]

    # close the file without it error 32 occur
    pdf.stream.close()

    return page_size_dict


def split_pages_by_height(path, page_size_dict, output_path=False):
    """Functions split document into several files
     grouped by page height parameter"""

    pdf = PdfFileReader(path)
    if output_path:
        output_path += "\\"
        print(output_path)

    for key in page_size_dict:
        print(f"{key}:{page_size_dict[key]}")
        pdf_writer = PdfFileWriter()
        for page_num in page_size_dict[key]:
            pdf_writer.addPage(pdf.getPage(page_num-1))
            filename = path.split("\\")[-1][:-4]
            output = output_path + f'{filename}_{key}.pdf'
            with open(output, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)


if __name__ == '__main__':
    dir_path = r"D:\SONY\Nauka\EDX\Week_10_Final_Project\static\pdf"
    directory_check(dir_path)
