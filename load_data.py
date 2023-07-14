import json
import logging
import requests

from models import Applicant, Vacancy


logger = logging.getLogger(__name__)


ACCOUNT_ID_MESSAGE = 'Response status from API - {status}. Got account_id from API, id is {account_id}.'
STATUS_ID_MESSAGE = 'Response status from API - {status}. Got id for status {name} from API, id is {status_id}.'
VACANCIES_MESSAGE = 'Response status from API - {status}. Got a list with company vacancies from API.'
APPLICANTS_AMOUNT_MESSAGE = 'Response status from API - {status}. The amount of applicants in system is {amount}.'
LOADING_CV_APPLICANT_MESSAGE = 'Response status from API - {status}. Loaded CV with filename {name} in system.'
LOADING_APPLICANT_MESSAGE = ('Response status from API - {status}.'
                             ' Loaded applicant with name {last_name} {first_name} in system.')
LOADING_APPLICANT_TO_VACANCY_MESSAGE = ('Response status from API - {status}. Loaded applicant with id - {applicant_id}'
                                        ' to vacancy with id - {vacancy_id} in system.')
FILE_EXTENSION_ERROR = 'Incorrent file extension {extension}.'


class Loader:
    """A class to get and send data with API."""

    def __init__(self, file_path, api_url, token) -> None:
        self.file_path = file_path
        self.api_url = api_url
        self.token = token

    def get_account_id(self) -> int:
        # получаем id организации по ее названию
        response = requests.get(
            f'{self.api_url}/accounts',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        items = response.json().get('items')[0]
        account_id = items.get('id')
        logger.debug(ACCOUNT_ID_MESSAGE.format(status=response.status_code, account_id=account_id))
        return account_id

    def get_status_id(self, status: str, account_id: int) -> int:
        response = requests.get(
            f'{self.api_url}/accounts/{account_id}/vacancies/statuses',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        items = response.json().get('items')
        for item in items:
            if item.get('name') == status:
                logger.debug(STATUS_ID_MESSAGE.format(
                    status=response.status_code, name=status, status_id=item.get('id'))
                )
                return item.get('id')

    def get_vacancies(self, account_id: int) -> list[dict]:
        response = requests.get(
            f'{self.api_url}/accounts/{account_id}/vacancies',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        items = response.json().get('items')
        vacancies = [{i.get('position'): i.get('id')} for i in items]
        logger.debug(VACANCIES_MESSAGE.format(status=response.status_code))
        return vacancies

    def get_applicants_amount(self, account_id: int) -> int:
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(
            f'{self.api_url}/accounts/{account_id}/applicants',
            headers=headers
        )
        logger.debug(APPLICANTS_AMOUNT_MESSAGE.format(
            status=response.status_code, amount=response.json().get('total_items'))
        )
        return response.json().get('total_items')

    def upload_cv(self, account_id: id, filepath: str, filename: str, extension: str):
        content_type = None
        if extension == '.pdf':
            content_type = 'application/pdf'
        elif extension == '.doc':
            content_type = 'application/msword'
        else:
            logger.error(FILE_EXTENSION_ERROR.format(extension=extension))
        files = {
            'file': (filename,
                     open(filepath, 'rb'),
                     content_type),
        }
        headers = {
            'Authorization': f'Bearer {self.token}',
            'X-File-Parse': 'true',
        }
        response = requests.post(
            f'{self.api_url}/accounts/{account_id}/upload',
            headers=headers,
            files=files
        )
        logger.debug(LOADING_CV_APPLICANT_MESSAGE.format(status=response.status_code, name=filename))
        return response

    def add_applicant(self, applicant: Applicant, account_id: int):
        headers = {
            'Authorization': f'Bearer {self.token}',
        }
        data = json.loads(applicant.model_dump_json())
        response = requests.post(
            f'{self.api_url}/accounts/{account_id}/applicants',
            headers=headers,
            json=data
        )
        logger.debug(LOADING_APPLICANT_MESSAGE.format(
            status=response.status_code, last_name=applicant.last_name, first_name=applicant.first_name)
        )
        return response

    def add_applicant_to_vacancy(self, vacancy: Vacancy, applicant_id: int, account_id: int):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        data = json.loads(vacancy.model_dump_json())
        response = requests.post(
            f'{self.api_url}/accounts/{account_id}/applicants/{applicant_id}/vacancy',
            headers=headers,
            json=data
        )
        logger.debug(LOADING_APPLICANT_TO_VACANCY_MESSAGE.format(
            status=response.status_code, applicant_id=applicant_id, vacancy_id=vacancy.vacancy)
        )
        return response
