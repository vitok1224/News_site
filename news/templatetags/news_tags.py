from django import template
from news.models import Category
from django.db.models import *
register = template.Library()


@register.simple_tag(name='get_categories_tag')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/../../templates/inc/list_categories.html', name='show_categories', )
def show_categories():
    categories = Category.objects.annotate(count=Count('news', filter=F('news__is_published'))).filter(count__gt=0)
    return {'categories': categories}
