from __future__ import unicode_literals

from django.views.generic import TemplateView

from haystack.views import SearchView

from .article.views import (ArticleCreateView, ArticleDeleteView,
                            ArticleDetailView, ArticleListView,
                            ArticleUpdateView)
from .base.views import AddSearchFormToContextMixin
from .category.views import (CategoryCreateView, CategoryDeleteView,
                             CategoryDetailView, CategoryListView,
                             CategoryUpdateView)
from .forms import SimpleSearchForm
from .models import Article, Category

__all__ = [
    'ArticleListView',
    'ArticleDetailView',
    'ArticleCreateView',
    'ArticleDeleteView',
    'ArticleUpdateView',
    'CategoryListView',
    'CategoryDetailView',
    'CategoryCreateView',
    'CategoryUpdateView',
    'CategoryDeleteView',
    'Homepage',
    'KnowledgeSearchView',
    'search_view',
]


class Homepage(AddSearchFormToContextMixin,
               TemplateView):

    template_name = 'knowledge/index.html'

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        context['categories'] = self.get_categories()
        context['new_articles'] = self.get_new_articles()
        context['top_viewed_articles'] = self.get_top_viewed_articles()
        context['top_rated_articles'] = self.get_top_rated_articles()
        return context

    def get_categories(self):
        return Category.objects.categories(self.request.user.is_anonymous())

    def get_new_articles(self):
        return Article.objects.new(self.request.user.is_anonymous())

    def get_top_viewed_articles(self):
        return Article.objects.top_viewed(self.request.user.is_anonymous())

    def get_top_rated_articles(self):
        return Article.objects.top_rated(self.request.user.is_anonymous())


class KnowledgeSearchView(SearchView):
    pass

search_view = KnowledgeSearchView(form_class=SimpleSearchForm)
