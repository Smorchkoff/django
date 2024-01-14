from django import template
import hello.views as views

register = template.Library()


@register.simple_tag()
def get_db():
    return views.data_db

@register.inclusion_tag('list_db.html')
def show_db(selected=0):
    db = views.data_db
    return {'db':db, "selected":selected}
