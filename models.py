from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, HttpUrl


class CVPhoto(BaseModel):
    id: int | None = None
    url: HttpUrl | None = None
    content_type: str | None = None
    name: str | None = None


class ApplicantName(BaseModel):
    first: str | None = None
    last: str | None = None
    middle: str | None = None


class Birthdate(BaseModel):
    year: int | None
    month: int | None
    day: int | None
    precision: str | None


class Experience(BaseModel):
    position: str | None = None
    company: str | None = None


class CVFields(BaseModel):
    name: ApplicantName | None = None
    birthdate: Birthdate | None = None
    phones: list[str] | None = None
    email: EmailStr | None = None
    salary: int | None = None
    position: str | None = None
    skype: str | None = None
    telegram: str | None = None
    experience: list[Experience] | None = None


class UploadFileResponse(BaseModel):
    id: int | None
    url: HttpUrl | None = None
    content_type: str | None = None
    name: str | None = None
    photo: CVPhoto
    text: str | None = None
    fields: CVFields | None = None


class CVBody(BaseModel):
    body: str | None = None


class CV(BaseModel):
    auth_type: str | None = None
    account_source: int | None = None
    data: CVBody | None = None
    files: list[int] | None = None


class SocialType(Enum):
    TELEGRAM = 'TELEGRAM'
    WHATSAPP = 'WHATSAPP'
    LINKEDIN = 'LINKEDIN'
    VIBER = 'VIBER'


class SocialAccount(BaseModel):
    social_type: SocialType
    value: str


class Applicant(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    money: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    skype: str | None = None
    position: str | None = None
    company: str | None = None
    photo: int | None = None
    birthday: str | None = None
    externals: list[CV] | None = None
    social: list[SocialAccount] | None = None


class ApplicantOffer(BaseModel):
    account_applicant_offer: int
    values: dict[str, str]


class FollowUp(BaseModel):
    id: int
    account_member_template: int
    html: str
    days: int


class EmailType(Enum):
    cc = 'cc'
    bcc = 'bcc'
    to = 'to'


class Recipient(BaseModel):
    email: EmailStr
    type: EmailType
    displayName: str | None = None


class EventType(Enum):
    interview = 'interview'
    other = 'other'


class Attendee(BaseModel):
    member: int | None = None
    displayName: str | None = None
    email: EmailStr


class EventTransparency(Enum):
    busy = 'busy'
    free = 'free'


class ReminderMethod(Enum):
    popup = 'popup'
    email = 'email'


class ReminderPeriod(Enum):
    minutes = 'minutes'
    hours = 'hours'
    days = 'days'


class Reminder(BaseModel):
    multiplier: ReminderPeriod
    value: int
    method: ReminderMethod


class CalendarEvent(BaseModel):
    private: bool | None = None
    name: str | None = None
    reminders: list[Reminder]
    location: str | None = None
    interview_type: int | None = None
    event_type: EventType
    description: str | None = None
    calendar: int
    attendees: list[Attendee]
    start: datetime
    end: datetime
    timezone: str | None = None
    transparency: EventTransparency


class TelegramMessage(BaseModel):
    account_im: int
    receiver: str
    body: str


class SmsMessage(BaseModel):
    phone: str
    body: str


class Email(BaseModel):
    account_email: int
    files: list[int] | None = None
    followups: list[FollowUp] | None = None
    html: str
    email: EmailStr
    subject: str
    send_at: datetime | None = None
    timezone: str | None = None
    to: list[Recipient]
    reply: int | None = None


class Vacancy(BaseModel):
    vacancy: int
    status: int
    comment: str | None = None
    rejection_reason: int | None = None
    fill_quota: int | None = None
    employment_date: date | None = None
    files: list[int] | None = None
    calendar_event: CalendarEvent | None = None
    email: Email | None = None
    im: list[TelegramMessage] | None = None
    sms: SmsMessage | None = None
    applicant_offer: ApplicantOffer | None = None
    survey_questionary_id: int | None = None
