from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.views.generic import TemplateView, ListView
from .models import Event, Asset, Location ,FileUplaod
from .forms import EventCreationForm, AssetCreationForm, LocationCreationForm
from django.views.generic import ListView, DetailView  # new
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.db.models import Q
import datetime
from shapeshifter.views import MultiFormView



# class HomePageView(TemplateView):
#     template_name = 'home.html'


class HomePageView(MultiFormView):
    form_classes = (AssetCreationForm, LocationCreationForm)
    template_name = 'home.html'
    success_url = reverse_lazy('Assets_list')

    def forms_valid(self):
        forms = self.get_forms()
        # contact_form = forms['AssetCreationForm']
        # interest_form = forms['LocationCreationForm']
        return super().forms_valid()

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
    form = AssetCreationForm(request.POST or None, request.FILES)

    if request.method == 'POST':

        if form.is_valid():
            files = request.FILES.getlist('file[]')
            im = 1
            IDs = []
            while im <= int(request.POST['count']):
                location = Location(Longitude1=request.POST['longitude' + str(im)],
                                    Latitude1=request.POST['latitude' + str(im)])
                location.save(force_insert=True)
                IDs.append(location.id)
                im += 1
            filesIDs = []
            for asset in files:
                fs = FileSystemStorage()
                file_path = fs.save(asset.name, asset)
                # uploadedFile = FileUplaod(file=asset.read())
                # uploadedFile.save(force_insert=True)
                # filesIDs.append(uploadedFile.id)

            asset = Asset(multi_uploads=files, Expiry_date=request.POST['Expiry_date'],
                             Expiry_time=request.POST['Expiry_time'],)
            asset.save(force_insert=True)
            asset.Locations.set(IDs)
            asset.files.set(filesIDs)

            Multi_assets = files

            print(Multi_assets)

            return redirect(reverse_lazy('Assets_list'))

        else:
            print(form.errors)

    # images = Asset.objects.select_related('asset_id').all()
    # print(images)
    context = {"form": form
               }
    return render(request, "Asset_new.html", context)


def AssetUpdateView(request, pk):
    asset = Asset.objects.get(id=pk)
    form = AssetCreationForm(request.POST or None, request.FILES)
    Expiry_date = asset.Expiry_date.strftime("%Y-%m-%d")
    Expiry_time=asset.Expiry_time.strftime("%H:%M")
    count=len(asset.Locations.all())
    uploaded_files=asset.multi_uploads
    long_lat=[]
    allAssets=[]
    for aset in asset.multi_uploads:
        allAssets.append(aset)
    allAssetsNum=len(allAssets)
    for loc in asset.Locations.all():
        long_lat.append({"Long": loc.Longitude1, "Lat": loc.Latitude1})

    if request.method == 'POST':

        if form.is_valid():
            im = 1
            IDs = []
            for loc in asset.Locations.all():
                location, created = Location.objects.update_or_create(
                    id=loc.id,
                    defaults={'Longitude1': request.POST['longitude' + str(im)],
                              'Latitude1': request.POST['latitude' + str(im)]},
                )
                IDs.append(location.id)
                im += 1
            files = request.FILES.getlist('file[]')
            deletedAssets = request.POST.getlist('AssetInput')
            for asset in deletedAssets :
                if asset != " ":
                    allAssets.remove(asset)

            res = [*allAssets, *files]

            for asset in files:
                fs = FileSystemStorage()
                file_path = fs.save(asset.name, asset)

            # asset = Asset(multi_uploads=files, Expiry_date=request.POST['Expiry_date'],
            #               Expiry_time=request.POST['Expiry_time'], )
            # asset.save(force_insert=True)
            # asset.Locations.set(IDs)
            obj, created = Asset.objects.update_or_create(
                id=pk,
                defaults={'multi_uploads':res, 'Expiry_date':request.POST['Expiry_date'],
                          'Expiry_time':request.POST['Expiry_time'],},
            )
            obj.Locations.set(IDs)

            Multi_assets = files
            print(Multi_assets)

            return redirect(reverse_lazy('Assets_list'))

        else:
            print(form.errors)
    context = {
        "asset": asset,
        "form":form,
        "Expiry_date": Expiry_date,
        "Expiry_time": Expiry_time,
        "count":count,
        "long_lat":long_lat,
        "uploaded_files":uploaded_files
    }
    return render(request, "Asset_edit.html", context)


def AssetDeleteView(request, pk):
    # dictionary for initial data with
    # field names as keys
    # fetch the object related to passed id

    obj = Asset.objects.get(pk=pk)

    if request.method == "POST":
        for loc in obj.Locations.all():
            Location.objects.filter(id=loc.id).delete()
        # delete object
        # obj.delete()
        Asset.objects.filter(id=pk).delete()

        # after deleting redirect to
        # home page
        return redirect(reverse_lazy('Assets_list'))

    context = {
        "asset":obj,
        "assetId": pk,
    }
    return render(request, "Asset_delete.html", context)
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


# class AssetUpdateView(UpdateView):
#     model = Asset
#     form_class = AssetCreationForm
#     template_name = 'Asset_edit.html'
# #     emailvalue= form.cleaned_data.get("email")


# class AssetDeleteView(DeleteView):
#     model = Asset
#     template_name = 'Asset_delete.html'
#     success_url = reverse_lazy('Assets_list')


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
