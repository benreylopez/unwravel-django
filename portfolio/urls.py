from django.contrib import admin
from django.urls import path
from django.conf.urls import  include, url
from portal import views as portal_views
from django.conf import settings
from django.template import RequestContext
from django import template
from django.template import Context
from rest_framework.schemas import get_schema_view
from .views import PortfolioListAPIView
from .views import PortfolioListCreateAPIView

urlpatterns = [
    path(
        '',
        PortfolioListAPIView.as_view(),
        name='portfolio-list',
    ),
    path(
    	'/changeLOL',
    	PortfolioListCreateAPIView.as_view(),
    	name='portfolio-createlist'

    )
    # url(r'^$', views.portfolioList, name='portfolioList')
]