from django.urls import path
from django.views.generic import CreateView, ListView

from . import views
from .models import Division, Host, Person, UsbStor

urlpatterns = [
    path("", views.index, name="index"),
    path("division/", ListView.as_view(model=Division), name="divisions"),
    # path("division/add", CreateView.as_view(model=Division, fields='__all__', success_url='.'), name="division-add"),
    path("division/add", views.DivisionCreateView.as_view(), name="division-add"),
    path("host/", ListView.as_view(model=Host), name="hosts"),
    path("host/<int:pk>", views.HostUpdateView.as_view(), name="host-update"),
    path("host/upload", views.host_info_form, name="hostInfoUpload"),
    path("host/update/<cssiid>", views.host_update_info_form, name="hostInfoUpdate"),
    path("usbstor/", ListView.as_view(model=UsbStor, ordering=['regdate']), name="usbstors"),
    path("usbstor/<int:pk>", views.StorageUpdateView.as_view(), name="storage-update"),
    path("person/", ListView.as_view(model=Person), name="persons"),
    path("person/<int:pk>", views.PersonUpdateView.as_view(), name="person-update"),
    path("person/add", views.PersonCreateView.as_view(), name="person-add"),
]
