from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^review/',views.reviews,name='review'),
    url(r'^$',views.etlForm,name='etlForm'),
    url(r'^display/$',views.reviewCSV,name='reviewCSV'),
    url(r'^submittask/$',views.etlForm,name='etlForm'),
]