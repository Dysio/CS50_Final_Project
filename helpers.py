import os

def directory_check(dir_path):
    """Function check if directory exist if not it will create it"""
    if os.path.isdir(dir_path):
        print("exist")
        return True
    else:
        dir_name = dir_path.split('\\')[-1]
        print(f"Created directory = {dir_name}")
        os.mkdir(dir_path)

    return True

def files_check(dir_path):
    if len(os.listdir(dir_path)) == 0:
        return "Directory is empty"
    else:
        for file in os.listdir(dir_path):
            file = os.path.join(dir_path, file)
            print(file)
            os.remove(file)
        return "There were files in directory"

dir_path = r"D:\SONY\Nauka\EDX\Week_10_Final_Project\static\pdf"
directory_check(dir_path)
