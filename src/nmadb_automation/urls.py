from django.conf.urls import patterns, url


urlpatterns = patterns(
    'nmadb_automation.views',
    url(r'^admin/mail/create/$', 'create_mail',
        name='nmadb-automation-create-mail',),
    )
