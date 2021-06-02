from rango.models import Category, Page
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone


class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        Ensures the number of views received
        for a Category are positive or zero.
        """

        category = Category(name='test', views=-1, likes=0)
        category.save()
        self.assertEqual((category.views >= 0), True)

    def test_slug_line_creation(self):
        """
        Checks to make sure that when a category is created, an
        appropriate slug is created.
        Example: "Random Category String" should be "random-category-string".
        """

        category = Category(name='Random Category String')
        category.save()
        self.assertEqual(category.slug, 'random-category-string')


class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """
        If no categories exist, the appropriate message should be displayed.
        """
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present")
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        """
        Checks whether categories are displayed correctly when present.
        """
        add_category('Python', 1, 1)
        add_category('C++', 1, 1)
        add_category('Erlang', 1, 1)

        response = self.client.get(reverse('rango:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")
        self.assertContains(response, "C++")
        self.assertContains(response, "Erlang")
        num_categories = len(response.context['categories'])
        self.assertEquals(num_categories, 3)


class PageAccessTests(TestCase):

    def test_timestamp_update(self):
        category = add_category("FilmCategory", 56, 21)
        page = add_page(category, "FilmPage",
                        "https://www.bladerunner2049movie.com")
        oldtime = page.last_visit
        self.client.get(reverse('rango:goto'), {'page_id': page.id})
        page.refresh_from_db()
        self.assertGreater(page.last_visit, oldtime)

    def test_time_not_future(self):
        category = add_category("FilmCategory")
        page = add_page(category, "FilmPage",
                        "https://www.bladerunner2049movie.com")
        self.assertTrue(page.last_visit < timezone.now())


# extracted from populate
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_category(name, views=0, likes=0):
    category = Category.objects.get_or_create(name=name)[0]
    category.views = views
    category.likes = likes
    category.save()
    return category
