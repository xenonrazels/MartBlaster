from django import template
from store.models import Main_Navigation

register =template.Library()

@register.inclusion_tag('includes/main_nav.html')
def main_nav():
    main_nav=Main_Navigation.objects.all()
    return {'main_nav':main_nav}
    
    


