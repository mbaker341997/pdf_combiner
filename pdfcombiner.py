from os import path, walk
from PyPDF2 import PdfFileMerger
from time import time

merger = PdfFileMerger()
print("pdf combiner script")
directory_name = input("Enter directory with files: ")

print("Reading pdfs from: {}".format(directory_name))
read_files = []
for (root, _, filenames) in walk(directory_name):
    for filename in filenames:
        input_file = path.join(root, filename)
        merger.append(input_file)
        print("Read file: {}".format(filename))

print("Combining pdfs")
output_filename = "{}.pdf".format(int(time() * 1000))
output = open(output_filename, "wb")
merger.write(output)
output.close()
merger.close()
print("File written to: {}".format(output_filename))
