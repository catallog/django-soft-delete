# -*- coding: utf-8 -*-
# @Date    : 2015-11-03 14:24:10
# @Author  : Rafael Fernandes (basask@collabo.com.br)
# @Link    : http://www.collabo.com.br/

from __future__ import unicode_literals

from softdelete.models import SoftDeleteModel
from django.db import models


class NameMixin(models.Model):
    name = models.CharField(max_length=30)
    class Meta:
        abstract = True

class TestModel(NameMixin, SoftDeleteModel):
    pass


class TestRegularModel(NameMixin):
    pass


class TestOneToMany(NameMixin, SoftDeleteModel):
    ref = models.OneToOneField(TestModel, null=False, blank=False)


class TestManyToMany(NameMixin, SoftDeleteModel):
    rigth = models.ForeignKey(TestModel, related_name='rigth', null=False, blank=False)
    left = models.ForeignKey(TestModel, related_name='left', null=False, blank=False)


class TestNoSubclassReference(NameMixin):
    ref = models.OneToOneField(TestModel, null=False, blank=False)


class TestMixedM2MModel(NameMixin, SoftDeleteModel):
    regular = models.ForeignKey(TestRegularModel, null=False, blank=False)
    soft = models.ForeignKey(TestModel, null=False, blank=False)
