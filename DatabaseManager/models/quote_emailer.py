import logging
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from DatabaseManager.constants import SETTINGS_MANAGER


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
        subject_prefix = ""
        file_number = self.inputs["File Number"].get().strip()
        address = self.parcel_data.get("PRIMARY_ADDRESS", "")
        if file_number and address[0].isnumeric():
            subject_prefix = f"FN {file_number} #"
        elif file_number:
            subject_prefix = f"FN {file_number} "

        subject = self.parcel_data.get("PRIMARY_ADDRESS", "")
        subject_suffix = " - (Survey Quote Request)"

        return (subject_prefix + subject + subject_suffix).strip()

    def create_message(self) -> str:
        """This method will create the message for the email.

        Returns:
            str: The message for the email.
        """
        address = self.parcel_data.get("PRIMARY_ADDRESS", "")
        parcel_id = self.parcel_data.get("PARCEL_ID", "")
        scope_of_work = self.inputs["Scope of Work"].get().strip()
        additional_info = self.inputs["Additional Information"].get().strip()
        parcel_links = self.parcel_data.get("LINKS", "")

        appraiser = parcel_links.get("PROPERTY_APPRAISER", "")
        appraiser_map = parcel_links.get("MAP", "")
        deed = parcel_links.get("DEED", "")
        file_number = self.inputs["File Number"].get().strip()

        if additional_info:
            additional_info = "\nAdditional Info = " + additional_info

        if appraiser_map:
            appraiser_map = "\nMap = " + appraiser_map

        if deed:
            deed = "\nDeed = " + deed

        if file_number:
            file_number = f"File Number = {file_number}\n"

        plat = ""
        if self.parcel_data.get("PLAT_BOOK"):
            plat = "\nPlat = " + parcel_links.get("PLAT", "")

        message = f"""Hello,

See attached files for supporting data on this quote.

{file_number}Address = {address}
Parcel ID = {parcel_id}
Requested services = {scope_of_work}{additional_info}

Property Appraiser = {appraiser}{appraiser_map}{deed}{plat}

Thank you"""

        return message

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
