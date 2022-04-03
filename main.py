# PDF to Audio Project
# Create a script that takes a PDF file and converts the text to speech.

# Example Text-To-Speech APIs
# http://www.ispeech.org/api/#introduction
# https://cloud.google.com/text-to-speech/docs/basics
# https://aws.amazon.com/polly/

# Possible free solutions
# pip install gtts
# http://www.voicerss.org/login.aspx

import os
import sys
from io import StringIO

import requests
from dotenv import load_dotenv
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser, PDFSyntaxError
from playsound import playsound

# Define API for conversion
load_dotenv()
API_KEY = os.getenv("VOICE_RSS_KEY")
VOICE_ENDPOINT = "http://api.voicerss.org/?"


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


def main():
    """Open a PDF file, parse text, and playback audio of text. File can be
    command line argument or entered from prompt."""
    pdf_text = open_file()
    # Change 'new line' to 'space' for reading continuity
    pdf_text = pdf_text.replace("\n", " ")
    pdf_text = pdf_text.replace("&", " and ")  # Remove amperstands to avoid URL errors
    pdf_text = pdf_text[:1940]  # Max length of characters excepted by voicerss.org

    # user_text = "Hello my name is John"
    voice_params = {
        "key": API_KEY,
        "hl": "en-us",
        "src": pdf_text,
    }

    # Submit file to online API for conversion
    voice_audio = requests.get(url=VOICE_ENDPOINT, params=voice_params)
    voice_audio.raise_for_status()
    with open("./voice_audio.wav", "wb") as file:
        file.write(voice_audio.content)

    # Save or play audio returned
    playsound("./voice_audio.wav")


if __name__ == "__main__":
    main()
