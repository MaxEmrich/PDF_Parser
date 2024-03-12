from PyPDF2 import PdfReader, PdfWriter
import os

class PDF_PARSER:
    def __init__(self, pdf_name):
        self.pdf_name = pdf_name
        return

    def create_reader(self, directory=None):
        if directory is None:
            # If no directory is specified, use the directory of the calling script
            print("ERROR: Path not provided")
            return 1

        document_path = os.path.join(directory, "document_uploads", self.pdf_name)
        reader = PdfReader(document_path)
        return reader

    def create_writer(self):
        writer = PdfWriter()
        return writer



