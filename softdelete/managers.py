# -*- coding: utf-8 -*-
# @Date    : 2015-10-29 15:49:53
# @Author  : Rafael Fernandes (basask@collabo.com.br)
# @Link    : http://www.collabo.com.br/

from __future__ import unicode_literals

from django.db import models
from django.db.models.query import QuerySet


class SoftDeleteQueryMixin(object):
    def delete(self):
        for model_instance in self.all():
            model_instance.delete()

    def undelete(self):
        for model_instance in self.raw_all():
            model_instance.undelete()


class SoftDeleteQuerySet(SoftDeleteQueryMixin, QuerySet):
    pass


class SoftDeleteManager(SoftDeleteQueryMixin, models.Manager):

    def get_raw_queryset(self):
        return super(SoftDeleteManager, self).get_queryset() if self.model else None

    def get_queryset(self):
        if self.model:
            query_set = SoftDeleteQuerySet(self.model, using=self._db)
            return query_set.exclude(deleted_at__isnull=False)

    def get(self, *args, **kwargs):
        return self.get_raw_queryset().get(*args, **kwargs)

    def raw_all(self, *args, **kwargs):
        return self.get_raw_queryset().all(*args, **kwargs)
