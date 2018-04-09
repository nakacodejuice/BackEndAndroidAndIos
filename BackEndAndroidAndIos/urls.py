"""BackEndAndroidAndIos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import BackEnd
from BackEnd.views import token
from django.conf.urls import url
urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^token', BackEnd.views.token, name='token'),
    url(r'^api/Account/Register', BackEnd.views.register, name='register'),
    url(r'^api/account', BackEnd.views.account, name='account'),
    url(r'^api/account/password/forgot/:*', BackEnd.views.forgot, name='forgot'),
    url(r'^api/account/device', BackEnd.views.device, name='device'),
    url(r'^api/Сhar', BackEnd.views.Сhar, name='Сhar'),
    url(r'^api/CounterCharge', BackEnd.views.MetersCharge, name='MetersCharge'),
    url(r'^api/Counter', BackEnd.views.Meters, name='Meters'),
    url(r'^api/Pay', BackEnd.views.Pay, name='Pay'),
    url(r'^api/Saldo', BackEnd.views.Saldo, name='Saldo'),
    url(r'^api/saldo/current', BackEnd.views.SaldoCurrent, name='SaldoCurrent'),
    url(r'^api/saldo/current:*', BackEnd.views.SaldoCurrentServiceId, name='SaldoCurrentServiceId'),
    url(r'^api/saldo/notification', BackEnd.views.notification, name='notification'),
    url(r'^api/saldo/notification/new', BackEnd.views.notificationnew, name='notificationnew'),
    url(r'^api/saldo/notification:*', BackEnd.views.notificationid, name='notificationid'),
    url(r'^api/news', BackEnd.views.news, name='news'),
    url(r'^api/news/:*', BackEnd.views.newsid, name='newsid'),
    url(r'^api/tariff/:*', BackEnd.views.tariffdate, name='tariffdate'),
    url(r'^api/tariff/list', BackEnd.views.tarifflist, name='tarifflist'),
    url(r'^api/uchastok/:(\d+)$', BackEnd.views.uchastokById, name='uchastokById'),
    url(r'^api/uchastok', BackEnd.views.uchastoklist, name='uchastoklist'),
    url(r'^api/kvit/delivery',BackEnd.views.delivery, name='delivery'),
    url(r'^api/meter/readings/received',BackEnd.views.ReadingsReceived, name='ReadingsReceived'),
    url(r'^api/meter/readings/accepted',BackEnd.views.ReadingsAccepted, name='ReadingsAccepted'),
    url(r'api/meter/readings',BackEnd.views.SetReadings, name='SetReadings'),
    url(r'api/question',BackEnd.views.Question, name='Question'),
    url(r'api/inform',BackEnd.views.Inform, name='Inform'),
]
