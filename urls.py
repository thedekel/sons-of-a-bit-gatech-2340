from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^start\.php', 'mordor.views.start'),
    url(r'^config\.php', 'mordor.views.config'),
    url(r'^start/submit\.php', 'mordor.views.submit'),
	url(r'^wagon.php', 'mordor.views.wag'),
    # url(r'^$', 'CS2340OregonTrail.views.home', name='home'),
    # url(r'^CS2340OregonTrail/', include('CS2340OregonTrail.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
