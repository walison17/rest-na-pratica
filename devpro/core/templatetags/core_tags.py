from django import template
from django.utils.itercompat import is_iterable
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def query_string(context, **kwargs):
    query_dict = context["request"].GET
    query_dict = query_dict.copy()

    for key, value in kwargs.items():
        if value is None:
            if key in query_dict:
                del query_dict[key]
        elif is_iterable(value) and not isinstance(value, str):
            query_dict.setlist(key, value)
        else:
            query_dict[key] = value
    if not query_dict:
        return ""
    query_string = query_dict.urlencode()
    return f"?{query_string}"


@register.simple_tag(takes_context=True)
def order_query_string(context, field):
    ordering = context['request'].GET.get("order", field)
    if ordering.startswith("-"):
        field_name = ordering[1:]
        order_dir = ""
    else:
        field_name = ordering
        order_dir = "-"

    if field_name != field:
        field_name = field
        order_dir = ""

    new_order_field = f"{order_dir}{field}"
    return query_string(context, order=new_order_field)


@register.simple_tag(takes_context=True)
def order_icon(context, field):
    ordering = context['request'].GET.get("order")
    if not ordering:
        return mark_safe('<i class="fa-solid fa-arrows-up-down"></i>')

    if ordering.startswith("-"):
        field_name = ordering[1:]
        icon = "fa-arrow-down-short-wide"
    else:
        field_name = ordering
        icon = "fa-arrow-up-short-wide"

    if field_name != field:
        icon = "fa-arrows-up-down"

    return mark_safe(f'<i class="fa-solid {icon}"></i>')


class OrderColumn:
    def __init__(self, name, direction):
        self.name = name
        self.direction = direction

    @classmethod
    def from_str(cls, string):
        if string.startswith('-'):
            direction = 'desc'
            name = string[1:]
        else:
            direction = 'asc'
            name = string

        return cls(name, direction)

    @property
    def ascending(self):
        return self.direction == 'asc'

    def __str__(self):
        return f'{self.direction}{self.name}'
