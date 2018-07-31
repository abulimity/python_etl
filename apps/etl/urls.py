from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^review/',views.reviews,name='review'),
    url(r'^$',views.etlForm,name='etlForm'),
    url(r'^display/$',views.reviewCSV,name='etlForm'),
    url(r'^submittask/$',views.etlForm,name='etlForm'),
    url(r'^showProgress/$',views.showProgress,name='etlForm'),
    # 异步检查目标表是否存在
    # url(r'^checkTable/$',views.checkTable,name='etlForm'),
]