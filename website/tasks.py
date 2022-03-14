from celery import shared_task
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template import loader

@shared_task
def send_welcome_mail(name, email):
    email_template = get_template('website/email/welcome.html')
    d = {'name': name}
    subject, from_email, to = 'Welcome to KnowledgeDunia.com', 'abhinav.raj.9a@gmail.com', email
    html_content = email_template.render(d)
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return 'E-mail send successfully'


@shared_task
def send_forgot_password_mail(self, subject_template_name, email_template_name,
              context, from_email, to_email, html_email_template_name=None):
    """
    Send a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(
        subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

    email_message.send()
    return 'E-mail send successfully'
