from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import ( HomePageView,
                     EventListView,
                     EventCreateView,
                     EventUpdateView,
                     EventDetailView,
                     EventDeleteView,
                     AssetListView,
                     AssetUpdateView,
                     AssetDetailView,
                     AssetDeleteView,
                     LocationListView,
                     LocationCreateView,
                     LocationUpdateView,
                     LocationDetailView,
                     LocationDeleteView,
                     asset_create,
                     asset_list
                     )
urlpatterns = [
    path('', login_required(HomePageView.as_view()), name='home'), # new
    path('new_asset/', login_required(asset_create), name="Asset_new"),  # new
    path('events/', login_required(EventListView.as_view()), name='events'),
    path('assets/', login_required(asset_list), name='Assets_list'),
    path('locations/', login_required(LocationListView.as_view()), name='location_list'),
    path('new_event/', login_required(EventCreateView.as_view()), name='event_new'),
    path('<pk>/edit_event/', login_required(EventUpdateView.as_view()), name='event_edit'),
    path('<pk>/event_details', login_required(EventDetailView.as_view()), name='event_detail'),
    path('<pk>/delete_event', login_required(EventDeleteView.as_view()), name='event_delete'),
    # path('new_asset/', AssetCreateView.as_view(), name='Asset_new'),
    path('<pk>/edit_asset/', login_required(AssetUpdateView), name='Asset_edit'),
    path('<pk>/assets_details', login_required(AssetDetailView.as_view()), name='Asset_detail'),
    path('<pk>/delete_asset/', login_required(AssetDeleteView), name='Asset_delete'),
    path('new_location/', login_required(LocationCreateView.as_view()), name='location_new'),
    path('<pk>/edit_location/', login_required(LocationUpdateView.as_view()), name='location_edit'),
    path('<pk>/location_details', login_required(LocationDetailView.as_view()), name='location_detail'),
    path('<pk>/delete_location/', login_required(LocationDeleteView.as_view()), name='location_delete'),
]
