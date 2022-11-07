from django.contrib.auth.forms import PasswordResetForm
...

class PasswordResetForm(PasswordResetForm):
    def _int(self, *args, **kwargs):
        super (PasswordResetForm, self). _init_(*args, **kwargs)
        
    # captcha = ReCaptchaField(widget=ReCaptchaFieldV2Checkbox())    