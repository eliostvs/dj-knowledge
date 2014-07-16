from __future__ import unicode_literals

from django.test import TestCase

from model_mommy import mommy

from kb.base import test


class CategoryModelTestCase(test.PermalinkTestMixin,
                            test.TimeStampedMixin,
                            test.AuthorTestMixin,
                            test.SeqAssertionMixin,
                            TestCase):

    from kb.models import Category

    model = Category

    def create_instance(self, **kwargs):
        return mommy.make('Category', **kwargs)

    def test_create_new_category(self):
        category = self.create_instance(description='foo')

        self.assertTrue(category.name)
        self.assertTrue(category.name, str(category))
        self.assertTrue(category.description, 'foo')

    def test_subcategory(self):
        parent = self.create_instance()

        s1 = mommy.make_recipe('kb.tests.category_without_articles',
                               parent=parent)

        s2 = mommy.make_recipe('kb.tests.category_with_articles',
                               parent=parent)

        self.assertSeqEqual(parent.subcategories.all(), [s1, s2])

    def test_absolute_url(self):
        category = self.create_instance(slug='spam')
        self.assertEqual(category.get_absolute_url(), '/category/spam/')

    def test_articles_count(self):
        category = mommy.make_recipe('kb.tests.category_with_articles')

        self.assertEqual(category.articles.count(), 2)
        self.assertEqual(category.published_articles(), 1)