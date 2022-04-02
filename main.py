# PDF to Audio Project
# Create a script that takes a PDF file and converts the text to speech.

# Example Text-To-Speech APIs
# http://www.ispeech.org/api/#introduction
# https://cloud.google.com/text-to-speech/docs/basics
# https://aws.amazon.com/polly/

# Possible free solutions
# pip install gtts
# http://www.voicerss.org/login.aspx


# Import PDF 2 Text
import pdftotext
import sys

# Define API for conversion
# API URL GOES HERE


def open_PDF():
    """Check for a filename added at command line
    or ask the user to enter a filename."""
    # Check for command line input
    try:
        cl_input = sys.argv[1]
        with open(cl_input, "rb") as file:
            pdf = pdftotext.PDF(file)
            return pdf
    except IndexError:  # No argument at command line
        pass
    except (FileNotFoundError, pdftotext.Error):
        print("\nFile add at command line not found or not a valid PDF.\n")

    # If no command line input ask user for input
    while True:
        work_file = input("What is the file you want to convert?\n> ")
        try:
            with open(work_file, "rb") as file:
                pdf = pdftotext.PDF(file)
                return pdf
        except (FileNotFoundError, pdftotext.Error):
            print("\nFile not found or not valid, try again.\n")


pdf = open_PDF()

# Parse file through PDF To Text
text_to_convert = f"".join(pdf)

print(text_to_convert)


# Submit file to online API for conversion

# Save or play audio returned
