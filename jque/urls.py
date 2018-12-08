
from django.conf.urls import url
from jque import views


urlpatterns = [

	url('^$',views.index,name='index'),
	
]