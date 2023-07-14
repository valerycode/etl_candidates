import os

from collections.abc import Iterator
import openpyxl
from unicodedata import normalize


class Extractor:
    """A class to extract data from Excel file with db and create a list with applicants CVs."""

    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def get_cv_files(self) -> list:
        main_folder = os.path.dirname(self.file_path)
        cv_files = []
        for name in os.listdir(main_folder):
            folder = os.path.join(main_folder, name)
            if os.path.isdir(folder):
                for file in os.listdir(folder):
                    filepath = os.path.join(folder, file)
                    cv_files.append({
                        'filepath': filepath,
                        'filename': file,
                        'extension': os.path.splitext(filepath)[1]
                    })
        return cv_files

    def extract_data_from_excel_file(self, cv_files: list) -> Iterator:
        """Extract data from Excel file"""
        excel_file = openpyxl.load_workbook(self.file_path)
        candidates_sheet = excel_file.active
        max_row = candidates_sheet.max_row
        cells = candidates_sheet['A2':f'E{max_row}']
        for position, name, salary, comment, status in cells:
            for cv in cv_files:
                if normalize('NFD', name.value.split()[0].strip()) in cv.get('filename'):
                    yield {
                        'filepath': cv.get('filepath'),
                        'filename': cv.get('filename'),
                        'extension': cv.get('extension'),
                        'position': str(position.value),
                        'name': str(name.value),
                        'salary': str(salary.value),
                        'comment': str(comment.value),
                        'status': str(status.value),
                    }
