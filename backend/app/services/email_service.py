from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from typing import List
from app.core.config import settings

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

fm = FastMail(conf)


# ─── Helper ───────────────────────────────────────────────────

async def send_email(
    subject: str,
    recipients: List[str],
    body: str
):
    try:
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=MessageType.html
        )
        await fm.send_message(message)
    except Exception as e:
        # Don't crash app if email fails
        print(f"Email sending failed: {e}")


# ─── Email Templates ──────────────────────────────────────────

async def send_welcome_email(email: str, full_name: str):
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #7c3aed;">Welcome to Influencer Marketing Platform!</h2>
        <p>Hi <strong>{full_name}</strong>,</p>
        <p>Your account has been created successfully.</p>
        <p>You can now login and start using the platform.</p>
        <br>
        <p style="color: #666;">The Influencer Marketing Team</p>
    </body>
    </html>
    """
    await send_email(
        subject="Welcome to Influencer Marketing Platform",
        recipients=[email],
        body=body
    )


async def send_application_status_email(
    email: str,
    full_name: str,
    campaign_title: str,
    status: str
):
    color  = "#22c55e" if status == "approved" else "#ef4444"
    emoji  = "🎉" if status == "approved" else "😔"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: {color};">Application {status.title()} {emoji}</h2>
        <p>Hi <strong>{full_name}</strong>,</p>
        <p>Your application for campaign <strong>"{campaign_title}"</strong>
        has been <strong style="color: {color};">{status}</strong>.</p>
        {"<p>Please login to submit your deliverables.</p>"
          if status == "approved" else
         "<p>Don't worry, keep applying to other campaigns!</p>"}
        <br>
        <p style="color: #666;">The Influencer Marketing Team</p>
    </body>
    </html>
    """
    await send_email(
        subject=f"Application {status.title()} — {campaign_title}",
        recipients=[email],
        body=body
    )


async def send_deliverable_review_email(
    email: str,
    full_name: str,
    campaign_title: str,
    status: str
):
    color = "#22c55e" if status == "approved" else "#ef4444"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: {color};">Deliverable {status.title()}</h2>
        <p>Hi <strong>{full_name}</strong>,</p>
        <p>Your deliverable for campaign <strong>"{campaign_title}"</strong>
        has been <strong style="color: {color};">{status}</strong>.</p>
        {"<p>Payment will be released to you shortly.</p>"
          if status == "approved" else
         "<p>Please login and resubmit your deliverable.</p>"}
        <br>
        <p style="color: #666;">The Influencer Marketing Team</p>
    </body>
    </html>
    """
    await send_email(
        subject=f"Deliverable {status.title()} — {campaign_title}",
        recipients=[email],
        body=body
    )


async def send_payment_released_email(
    email: str,
    full_name: str,
    campaign_title: str,
    amount: float
):
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #22c55e;">Payment Released 💰</h2>
        <p>Hi <strong>{full_name}</strong>,</p>
        <p>Your payment of <strong>${amount:.2f}</strong> for campaign
        <strong>"{campaign_title}"</strong> has been released!</p>
        <p>Login to view your earnings dashboard.</p>
        <br>
        <p style="color: #666;">The Influencer Marketing Team</p>
    </body>
    </html>
    """
    await send_email(
        subject=f"Payment Released — ${amount:.2f}",
        recipients=[email],
        body=body
    )


async def send_campaign_created_email(
    email: str,
    full_name: str,
    campaign_title: str
):
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #7c3aed;">Campaign Created Successfully!</h2>
        <p>Hi <strong>{full_name}</strong>,</p>
        <p>Your campaign <strong>"{campaign_title}"</strong>
        has been created and is now live!</p>
        <p>Influencers can now browse and apply to your campaign.</p>
        <br>
        <p style="color: #666;">The Influencer Marketing Team</p>
    </body>
    </html>
    """
    await send_email(
        subject=f"Campaign Created — {campaign_title}",
        recipients=[email],
        body=body
    )