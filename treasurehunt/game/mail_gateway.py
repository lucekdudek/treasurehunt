from abc import ABC, abstractmethod
from email.message import EmailMessage
from smtplib import SMTP, SMTPException

from treasurehunt.game.exceptions import MailGatewayException
from treasurehunt.settings import TREASUREHUNT_SETTINGS


class MailGateway(ABC):
    @abstractmethod
    async def send_mail(self, subject: str, message: str, recipient: str) -> None:
        raise NotImplementedError


class SMTPlibMailGateway(MailGateway):
    async def send_mail(self, subject: str, message: str, recipient: str) -> None:
        with SMTP(
            TREASUREHUNT_SETTINGS.smtp_host, port=TREASUREHUNT_SETTINGS.smtp_port
        ) as mailman:
            try:
                mailman.send_message(self.__build_message(subject, message, recipient))
            except SMTPException:
                raise MailGatewayException("Cannot send message")

    def __build_message(self, subject: str, message: str, recipient: str):
        email_msg = EmailMessage()
        email_msg.set_content(message, "utf-8")
        email_msg["Subject"] = subject
        email_msg["From"] = TREASUREHUNT_SETTINGS.tresurehunt_email
        email_msg["To"] = recipient
        return email_msg
