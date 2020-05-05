from django.conf.urls import url
from django import template
import re

register = template.Library()

@register.filter
def add_link_2(value):
    main_text = value.main_text
    tags_2 = value.tag_set_2.all()

    for tag_2 in tags_2:
        main_text = re.sub(r'\#'+tag_2.tag_name_2+r'\b', '<a href="/intworldapp/explore/tags_2/'+tag_2.tag_name_2+'">#'+tag_2.tag_name_2+'</a>', main_text)
    return main_text