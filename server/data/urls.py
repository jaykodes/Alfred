from django.conf.urls import url
from data import views
 
urlpatterns = [ 
	url(r'^api/data/(?P<sentence>[0-9a-z_.]+)$', views.new_data),
]