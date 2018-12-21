from os import mkdir

def setup_temp():
    try:
        mkdir("temp")
    except FileExistsError:
        pass