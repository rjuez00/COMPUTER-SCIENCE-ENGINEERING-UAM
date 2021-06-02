# Uncomment if you want to run tests in transaction mode with a final rollback
# from django.test import TestCase
# uncomment this if you want to keep data after running tests
from unittest import TestCase

from django.test import Client
from django.urls import reverse
from populate_rango import populate
from rango.models import Category

class Chapter6FormTests(TestCase):

    def setUp(self):
        self.client = Client()
        try:
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')


    def get_category(self, name):
        try:
            cat = Category.objects.get(name=name)
        except Category.DoesNotExist:
            cat = None
        return cat

    def test_forms_exist(self):
        # Check forms are defined
        try:
            from rango.forms import PageForm
            from rango.forms import CategoryForm
            PageForm()
            CategoryForm()
        except ImportError:
            self.assertTrue(False,
                 'The module forms does not exist')
        except NameError:
            self.assertTrue(False,
                 'The class PageForm/CategoryForm does not exist or is not correct')
        except Exception:
            print('Something else went wrong :-(')
