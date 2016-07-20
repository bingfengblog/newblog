#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import markdown2
import markdown
from django import template
from django.template.defaultfilters import stringfilter
#from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def djangomarkdown(value):
    '''
    http://www.dominicrodger.com/django-markdown.html
    '''
    

    return mark_safe(markdown.markdown(value,
                                        extras=["code-friendly"]
                                        )
                     )


if __name__ == "__main__":
    mystring = u'''
### haha

+ aa

**aaa**

<p>aaa</p>

<h1>aa</h1>

    '''
    
    #html = markdown2.markdown(mystring, extras=["xml"])
    html = markdown.markdown(mystring, extras=["code-friendly"])
    print(html)













