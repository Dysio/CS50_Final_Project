# DYSIO PDF EDITOR
### CS50 course: Week 10 Final Project

#### Video Demo: https://www.youtube.com/watch?v=sDyCPWlFfuc
#### Description:

This project is a website that allows users to edit pdf files. 
It was created with Python Flask framework and PyPDF2 library.
There are five pages that consist four main functions to edit pdfs described below.

1. **Home Page**

⋅⋅⋅Welcome to DYSIO PDF EDITOR where you can edit your pdf files with some simple functions.

2. **Merge**

<p>With merge you can join multiple pdf files. They are joined in alphabetical way so remember to give appropriate names to the files first and then upload them.</p>

3. **Split**
<p>With split you can split the whole document just by uploading the file and passing numbers of pages where you want to split the file. Numbers have to be separeted with comma in example "3,5,10". If you want to split all documents into separate pages you can do it by selecting check box "Split all pages".</p> 

4. **Split By Page Size**
<p>With split by page size you can split the whole document by page size. The document will be split into files that consist one height of page: A4, A3, 297, 420, 610 and bigger.</p>

5. **Rotate**
<p>With rotate you can rotate each size of the document just by uploading the file and passing numbers of pages where you want to rotate the page. There are three input fields which allows you to rotate page by 90, 180 and 270 degrees. Like it was in split function numbers have to be separated by comma i.e. "3,5,10".</p> 

In Merge site you can upload multiple files. At other sites Split, Split By Page Size and Rotate you can only upload only one file. Every page with a function includes an upload file option. This form is created to accept only files with a ".pdf" extension.
If you try to do upload some other file extension, the site will inform you that this file extension is not allowed. Also, you can not upload an empty file. The site will show you an error that no file was selected.

Split and Rotate size have additional field input for page numbers where you want to split or rotate the document. You can pass here only positive integers separated by a comma. If you pass character or don't pass anything website will show you information on the top of site that only positive integers are allowed.

#### Running 
1. Download repository to your computer.
1. Set virtual_environment for project.
1. In terminal run command "pip install -r requirements.txt"
1. In main folder create file called ".env" and write in it "SECRET_KEY=(pass_secret_key_here)"
1. In terminal run command "set FLASK_APP=main.py" in Windows or "export FLASK_APP=main.py" in Linux
1. In terminal run command "flask run"

#### Technologies used
 - Python
 - Flask
 - HTML
 - CSS