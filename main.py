import logging

from config import etl_settings
from extract_data import Extractor
from load_data import Loader
from transform_data import Transformer


logging.basicConfig(
    level=etl_settings.LOGGING_LEVEL,
    filename=etl_settings.FILENAME,
    format="%(asctime)s, %(levelname)s, %(message)s, %(name)s",
    filemode=etl_settings.FILEMODE,
)

logger = logging.getLogger(__name__)

LOAD_MESSAGE = "Load in Huntflow system {applicants_number} applicants on vacancies with CV files."
ERROR_MESSAGE = "ETL process failed. Error occurs: {error}."
LOADING_SUCCEEDED_MESSAGE = 'Data was successfully loaded in Huntflow system.'
CHANGE_IN_APPLICANTS_AMOUNT_MESSAGE = ('Applicants amount in system before loading is {amount_before},'
                                       ' after loading the number of applicants in system is {amount_after}.')
LOADING_APPLICANT_CV_MESSAGE = 'Start loading applicant CV {filename} in system.'


class ETL:
    """A class to extract, transform and send data with API to Huntflow system."""
    def __init__(self):
        self.extractor = Extractor(etl_settings.FILE_PATH)
        self.transformer = Transformer()
        self.loader = Loader(etl_settings.FILE_PATH, etl_settings.API_URL, etl_settings.ACCESS_TOKEN)

    def load_data_from_files_to_huntflow_system_with_api(self):
        """Load data from CV files and Excel file with db to Huntflow system."""
        account_id = self.loader.get_account_id()
        vacancies = self.loader.get_vacancies(account_id)
        applicants_amount_in_system_before_loading = self.loader.get_applicants_amount(account_id)
        count = 0
        cv_files = self.extractor.get_cv_files()
        for db_data in self.extractor.extract_data_from_excel_file(cv_files):
            response = self.loader.upload_cv(
                account_id, db_data.get('filepath'), db_data.get('filename'), db_data.get('extension'))
            cv_data = self.transformer.get_cv_info_from_api_response(response)
            applicant_data = self.transformer.prepare_applicant_data_for_upload(cv_data, db_data)
            response = self.loader.add_applicant(applicant_data, account_id)
            applicant_id = response.json().get('id')
            vacancy_id = self.transformer.get_vacancy_id(vacancies, db_data.get('position'))
            status_id = self.loader.get_status_id(db_data.get('status'), account_id)
            vacancy = self.transformer.prepare_vacancy_data_for_upload(vacancy_id, status_id, db_data.get('comment'))
            self.loader.add_applicant_to_vacancy(vacancy, applicant_id, account_id)
            count += 1
        logger.debug(LOAD_MESSAGE.format(applicants_number=count))
        applicants_amount_in_system_after_loading = self.loader.get_applicants_amount(account_id)
        logger.debug(CHANGE_IN_APPLICANTS_AMOUNT_MESSAGE.format(
            amount_before=applicants_amount_in_system_before_loading,
            amount_after=applicants_amount_in_system_after_loading)
        )


def main():
    etl = ETL()
    try:
        etl.load_data_from_files_to_huntflow_system_with_api()
    except Exception as error:
        logger.error(ERROR_MESSAGE.format(error=error))
    finally:
        logger.debug(LOADING_SUCCEEDED_MESSAGE)


if __name__ == '__main__':
    main()
