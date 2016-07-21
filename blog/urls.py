from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^$',                                                         views.index,   name='index'),
    url(r'^archive',                                                   views.archive, name='archive'),
    url(r'^(?P<article_id>\d+)/$',                                     views.article, name='article'),
    url(r'^(?P<article_id>\d+)/submit-comment$',                       views.comment, name='submit-comment'),
    url(r'^tag-(?P<tag_slug>\w+)/$',                                   views.index,   name='tag'),
    url(r'^tag-(?P<tag_slug>\w+)/(?P<article_id>\d+)$',                views.article, name='tag-article'),
    url(r'^tag-(?P<tag_slug>\w+)/(?P<article_id>\d+)/submit-comment$', views.comment, name='tag-comment'),
]


