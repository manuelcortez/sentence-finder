# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class phrase(models.Model):
    """ Default model created for a sentence. It contains just language and the sentence itself.
    This model is not exposed to the admin interface because it is not intended to be filled that way, see management/commands/import.phrases for  more details."""

    language = models.CharField(max_length=3)
    phrase = models.CharField(max_length=64*1024)