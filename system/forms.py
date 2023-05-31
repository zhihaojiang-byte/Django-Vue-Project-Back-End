import random

from django import forms
from django.core.cache import cache
from django.core.mail import send_mail

from djangoProject import settings


class VerificationCodeForm(forms.Form):
    email = forms.EmailField(required=True, max_length=100, error_messages={
        'required': "E-mail address is required",
        'max_length': "E-mail address is too long, please use another one."
    })

    def send_verification_code(self):
        try:
            # generate verification code as a 4 digits string
            verification_code = str(random.randint(0, 9999)).rjust(4, "0")
            email = self.cleaned_data.get('email', None)

            # send email to user
            send_mail(
                subject='Welcome to Fun Booking.',
                message=f'Your verification code is {verification_code}. \n'
                        f'The verification code will be expired in 5 minutes.\n'
                        f'If you are not registering Fun Booking, please ignore this email.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            # store verification code in redis, set expired in 5 minutes
            timeout = 5*60
            cache.set(email, verification_code, timeout=timeout)
            return {
                'email': email,
                'timeout': timeout,
            }
        except Exception as e:
            print(e)
            return None



