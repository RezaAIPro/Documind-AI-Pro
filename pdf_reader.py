import PyPDF2
import os


class PDFReader:

    def read_pdf(self, file_path):
        text = ""

        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            page_count = len(reader.pages)

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        word_count = len(text.split())

        file_size = round(
            os.path.getsize(file_path) / 1024,
            2
        )

        return {
            "text": text,
            "pages": page_count,
            "words": word_count,
            "size": file_size,
            "name": os.path.basename(file_path)
        }