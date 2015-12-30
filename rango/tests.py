from django.test import TestCase
from rango.models import Category, Page
from django.core.urlresolvers import reverse
import datetime

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

def add_page(category, title, url, first_visit, last_visit):
    p = Page.objects.get_or_create(category=category, title=title, url=url)[0]
    p.first_visit = first_visit
    p.last_visit = last_visit
    p.save()
    return p

class CategoryMethodTests(TestCase):

    def test_ensure_views_are_positive(self):

        """
                ensure_views_are_positive should results True for categories where views are zero or positive
        """
        cat = Category(name='test',views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """
        slug_line_creation checks to make sure that when we add a category an appropriate slug line is created
        i.e. "Random Category String" -> "random-category-string"
        """

        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')
        
class IndexViewTests(TestCase):

    def test_index_view_with_no_categories(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """

        add_cat('test',1,1)
        add_cat('temp',1,1)
        add_cat('tmp',1,1)
        add_cat('tmp test temp',1,1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")

        num_cats =len(response.context['categories'])
        self.assertEqual(num_cats , 4)

class visitTests(TestCase):

    def test_last_visit_not_future(self):
        cat = Category(name='test')
        cat.save()
        futuredate = datetime.date.today() + datetime.timedelta(days=30)
        p=add_page (cat, 'last_future', 'www.exemple.it', first_visit=datetime.date.today(), last_visit = futuredate)
        self.assertEqual(p.last_visit, datetime.date.today())
        
    def test_first_visit_not_future(self):
        cat = Category(name='test')
        cat.save()
        futuredate = datetime.date.today() + datetime.timedelta(days=30)
        p=add_page (cat, 'first_future', 'www.exemple.it', first_visit=futuredate, last_visit = futuredate)
        self.assertEqual(p.first_visit, datetime.date.today())
        self.assertEqual(p.last_visit, datetime.date.today())

    def test_first_visit_before_last_visit(self):
        cat = Category(name='test')
        cat.save()
        firstdate = datetime.date.today() + datetime.timedelta(days=-3)
        lastdate = datetime.date.today() + datetime.timedelta(days=-5)
        p=add_page (cat, 'first_future', 'www.exemple.it', first_visit=firstdate, last_visit = lastdate)
        self.assertEqual(p.first_visit, p.last_visit)
        
