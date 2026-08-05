import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(receiver: str, subject: str, body: str):
    """
    Generic email sender
    """

    if not EMAIL or not EMAIL_PASSWORD:
        print("Email credentials are not configured.")
        return

    try:
        message = MIMEMultipart()

        message["From"] = EMAIL
        message["To"] = receiver
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)

        server.sendmail(
            EMAIL,
            receiver,
            message.as_string()
        )

        server.quit()

        print(f"Email sent to {receiver}")

    except Exception as e:
        print("Email sending failed")
        print(e)


def send_receive_email(partner, shipment):
    """
    Send Goods Receive Note email to partner.
    """

    body = f"""
Dear {partner.name},

We have successfully received your shipment.

========================================

Receive No : {shipment.receive_no}

Shipment No : {shipment.shipment_no}

Received Date : {shipment.received_date}

Received By : {shipment.received_by}

Origin : {shipment.origin}

Carrier : {shipment.carrier}

Tracking No : {shipment.tracking_no}

========================================

Equipment Received

"""

    for item in shipment.items:
        body += (
            f"- {item.equipment.name}"
            f" | Qty: {item.quantity}"
            f" | Condition: {item.condition}\n"
        )

    body += f"""

========================================

Remarks

{shipment.remarks or "-"}

Thank you.

Makalu Adventure Pvt. Ltd.
Kathmandu, Nepal
"""

    send_email(
        receiver=partner.email,
        subject=f"Goods Received - {shipment.receive_no}",
        body=body,
    )


def send_assignment_email(partner, assignment):
    """
    Email when equipment is assigned.
    """

    body = f"""
Dear {partner.name},

Equipment has been assigned.

Assignment No : {assignment.assignment_no}

Trip : {assignment.trip_name}

Leader : {assignment.expedition_leader}

Assigned Date : {assignment.assigned_date}

========================================

Equipment

"""

    for item in assignment.items:
        body += (
            f"- {item.equipment.name}"
            f" | Qty: {item.quantity}\n"
        )

    body += """

Regards,

Makalu Adventure Pvt. Ltd.
"""

    send_email(
        receiver=partner.email,
        subject=f"Equipment Assignment - {assignment.assignment_no}",
        body=body,
    )


def send_return_email(partner, partner_return):
    """
    Email when equipment is returned.
    """

    body = f"""
Dear {partner.name},

Equipment has been returned.

Return No : {partner_return.return_no}

Returned Date : {partner_return.returned_date}

========================================

Returned Equipment

"""

    for item in partner_return.items:
        body += (
            f"- {item.equipment.name}"
            f" | Returned: {item.returned_quantity}"
            f" | Missing: {item.missing_quantity}"
            f" | Damaged: {item.damaged_quantity}\n"
        )

    body += """

Regards,

Makalu Adventure Pvt. Ltd.
"""

    send_email(
        receiver=partner.email,
        subject=f"Equipment Return - {partner_return.return_no}",
        body=body,
    )