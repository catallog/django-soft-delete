# -*- coding: utf-8 -*-
# @Date    : 2015-11-03 08:49:20
# @Author  : Rafael Fernandes (basask@collabo.com.br)
# @Link    : http://www.collabo.com.br/

from __future__ import unicode_literals

from django.db import models
from django.test import TestCase
from .models import TestModel
from .models import TestOneToMany
from .models import TestManyToMany
from .models import TestNoSubclassReference


class SoftDeleteTestCase(TestCase):

    def setUp(self):
        mod_a = TestModel.objects.create(name='Name_A')
        mod_b = TestModel.objects.create(name='Name_B')
        mod_c = TestModel.objects.create(name='Name_C')
        mod_d = TestModel.objects.create(name='Name_D')
        mod_e = TestModel.objects.create(name='Name_E')


        TestOneToMany.objects.create(name='O2M_A', ref=mod_a)
        TestOneToMany.objects.create(name='O2M_B', ref=mod_b)
        TestOneToMany.objects.create(name='O2M_C', ref=mod_c)
        TestOneToMany.objects.create(name='O2M_D', ref=mod_d)
        TestOneToMany.objects.create(name='O2M_E', ref=mod_e)

        TestNoSubclassReference.objects.create(name='O2M_A', ref=mod_a)
        TestNoSubclassReference.objects.create(name='O2M_B', ref=mod_b)
        TestNoSubclassReference.objects.create(name='O2M_C', ref=mod_c)
        TestNoSubclassReference.objects.create(name='O2M_D', ref=mod_d)
        TestNoSubclassReference.objects.create(name='O2M_E', ref=mod_e)

        TestManyToMany.objects.create(name='M2M_AB', rigth=mod_a, left=mod_b)
        TestManyToMany.objects.create(name='M2M_AC', rigth=mod_a, left=mod_c)
        TestManyToMany.objects.create(name='M2M_BA', rigth=mod_b, left=mod_a)

        TestManyToMany.objects.create(name='M2M_DB', rigth=mod_d, left=mod_e)
        TestManyToMany.objects.create(name='M2M_ED', rigth=mod_e, left=mod_d)


    def _assert_count(self, soft, real=None):
        real = real or soft
        self.assertEqual(TestModel.objects.count(), soft)
        self.assertEqual(TestModel.raw_objects.count(), real)

    def test_insert_quantity_consistency(self):
        self._assert_count(5)
        self.assertEqual( TestOneToMany.objects.count(), 5)
        self.assertEqual( TestManyToMany.objects.count(), 5)
        self.assertEqual( TestNoSubclassReference.objects.count(), 5)

        TestModel.objects.create(name='Name_F')
        self._assert_count(6)


    def test_insert_mixed_manager(self):
        self._assert_count(5)

        TestModel.objects.create(name='Name_F')
        self._assert_count(6)

        TestModel.raw_objects.create(name='Name_G')
        self._assert_count(7)

    def test_model_logical_deletion(self):
        mod = TestModel.objects.filter(name='Name_A').last()
        mod.delete()
        self._assert_count(4, 5)

        mod = TestModel.objects.get(id='2')
        mod.delete()
        self._assert_count(3, 5)

    def test_model_hard_deletion(self):
        mod = TestModel.raw_objects.filter(name='Name_A').last()
        mod.hard_delete()
        self._assert_count(4)

        mod = TestModel.raw_objects.get(id='2')
        mod.hard_delete()
        self._assert_count(3)

    def test_manager_softdelete(self):
        TestModel.objects.filter(id=2).delete()
        self._assert_count(4, 5)

        TestModel.objects.last().delete()
        self._assert_count(3, 5)

        TestModel.objects.first().delete()
        self._assert_count(2, 5)

    def test_manager_harddeletion(self):
        TestModel.objects.last().hard_delete()
        self._assert_count(4)

    def test_raw_all(self):

        all = TestModel.objects.raw_all()
        self.assertEqual(len(all), 5)

        TestModel.objects.last().delete()
        all = TestModel.objects.raw_all()
        self.assertEqual(len(all), 5)

    def test_undelete(self):
        self._assert_count(5)

        TestModel.objects.filter(name='Name_A').last().delete()
        self._assert_count(4, 5)

        mod = TestModel.objects.get(name='Name_A')
        self.assertTrue(issubclass(mod.__class__, TestModel))
        self._assert_count(4, 5)

        mod.undelete()
        self._assert_count(5)

    def test_cascade_delete(self):

        self.assertEqual(TestManyToMany.objects.count(), 5)
        self.assertEqual(TestOneToMany.objects.count(), 5)

        TestModel.objects.filter(name='Name_A').delete()
        self._assert_count(4, 5)

        self.assertEqual(TestNoSubclassReference.objects.count(), 5)
        self.assertEqual(TestOneToMany.objects.count(), 4)
        self.assertEqual(TestManyToMany.objects.count(), 2)

        TestModel.objects.filter(name='Name_E').delete()

        self.assertEqual(TestNoSubclassReference.objects.count(), 5)
        self.assertEqual(TestOneToMany.objects.count(), 3)
        self.assertEqual(TestManyToMany.objects.count(), 0)


    def test_cascade_undelete(self):

        self._assert_count(5)

        TestModel.objects.filter(name='Name_E').delete()
        self._assert_count(4, 5)
        self.assertEqual(TestNoSubclassReference.objects.count(), 5)
        self.assertEqual(TestOneToMany.objects.count(), 4)
        self.assertEqual(TestManyToMany.objects.count(), 3)

        TestModel.objects.get(name='Name_E').undelete()
        self._assert_count(5)
        self.assertEqual(TestNoSubclassReference.objects.count(), 5)
        self.assertEqual(TestOneToMany.objects.count(), 5)
        self.assertEqual(TestManyToMany.objects.count(), 5)



