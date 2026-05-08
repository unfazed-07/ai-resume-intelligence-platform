import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_automation_email(receiver_email, candidate_name, score, custom_msg):
    """
    Sends a formal invitation for an interview to selected candidates.
    """
    sender_email = os.getenv("SENDER_EMAIL")
    password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender_email or not password:
        return False, "Email credentials missing in .env"

    # Create the email container
    message = MIMEMultipart()
    message["From"] = f"Hiring Team <{sender_email}>"
    message["To"] = receiver_email
    message["Subject"] = f"Interview Invitation: {candidate_name}"

    # Formal HTML Email Body
    # We use f-strings to inject the name and score directly into the formal template
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: auto; border: 1px solid #eee; padding: 20px;">
            <h2 style="color: #2c3e50;">Congratulations, {candidate_name}!</h2>
            <p>Dear {candidate_name},</p>

            <p>Following a comprehensive review of your profile and technical qualifications, we are pleased to inform you that you have been <b>selected for an interview</b>.</p>

            <p>Our AI-driven assessment platform identified a strong alignment between your expertise and our current requirements, with a calculated match score of <b>{score}%</b>.</p>

            <div style="background-color: #f9f9f9; padding: 15px; border-left: 5px solid #27ae60; margin: 20px 0;">
                <b>Message from the Recruiter:</b><br>
                <i>"{custom_msg}"</i>
            </div>

            <p>Our team will reach out to you shortly to coordinate a convenient time for the initial discussion. In the meantime, please feel free to reply to this email if you have any immediate questions.</p>

            <p>We look forward to speaking with you.</p>

            <hr style="border: 0; border-top: 1px solid #eee;">
            <p style="font-size: 0.9em; color: #7f8c8d;">
                Best Regards,<br>
                <b>The Talent Acquisition Team</b><br>
                <i>Sent via AI Resume Intelligence Platform</i>
            </p>
        </div>
    </body>
    </html>
    """

    message.attach(MIMEText(body, "html"))

    try:
        # Establish a secure connection to the Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(1)  # Set to 1 to see the exact error in your terminal if it fails
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True, "Email sent successfully"
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication Failed: Check your App Password and Sender Email."
    except Exception as e:
        return False, f"Connection Error: {str(e)}"