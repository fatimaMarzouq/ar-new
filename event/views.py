from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import TemplateView, ListView
from .models import Event, Asset, Location
from .forms import EventCreationForm, AssetCreationForm, LocationCreationForm
from django.views.generic import ListView, DetailView  # new
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.db.models import Q
import datetime


class HomePageView(TemplateView):
    template_name = 'home.html'


def asset_list(request):
    now = datetime.datetime.now()
    assets = Asset.objects.filter(Q(Expiry_date__gte=datetime.date.today()) |
                                  Q(Expiry_time__gte=now.time()))
    context = {
        "assets": assets
    }
    return render(request, "Assets_list.html", context)


class AssetListView(ListView):
    model = Asset
    template_name = 'Assets_list.html'


# class AssetCreateView(LoginRequiredMixin, CreateView):
#     model = Asset
#     form_class = AssetCreationForm
#     template_name = 'Asset_new.html'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


def asset_create(request):
    locations = []
    asset_files = []
    form = AssetCreationForm(request.POST or None, request.FILES)
    i = 1
    if request.method == 'POST':
        for e in request.POST:
            i = i + 1
            if i > 5:
                locations.append(request.POST.getlist('location' + str(i - 5)))
        if form.is_valid():
            files = request.FILES.getlist('file[]')

            for asset in files:
                fs = FileSystemStorage()
                file_path = fs.save(asset.name, asset)

            # print(asset_files)
            location = Asset(multi_uploads=files, Expiry_date=request.POST['Expiry_date'],
                             Expiry_time=request.POST['Expiry_time'], Multi_Locations=locations)
            location.save(force_insert=True)

            Multi_Locations = locations
            Multi_assets = files
            # print(request.POST.getlist('location1')[0])
            # print(locations)
            print(Multi_assets)

            # print(request.POST)

            return redirect(reverse_lazy('Assets_list'))

        else:
            print(form.errors)

    # images = Asset.objects.select_related('asset_id').all()
    # print(images)
    context = {"form": form
               }
    return render(request, "Asset_new.html", context)


# def asset_create(request):
#     # if this is a POST request we need to process the form data
#     print("hello")
#     if request.method == 'POST':
#         print("hellos")
#         form = AssetCreationForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # Asset_instance = Asset.objects.create(Longitude='Longitude', )
#             print(request.POST)
#
#             return HttpResponseRedirect('/asset_list.html')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = AssetCreationForm()
#
#     # return render(request, 'asset_list.html', {'form': form})
#     return


class EventListView(ListView):
    model = Event
    template_name = 'events.html'


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventCreationForm
    template_name = 'event_new.html'

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(EventCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventCreationForm
    template_name = 'event_edit.html'

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(EventUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class EventDeleteView(DeleteView):
    model = Event
    template_name = 'event_delete.html'
    success_url = reverse_lazy('events')


class AssetDetailView(DetailView):
    model = Asset
    template_name = 'Asset_detail.html'


class AssetUpdateView(UpdateView):
    model = Asset
    form_class = AssetCreationForm
    template_name = 'Asset_edit.html'


def asset_update(request, pk):
    asset = Asset.objects.get(id=pk)
    locations = []
    asset_files = []
    form = AssetCreationForm(request.POST or None, request.FILES)
    i = 1
    if request.method == 'POST':
        for e in request.POST:
            i = i + 1
            if i > 5:
                locations.append(request.POST.getlist('location' + str(i - 5)))
        if form.is_valid():
            files = request.FILES.getlist('file[]')

            for asset in files:
                fs = FileSystemStorage()
                file_path = fs.save(asset.name, asset)

            # print(asset_files)
            location = Asset(multi_uploads=files, Expiry_date=request.POST['Expiry_date'],
                             Expiry_time=request.POST['Expiry_time'], Multi_Locations=locations)
            location.save(force_insert=True)

            Multi_Locations = locations
            Multi_assets = files
            # print(request.POST.getlist('location1')[0])
            # print(locations)
            print(Multi_assets)
    context = {
        "asset": asset
    }
    return render(request, "Asset_edit.html", context)


class AssetDeleteView(DeleteView):
    model = Asset
    template_name = 'Asset_delete.html'
    success_url = reverse_lazy('Assets_list')


class LocationListView(ListView):
    model = Location
    template_name = 'location_list.html'


class LocationCreateView(CreateView):
    model = Location
    form_class = LocationCreationForm
    template_name = 'location_new.html'

    # fields = ('Name', 'Photo', 'starting_date', 'ending_date')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(LocationCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LocationDetailView(DetailView):
    model = Location
    template_name = 'location_detail.html'


class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationCreationForm
    template_name = 'location_edit.html'

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(LocationUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LocationDeleteView(DeleteView):
    model = Location
    template_name = 'location_delete.html'
    success_url = reverse_lazy('location_list')
