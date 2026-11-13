Django Soft Delete
============

[![Build Status](https://travis-ci.org/collabo-br/django-soft-delete.svg?branch=master)](https://travis-ci.org/collabo-br/django-soft-delete)
[![codecov](https://codecov.io/gh/collabo-br/django-soft-delete/branch/master/graph/badge.svg)](https://codecov.io/gh/collabo-br/django-soft-delete)



Django Soft Delete gives Django models the ability to soft delete(logical delete). it also gives the ability to restore or undelete soft-deleted instances.

Basic usage
============

1. Clone this repo and then ``$pip install django-soft-delete``
1. Add `django_softdelete` to INSTALLED_APPS
1. Inherit all models you want to have this functionality from softdelete.models.SoftDeleteModel

```bash

>>> MyModel.objects.create(name='Anakin')
>>> MyModel.objects.create(name='Luke')
>>> MyModel.objects.create(name='Yoda')

>>> luke  = MyModel.objecs.filter(name='Luke')
>>> MyModel.objecs.filter(name='Luke').delete()

>>> MyModel.objects.count()
2

>>> MyModel.raw_objects.count()
3

>>> MyModel.objects.get(id=luke.id).undelete()
>>> MyModel.objects.count()
3

```

Samples
============

```python
from softdelete.models import SoftDeleteModel


class MyModel(SoftDeleteModel):
    name = models.CharField(max_length=30)
```

You can also use the SoftDelete django manager to extends your custom manager funcionalities. Do it like so:

```python
#my_model_manager.py
from softdelete.managers import SoftDeleteManager


class MyModelManager(SoftDeleteManager):

    def create_john_smith(self):
        self.model.objects.create(name='Jonh Smith')


#my_model.py
from django.db import models
from my_model_manager import MyModelManager


class MyModel(SoftDeleteModel):
    name = models.CharField(max_length=30)

    objects = models.Manager()
    my_manager = MyModelManager()

```

It's possible to have access to delete instances through an alternative manager `` raw_objects``

```python
    for inst in MyModel.raw_objects.all():
        print inst.name
```
