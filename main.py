# PDF to Audio Project
# Create a script that takes a PDF file and converts the text to speech.

# Example Text-To-Speech APIs
# http://www.ispeech.org/api/#introduction
# https://cloud.google.com/text-to-speech/docs/basics
# https://aws.amazon.com/polly/

# Possible free solutions
# pip install gtts
# http://www.voicerss.org/login.aspx

import sys
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser, PDFSyntaxError

# Define API for conversion
# API URL GOES HERE


def open_file():
    """Check for a filename added at command line
    or ask the user to enter a filename."""
    # Check for command line input
    try:
        cl_argument = sys.argv[1]
        extracted_text = convert_pdf_to_string(cl_argument)
        return extracted_text
    except IndexError:  # No argument at command line
        pass
    except (FileNotFoundError, PDFSyntaxError):
        print("\nFile added at command line not found or not a valid PDF.\n")

    # If no command line input ask user for input
    while True:
        input_file = input("What is the file you want to convert?\n> ")
        try:
            extracted_text = convert_pdf_to_string(input_file)
            return extracted_text
        except (FileNotFoundError, PDFSyntaxError):
            print("\nFile not found or not valid, try again.\n")


def convert_pdf_to_string(file_path):
    """Parse PDF and return text as string"""
    output_string = StringIO()
    with open(file_path, "rb") as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return output_string.getvalue()


pdf = open_file()

print(pdf)


# Submit file to online API for conversion

# Save or play audio returned
