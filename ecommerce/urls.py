"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from ecomapp.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('product', product),
    path('register',register),
    path('login',ulogin),
    path('user_logout',user_logout),
    path('contact',contact),
    path('about',about),
    path('catfilter/<cv>',catfilter),
    path('sortfilter/<sv>',sortfilter),
    path('pricefilter',pricefilter),
    path('search',search),
    path('product_detail/<pid>',product_detail),
    path('addtocart/<pid>',addtocard),
    path('viewcart',cart),
    path('updateqty/<u>/<cid>',updateqty),
    path('remove/<cid>',remove),
    path('placeorder',placeorder),
    path('fetchorder',fetchorder),
    path('makepayment',makepayment),
    path('paymentsucess',paymentsucess),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT) ## += means for creating new file statically

