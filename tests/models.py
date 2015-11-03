# -*- coding: utf-8 -*-
# @Date    : 2015-11-03 14:24:10
# @Author  : Rafael Fernandes (basask@collabo.com.br)
# @Link    : http://www.collabo.com.br/

from __future__ import unicode_literals

from softdelete.models import SoftDeleteModel
from django.db import models


class TestModel(SoftDeleteModel):
    name = models.CharField(max_length=30)


class TestOneToMany(SoftDeleteModel):
    name = models.CharField(max_length=30)
    ref = models.OneToOneField(TestModel, null=False, blank=False)

class TestManyToMany(SoftDeleteModel):
    name = models.CharField(max_length=30)
    rigth = models.ForeignKey(TestModel, related_name='rigth', null=False, blank=False)
    left = models.ForeignKey(TestModel, related_name='left', null=False, blank=False)


class TestNoSubclassReference(models.Model):
    name = models.CharField(max_length=30)
    ref = models.OneToOneField(TestModel, null=False, blank=False)
