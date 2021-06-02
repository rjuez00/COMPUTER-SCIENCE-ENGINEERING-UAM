import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/3/tutorial/',
         'views': random.randint(1, 200)},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/',
         'views': random.randint(1, 200)},
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorials/python/',
         'views': random.randint(1, 200)}
                    ]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
         'views': random.randint(1, 200)},
        {'title': 'Django Rocks',
         'url': 'http://www.djangorocks.com/',
         'views': random.randint(1, 200)},
        {'title': 'How to Tango with Django',
         'url': 'http://www.tangowithdjango.com/',
         'views': random.randint(1, 200)}
                    ]

    other_pages = [
        {'title': 'Bottle',
         'url': 'http://bottlepy.org/docs/dev/',
         'views': random.randint(1, 200)},
        {'title': 'Flask',
         'url': 'http://flask.pocoo.org',
         'views': random.randint(1, 200)}
                    ]

    python_other_pages = [
        {'title': 'PyCrypto',
         'url': 'https://pypi.org/project/pycryptodome/',
         'views': random.randint(1, 200)}
    ]


    film_pages = [
        {'title': 'Blade Runner 2049',
         'url': 'http://www.youtube.com/watch?v=gCcx85zbxz4',
         'views': random.randint(1, 200)},
        {'title': 'Drive',
         'url': 'http://www.youtube.com/watch?v=KBiOF3y1W0Y',
         'views': random.randint(1, 200)},
        {'title': 'Joker',
         'url': 'https://www.youtube.com/watch?v=ygUHhImN98w',
         'views': random.randint(1, 200)},
        {'title': 'Alicia en el país de las maravillas',
         'url': 'https://www.youtube.com/watch?v=KLIqErnQCuw',
         'views': random.randint(1, 200)},
                    ]

    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            'Other Frameworks': {'pages': other_pages,
                                 'views': 32, 'likes': 16},
            'Other Python Libraries': {'pages': python_other_pages,
                                       'views': 4, 'likes': 2},
            'Films': {'pages': film_pages, 'views': 200, 'likes': 1000}
            }

    # If you want to add more categories or pages,
    # add them to the dictionaries above.
    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print('- {0} - {1}'.format(str(c), str(p)))


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]

    c.views = views
    c.likes = likes
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
