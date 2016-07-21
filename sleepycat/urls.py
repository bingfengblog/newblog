from django.conf.urls import include, url
from django.contrib import admin


from django.conf.urls.static import static
from sleepycat import settings

admin.autodiscover()


urlpatterns = [
    # Examples:
    # url(r'^$', 'sleepycat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/',      include(admin.site.urls)),
    url(r'^',           include('blog.urls')),
    url(r'^blog/',       include('blog.urls', namespace="blog")),
    
] + static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)


handler404 = 'blog.views.err404'
handler500 = 'blog.views.err500'


