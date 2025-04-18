# store_admin/templatetags/form_filters.py
import re

from django import template
from django.forms.boundfield import BoundField
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    if not isinstance(field, BoundField):
        return field  # safely return the original if not a field

    existing_classes = field.field.widget.attrs.get('class', '')
    new_class = f"{existing_classes} {css_class}".strip()
    return field.as_widget(attrs={**field.field.widget.attrs, 'class': new_class})


@register.filter(name='add_label_class')
def add_label_class(label_tag, css_class):
    """Adds CSS class to Django label_tag output."""
    # Inject class into label HTML string
    return mark_safe(re.sub(r'<label(.*?)>', fr'<label\1 class="{css_class}">', label_tag))