import binascii
import os
from django.db.models import Q
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Token(models.Model):
    """
    The default authorization token model.
    """
    WEB = "WEB"
    SPECTRO_TV = "SPECTRO_TV"
    LOG_SHEET = "LOG_SHEET"
    MELTING_REPORT = "MELTING_REPORT"
    IOT = "IOT"
    DEVICE_TYPES = (
        (WEB, "WEB"),
        (SPECTRO_TV, "SPECTRO_TV"),
        (LOG_SHEET, "LOG_SHEET"),
        (MELTING_REPORT, "MELTING_REPORT"),
        (IOT, "IOT"),
    )
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    device_id = models.CharField(max_length=64, blank=True, null=True)
    device_type = models.CharField(
        choices=DEVICE_TYPES, max_length=32, blank=True, null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = 'drfpasswordless.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class TokenProxy(Token):
    """
    Proxy mapping pk to user pk for use in admin.
    """
    @property
    def pk(self):
        return self.user_id

    class Meta:
        proxy = 'drfpasswordless.authtoken' in settings.INSTALLED_APPS
        abstract = 'drfpasswordless.authtoken' not in settings.INSTALLED_APPS
        verbose_name = "token"
