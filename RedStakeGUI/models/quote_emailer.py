import logging
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from RedStakeGUI.constants import SETTINGS_MANAGER


class QuoteEmail:
    """Class to send email with quote attached."""

    def __init__(self, inputs: dict, parcel_data: dict, quote_file_path: str):
        self.inputs = inputs
        self.parcel_data = parcel_data
        self.quote_file_path = quote_file_path
        (
            self.sender,
            self.receiver,
            self.password,
        ) = SETTINGS_MANAGER.get_email_settings()
        self.subject = self.create_subject()
        self.message = self.create_message()

    def create_subject(self) -> str:
        """This method will create the subject for the email.

        Returns:
            str: The subject for the email.
        """
        subject_suffix = " - (Survey Quote Request)"
        subject = self.parcel_data.get("PRIMARY_ADDRESS", "")
        return subject + subject_suffix

    def create_message(self) -> str:
        """This method will create the message for the email.

        Returns:
            str: The message for the email.
        """
        address = self.parcel_data.get("PRIMARY_ADDRESS", "")
        scope_of_work = self.inputs.get("Scope of Work", "").get().strip()
        additional_info = (
            self.inputs.get("Additional Information", "").get().strip()
        )
        if additional_info:
            additional_info = "\nAdditional Info = " + additional_info

        parcel_links = self.parcel_data.get("LINKS", "")
        appraiser = parcel_links.get("PROPERTY_APPRAISER", "")

        appraiser_map = parcel_links.get("MAP", "")
        if appraiser_map:
            appraiser_map = "\nMap = " + appraiser_map

        deed = parcel_links.get("DEED", "")
        if deed:
            deed = "\nDeed = " + deed

        plat = parcel_links.get("PLAT", "")
        if plat:
            plat = "\nPlat = " + plat

        message = """Hello,

See attached files for supporting data on this quote.

Address = {address}
Requested services = {scope_of_work}{additional_info}

Property Appraiser = {appraiser}{appraiser_map}{deed}{plat}

Thank you"""

        return message.format(
            address=address,
            scope_of_work=scope_of_work,
            additional_info=additional_info,
            appraiser=appraiser,
            appraiser_map=appraiser_map,
            deed=deed,
            plat=plat,
        )

    def send_email(self) -> None:
        """This method will send the email with the quote attached."""
        msg = MIMEMultipart()
        msg["Subject"] = self.subject
        msg["From"] = self.sender
        msg["To"] = self.receiver

        msg.attach(MIMEText(self.message, "plain"))

        filename = self.quote_file_path

        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {Path(filename).name}",
        )

        msg.attach(part)
        text = msg.as_string()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            try:
                logging.info("Logging into Gmail.")
                logging.info(f"Sender: {self.sender}")
                logging.info(f"Receiver: {self.receiver}")
                smtp_server.login(self.sender, self.password.decode())
            except smtplib.SMTPAuthenticationError:
                logging.error("Failed to log into Gmail.")
                return

            try:
                smtp_server.sendmail(self.sender, self.receiver, text)
                logging.info("Successfully sent email.")
            except smtplib.SMTPRecipientsRefused:
                logging.error("Failed to send email.")
                return
