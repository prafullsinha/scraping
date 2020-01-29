from .views import ScrapeView
from django.urls import path
from . import views

urlpatterns = [
                path('', ScrapeView.as_view(), name='home'),
                path('deatil/<str:product_id>/', views.DetailView, name="deatil"),
            ]