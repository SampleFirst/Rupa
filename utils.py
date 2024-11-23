def get_file_name(file):
    return file.file_name.split(".")[0]

def get_file_extension(file):
    return file.file_name.split(".")[-1]