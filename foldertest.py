import os
import main

print("Input the whole path to the directory where your HTML folders are");

start_directory = input()
i = 1


def start_func(directory):
    global i
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if f.endswith('.htm') or f.endswith('.html'):
            print(f)
            print("File nr# " + str(i))
            main.translate_to_hindi(f)
            i += 1
        if os.path.isdir(f):
            start_func(os.path.join(f))


start_func(start_directory)
