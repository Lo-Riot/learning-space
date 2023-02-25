from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_verification_email(
    from_email: str, to_emails: list[str], verification_link: str
) -> None:
    send_mail(
        "Verify your Learning Space account",
        "Follow this link to verify your "
        f"Learning Space account: \n{verification_link}",
        from_email,
        to_emails,
        fail_silently=True
    )
