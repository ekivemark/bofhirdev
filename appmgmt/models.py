# Create your models here.
# apps.appmgmt.models

# Extend the Django OAuth Provider Application Model
# Author: Mark Scrimshire (c) @ekivemark

from django.conf import settings
from django.db import models
from oauth2_provider.models import AbstractApplication

# Modify settings.py wih OAUTH2_PROVIDER_APPLICATION_MODEL=

class BBApplication(AbstractApplication):
    # Extension of the OAuth2 Application to add extra fields.

    organization = models.ForeignKey('Organization',
                                     blank=True,
                                     null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              blank=True,
                              null=True)
    logo = models.ImageField(blank=True, null=True)
    agree = models.BooleanField(verbose_name='Agreed to T&Cs',
                                default=False)
    agree_version = models.CharField(max_length=10,
                                     verbose_name='T&C Version',
                                     blank=True,
                                     null=True)
    agree_date = models.DateTimeField(verbose_name='Date T&C Agreed',
                                      blank=True,
                                      null=True, default=None)
    privacy_url = models.URLField(blank=True)
    support_url = models.URLField(blank=True)

    def privacy(self):
        return self.privacy_url

    def support(self):
        return self.support_url

    def terms_signed(self):
        if self.agree:
            terms = "Agreed to Terms and Conditions (v.%s) on %s" % (self.agree_version,
                                                                     self.agree_date)
            return terms
        return None


class Organization(models.Model):
    # We need an Organization model to coordinate applications for a user
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='+',
                              blank=True,
                              null=True,
                              verbose_name="Application Owner"
                              )
    name = models.CharField(max_length=100,
                            verbose_name='Organization Name')
    domain = models.URLField()
    trusted = models.BooleanField(default=False)
    trusted_until = models.DateTimeField(blank=True, null=True)
    developers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='+',
                                        blank=True)

    def __str__(self):
        return self.name

    def url(self):
        return self.domain

    def trust(self):
        return self.trusted

    def owned_by(self):
        return self.owner.email
