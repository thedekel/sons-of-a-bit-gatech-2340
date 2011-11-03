from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^inv.php', 'mordor.views.inv'),
    url(r'^$', 'mordor.views.main'),
    url(r'^start', 'mordor.views.start'),
    url(r'^status', 'mordor.views.status'),
    url(r'^newparty', 'mordor.views.newparty'),

    url(r'^advanceTurn', 'mordor.views.advanceTurn'),
    url(r'^changerats', 'mordor.views.changerats'),
    url(r'^makeParty', 'mordor.views.makeParty'),

    # url(r'^$', 'CS2340OregonTrail.views.home', name='home'),
    # url(r'^CS2340OregonTrail/', include('CS2340OregonTrail.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
