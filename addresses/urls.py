from django.urls import path
from .views import AddressView, AddressRiskView

urlpatterns = [
    path('api/addresses/', AddressView.as_view(), name='address-create'),
    path('api/addresses/<int:id>/risks/', AddressRiskView.as_view(), name='address-risks'),
]