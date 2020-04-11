from django import template

register = template.Library()


@register.filter
def normalize_placeholder_input(field):
    return field.as_widget(attrs={"placeholder": field.label.capitalize(), "class": "form-control"})
