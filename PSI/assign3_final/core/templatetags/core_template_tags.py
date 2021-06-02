from django import template

register = template.Library()


"""
EXAMPLE FROM PAST PRACTICE:
@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),
            'current_category': current_category}"""
