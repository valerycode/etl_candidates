from requests import Response

from models import Applicant, SocialType, UploadFileResponse, Vacancy


class Transformer:
    """A class to validate and transform data with pydantic models."""

    def get_cv_info_from_api_response(self, response: Response) -> UploadFileResponse:
        cv = UploadFileResponse(**response.json())
        return cv

    def get_salary(self, cv_salary, db_salary: str) -> str:
        if not cv_salary:
            return db_salary
        return cv_salary

    def get_social_type(self) -> str:
        return SocialType.TELEGRAM.name

    def get_social_value(self, cv_telegram: str, cv_phone: str) -> str:
        if not cv_telegram:
            return cv_phone

    def get_birthday(self, birthdate):
        if birthdate:
            return f'{birthdate.year}-{birthdate.month}-{birthdate.day}'
        return None

    def prepare_applicant_data_for_upload(
        self, cv: UploadFileResponse, db_data: dict
    ) -> Applicant:
        # используются auth_type': 'AH' и 'account_source': 586 до уточнения информации
        # (не поняла, как должен определяться тип для кандидата)
        social_type = self.get_social_type()
        social_value = self.get_social_value(
            cv.fields.telegram, cv.fields.phones[0])
        salary = self.get_salary(cv.fields.salary, db_data.get('salary'))
        birthday = self.get_birthday(cv.fields.birthdate)
        applicant = Applicant(
            first_name=cv.fields.name.first,
            last_name=cv.fields.name.last,
            middle_name=cv.fields.name.middle,
            money=salary,
            phone=cv.fields.phones[0],
            email=cv.fields.email,
            skype=cv.fields.skype,
            position=cv.fields.position,
            company=cv.fields.experience[0].company,
            photo=cv.photo.id,
            birthday=birthday,
            externals=[
                {
                    'auth_type': 'AH',
                    'account_source': 586,
                    'data': {'body': cv.text},
                    'files': [cv.id]
                }]
            ,
            social=[{'social_type': social_type, 'value': social_value}]
        )
        return applicant

    def get_vacancy_id(self, vacancies: list[dict], position: str) -> int:
        for vacancy in vacancies:
            for key, value in vacancy.items():
                if key == position:
                    return value

    def prepare_vacancy_data_for_upload(
            self, vacancy_id: int, status_id: int, comment: str) -> Vacancy:
        vacancy = Vacancy(vacancy=vacancy_id, status=status_id, comment=comment)
        return vacancy
