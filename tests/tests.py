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
from .models import TestRegularModel
from .models import TestMixedM2MModel


class SoftDeleteTestCase(TestCase):

    def setUp(self):
        soft_a = TestModel.objects.create(name='Name_A')
        soft_b = TestModel.objects.create(name='Name_B')
        soft_c = TestModel.objects.create(name='Name_C')
        soft_d = TestModel.objects.create(name='Name_D')
        soft_e = TestModel.objects.create(name='Name_E')

        reg_a = TestRegularModel.objects.create(name='Name_A')
        reg_b = TestRegularModel.objects.create(name='Name_B')
        reg_c = TestRegularModel.objects.create(name='Name_C')
        reg_d = TestRegularModel.objects.create(name='Name_D')
        reg_e = TestRegularModel.objects.create(name='Name_E')

        TestOneToMany.objects.create(name='O2M_A', ref=soft_a)
        TestOneToMany.objects.create(name='O2M_B', ref=soft_b)
        TestOneToMany.objects.create(name='O2M_C', ref=soft_c)
        TestOneToMany.objects.create(name='O2M_D', ref=soft_d)
        TestOneToMany.objects.create(name='O2M_E', ref=soft_e)

        TestNoSubclassReference.objects.create(name='O2M_A', ref=soft_a)
        TestNoSubclassReference.objects.create(name='O2M_B', ref=soft_b)
        TestNoSubclassReference.objects.create(name='O2M_C', ref=soft_c)
        TestNoSubclassReference.objects.create(name='O2M_D', ref=soft_d)
        TestNoSubclassReference.objects.create(name='O2M_E', ref=soft_e)

        TestManyToMany.objects.create(name='M2M_AB', rigth=soft_a, left=soft_b)
        TestManyToMany.objects.create(name='M2M_AC', rigth=soft_a, left=soft_c)
        TestManyToMany.objects.create(name='M2M_BA', rigth=soft_b, left=soft_a)

        TestManyToMany.objects.create(name='M2M_DB', rigth=soft_d, left=soft_e)
        TestManyToMany.objects.create(name='M2M_ED', rigth=soft_e, left=soft_d)

        TestMixedM2MModel.objects.create(name='MX2M_AA', regular=reg_a, soft=soft_a)
        TestMixedM2MModel.objects.create(name='MX2M_BB', regular=reg_b, soft=soft_b)
        TestMixedM2MModel.objects.create(name='MX2M_CC', regular=reg_c, soft=soft_c)
        TestMixedM2MModel.objects.create(name='MX2M_DD', regular=reg_d, soft=soft_d)
        TestMixedM2MModel.objects.create(name='MX2M_EE', regular=reg_e, soft=soft_e)

        TestMixedM2MModel.objects.create(name='MX2M_AB', regular=reg_a, soft=soft_b)
        TestMixedM2MModel.objects.create(name='MX2M_AC', regular=reg_a, soft=soft_c)


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

    def test_model_hard_deletion(self):
        mod = TestModel.raw_objects.filter(name='Name_A').last()
        mod.hard_delete()
        self._assert_count(4)

    def test_manager_softdelete(self):
        TestModel.objects.filter(name='Name_B').delete()
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

        self.assertTrue(mod.is_deleted())
        self.assertTrue(issubclass(mod.__class__, TestModel))
        self._assert_count(4, 5)

        mod.undelete()
        self.assertFalse(mod.is_deleted())
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

    def test_cascade_delete_regular_preserve(self):

        self.assertEqual(TestMixedM2MModel.objects.count(), 7)
        self.assertEqual(TestRegularModel.objects.count(), 5)

        TestModel.objects.filter(name='Name_A').delete()

        self.assertEqual(TestMixedM2MModel.objects.count(), 6)
        self.assertEqual(TestRegularModel.objects.count(), 5)

        TestModel.objects.filter(name='Name_C').delete()

        self.assertEqual(TestMixedM2MModel.objects.count(), 4)
        self.assertEqual(TestRegularModel.objects.count(), 5)

        TestModel.objects.get(name='Name_A').undelete()
        TestModel.objects.get(name='Name_C').undelete()

        self.assertEqual(TestMixedM2MModel.objects.count(), 7)
        self.assertEqual(TestRegularModel.objects.count(), 5)
