from django.shortcuts import render
from django.contrib.auth import login
from django.views import generic

from bayi.models import Customer


class DashboardView(generic.ListView):
    model = Customer
    template_name = 'pages/dashboard.html'

