from django import template 
from store.models import Category



register = template.Library()

@register.inclusion_tag('includes/department_category_nav.html')
def department_categories_nav():
    categories=Category.objects.all()
    return {'categories':categories}
    


