
#!/usr/bin/env python
"""
This module contains tests for djenerator app.
"""
import models as mdls
from django.db import models
from django.test import TestCase
from generate_test_data import field_sample_values
from model_reader import field_type
from model_reader import is_auto_field
from model_reader import is_instance_of_model
from model_reader import is_related
from model_reader import list_of_fields
from model_reader import list_of_models
from model_reader import module_import
from model_reader import names_of_fields
from model_reader import relation_type
from models import CycleA
from models import CycleB
from models import CycleC
from models import CycleD
from models import CycleE
from models import CycleF
from models import ExtendAbstract
from models import ExtendSuperClass
from models import ExtendingModel
from models import NotExtendingModel
from models import ProxyExtend
from models import SuperAbstract
from models import SuperClass
from models import TestModel0
from models import TestModel1
from models import TestModelA
from models import TestModelB
from models import TestModelC
from models import TestModelD
from models import TestModelE
from models import TestModelFields
from models import TestModelFieldsTwo
from models import TestModelX
from models import TestModelY


class TestInstanceOfModel(TestCase):
    def test(self):
        models = [TestModel0, TestModel1, TestModelA, TestModelB, TestModelC,
                  TestModelD, TestModelE, TestModelX, TestModelY, ExtendingModel]
        for model in models:
            self.assertTrue(is_instance_of_model(model))
        self.assertFalse(is_instance_of_model(NotExtendingModel))
        def not_extending_model_function():
            pass
        
        self.assertFalse(is_instance_of_model(not_extending_model_function))


class TestListOfModels(TestCase):
    def test(self):
        self.assertEqual(set([ExtendingModel, TestModel0, TestModel1, 
                              TestModelA, TestModelB, TestModelC, TestModelD, 
                              TestModelE, TestModelX, TestModelY, 
                              TestModelFields, SuperClass, ExtendAbstract, 
                              ExtendSuperClass, ProxyExtend, SuperAbstract, 
                              TestModelFieldsTwo, CycleA, CycleB, CycleC, 
                              CycleD, CycleE, CycleF]), 
                              set(list_of_models(mdls, keep_abstract=True)))
        self.assertEqual(set([ExtendingModel, TestModel0, TestModel1, 
                              TestModelA, TestModelB, TestModelC, TestModelD, 
                              TestModelE, TestModelX, TestModelY, 
                              TestModelFields, SuperClass, ExtendAbstract, 
                              ExtendSuperClass, TestModelFieldsTwo, ProxyExtend,
                              CycleA, CycleB, CycleC, CycleD, CycleE, CycleF]), 
                              set(list_of_models(mdls)))


class TestListOfFields(TestCase):
    def test(self):
        self.assertTrue(all([isinstance(*x) 
                             for x in zip(list_of_fields(TestModel1), 
                             [models.AutoField, models.CharField,
                              models.IntegerField, models.ForeignKey])]))
        self.assertTrue(all([isinstance(*x) 
                             for x in zip(list_of_fields(TestModel0),
                             [models.AutoField, models.BooleanField,
                              models.EmailField])]))
        self.assertTrue(all([isinstance(*x) 
                             for x in zip(list_of_fields(TestModelE),
                             [models.AutoField, models.OneToOneField,
                              models.ForeignKey, models.IntegerField,
                              models.ManyToManyField])]))


class TestNamesOfFields(TestCase):
    def test(self):
        self.assertEqual(['id', 'field1E', 'field3E', 'field4E', 'field2E'],
                          names_of_fields(TestModelE))
        self.assertEqual(['id', 'field1', 'field2', 'field3'],
                          names_of_fields(TestModel1))
        self.assertEqual(['id', 'field1', 'field2'],
                          names_of_fields(TestModel0))

class TestFieldType(TestCase):
    def test(self):
        self.assertEqual(field_type(models.CharField()),
                         'CharField')
        self.assertEqual(field_type(models.IntegerField()),
                         'IntegerField')
        self.assertEqual(field_type(models.EmailField()),
                         'CharField')
        self.assertEqual(field_type(models.BooleanField()),
                         'BooleanField')
        self.assertEqual(field_type(models.ForeignKey(ExtendingModel)),
                         'ForeignKey')
        self.assertEqual(field_type(models.OneToOneField(ExtendingModel)),
                         'OneToOneField')
        self.assertEqual(field_type(models.ManyToManyField(ExtendingModel)),
                         'ManyToManyField')


class TestIsAutoField(TestCase):
    def test(self):
        self.assertTrue(is_auto_field(models.AutoField(primary_key=True)))
        self.assertFalse(is_auto_field(models.CharField()))
        self.assertFalse(is_auto_field(models.BooleanField()))
        self.assertFalse(is_auto_field(models.IntegerField()))
        self.assertFalse(is_auto_field(models.ForeignKey(ExtendingModel)))


class TestIsRelated(TestCase):
    def test(self):
        self.assertTrue(is_related(models.ForeignKey))
        self.assertTrue(is_related(models.OneToOneField))
        self.assertTrue(is_related(models.ManyToManyField))
        self.assertFalse(is_related(models.CharField))
        self.assertFalse(is_related(models.BooleanField))
        self.assertFalse(is_related(models.EmailField))
        self.assertFalse(is_related(models.IntegerField))


class TestRelationType(TestCase):
    def test(self):
        self.assertEqual(relation_type(models.OneToOneField(ExtendingModel)),
                         'OneToOneRel')
        self.assertEqual(relation_type(models.ManyToManyField(ExtendingModel)),
                         'ManyToManyRel')
        self.assertEqual(relation_type(models.ForeignKey(ExtendingModel)),
                         'ManyToOneRel')


class TestModuleImport(TestCase):
    def test(self):
        self.assertEqual(mdls, module_import('djenerator.models'))
 
 
class TestListOfSampleFieldValues(TestCase):
    def test(self):
        Y = list_of_fields(TestModelY)
        X = list_of_fields(TestModelX)
        A = list_of_fields(TestModelA)
        B = list_of_fields(TestModelB)
        C = list_of_fields(TestModelC)
        D = list_of_fields(TestModelD)
        E = list_of_fields(TestModelE)
        self.assertFalse(field_sample_values(X[0]))
        self.assertEqual(field_sample_values(Y[1]), [2, 3, 5, 7, 11, 13])
        self.assertEqual(field_sample_values(Y[2]), ['MMa', 'XXa', 'azz'])
        self.assertEqual(field_sample_values(X[1]), 
                         [x * x * x for x in range(10)])
        self.assertEqual(field_sample_values(E[3]), [1000000009, 1000003, 101])
        self.assertEqual(field_sample_values(D[1]), 
                         [x * x * x for x in range(10)])
        self.assertEqual(field_sample_values(C[1]), 
                         ['Hello I am C', 'MUHAHAHAHAHA', 'CCCC', '^_^'])
        self.assertEqual(field_sample_values(B[1]), 
                         ['Hello Universe', 'Hello Parallel Universe!'])
        self.assertEqual(field_sample_values(A[1]), 
                         ['Hello World', 'Hello Africa', 'axxx!!'])
        self.assertEqual(field_sample_values(A[2]), 
                         ['Hello Second Field', 'field 2'])
        a = TestModelX(field1X=12)
        b = TestModelX(field1X=15)
        a.save()
        b.save()
        self.assertEqual((field_sample_values(models.ForeignKey(TestModelX))), 
                         ([a, b]))
        fld = models.ManyToManyField(TestModelX)
        self.assertTrue(all([x in [a, b] for x in field_sample_values(fld)[0]]))
        vals = [int (x) for x in field_sample_values(list_of_fields(CycleF)[2])]
        self.assertEqual(vals, range(4000, 5000))



