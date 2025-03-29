import os


def addToClipBoard(text):
    command = "echo " + text.strip() + "| clip"
    os.system(command)


# example
addToClipBoard("Hello")
