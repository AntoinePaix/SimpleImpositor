import argparse
import os
import sys
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from math import ceil

######### Simple Impositor ##########

# Author : Antoine Paix
# Github : https://github.com/AntoinePaix


# This Python script allows you to impose PDF files in order
# to print them in A5 format with 2 pages per side (i.e. 4 pages per sheet).


def extract_information(pdf_path):

    with open(pdf_path, "rb") as f:
        pdf = PdfFileReader(f)
        # information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
        return number_of_pages

def reordering_pages(number_of_pages):

    original_num_pages = number_of_pages
    new_num_pages = ceil(original_num_pages / 4) * 4
    pages_list = [i for i in range(new_num_pages)]

    n = len(pages_list) - 1

    new_list_pages = []

    for i in range(0, int(n/2), 2):
        page = pages_list[n-i]
        new_list_pages.append(page)
        page = pages_list[i]
        new_list_pages.append(page)
        page = pages_list[i+1]
        new_list_pages.append(page)
        page = pages_list[n-i-1]
        new_list_pages.append(page)

    for index, value in enumerate(new_list_pages):
        if value >= original_num_pages:
            new_list_pages[index] = "blank_page"

    return new_list_pages

def new_filename(filename):
    filename, file_extension = os.path.splitext(filename)
    return filename + "_convert_imposition" + file_extension


def generate_pdf(list_of_pages, path):
    pdf = PdfFileReader(path)
    pdf_writer = PdfFileWriter()

    for page in list_of_pages:
        if page == 'blank_page':
            pdf_writer.addBlankPage(611.97165, 791.97165)
        else:
            pdf_writer.addPage(pdf.getPage(page))

    output = new_filename(path)
    with open(output, "wb") as output_pdf:
        pdf_writer.write(output_pdf)
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Simple Python script to impose PDF files")
    parser.add_argument('file', metavar='path', type=str, help='Path to PDF file to impose')
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print("[-] The path specified does not exist.")
        sys.exit()

    num_pages = extract_information(args.file)
    list_of_pages = reordering_pages(num_pages)
    generate_pdf(list_of_pages, args.file)

    new_file = new_filename(args.file)
    abspath = os.path.abspath(new_file)

    if os.path.isfile(new_file):
        print('[+] The file "{}" has been generated.'.format(abspath))
    
