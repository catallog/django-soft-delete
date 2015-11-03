# -*- coding: utf-8 -*-
# @Date    : 2015-10-29 15:47:16
# @Author  : Rafael Fernandes (basask@collabo.com.br)
# @Link    : http://www.collabo.com.br/

from __future__ import unicode_literals

from django.db import models
from softdelete import managers
from django.utils import timezone


_call = lambda inst, method: hasattr(inst, method) and getattr(inst, method)()


class SoftDeleteModel(models.Model):

    objects = managers.SoftDeleteManager()
    raw_objects = models.Manager()

    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta(object):
        abstract = True


    def delete(self, *args, **kwargs):
        self.cascade_delete()

    def undelete(self):
        self.cascade_undelete()


    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def soft_undelete(self):
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        return super(SoftDeleteModel, self).delete()

    def cascade_delete(self):
        self.chain_action('delete')
        self.soft_delete()

    def cascade_undelete(self):
        self.chain_action('undelete')
        self.soft_undelete()


    def chain_action(self, method_name):
        for relation in self._meta.get_all_related_objects():
            accessor = relation.get_accessor_name()
            related_instances = getattr(self, accessor, None)
            if related_instances:
                if issubclass(related_instances.__class__, SoftDeleteModel):
                    _call(related_instances, method_name)
                elif hasattr(related_instances, 'raw_all'):
                    for indirect in related_instances.raw_all().filter(**{ accessor: self}):
                        _call(indirect, method_name)
