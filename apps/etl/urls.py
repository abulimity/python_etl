from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^review/',views.reviews,name='review'),
    url(r'^$',views.etlForm,name='etlForm'),
    # 预览文件
    url(r'^display/$',views.reviewCSV,name='etlForm'),
    url(r'^submittask/$',views.etlForm,name='etlForm'),
    # 查询进度
    url(r'^showProgress/$',views.showProgress,name='etlForm'),
    # 异步检查目标表是否存在
    url(r'^checkTable/$',views.checkTable,name='etlForm'),
    # 创建目标表
    url(r'^createTable/$',views.createTable,name='etlForm'),
    url(r'^doCreate/$',views.doCreate,name='etlForm'),
]