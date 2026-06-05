from pypdf import PdfReader


class ResumeParser:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text(self):

        reader = PdfReader(self.pdf_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    def extract_sections(self):

        text = self.extract_text()

        section_names = [
            "Education",
            "Research & Publications",
            "Experience",
            "Projects",
            "Technical Skills",
            "Certifications"
        ]

        sections = {}

        for i, section in enumerate(section_names):

            start = text.find(section)

            if start == -1:
                continue

            if i < len(section_names) - 1:

                next_section = section_names[i + 1]

                end = text.find(next_section)

                if end == -1:
                    end = len(text)

            else:
                end = len(text)

            sections[section] = text[start:end]

        return sections