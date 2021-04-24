import os

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

if __name__ == '__main__':
    dir_path = r"D:\SONY\Nauka\EDX\Week_10_Final_Project\static\pdf"
    directory_check(dir_path)
