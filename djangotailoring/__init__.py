# -*- encoding: utf-8 -*-
"""This Django Application is a django-ized wrapper around the tailoring2 and
surveytracking libraries to make integration into a django project as simple
and straight-forward as possible."""

__author__ = u'Dennis O’Reilly <doreilly@umich.edu>'
__version_info__ = (0, 5, 0)
__version__ = '.'.join(str(i) for i in __version_info__)

from djangotailoring.project import getproject, absify, getsubjectloader
from djangotailoring.project import project_document_path, project_tailoring_doc
from djangotailoring.tailoringrequest import TailoringRequest
