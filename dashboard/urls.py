"""
URL configuration for dashboard app.
"""

from django.urls import path
from .views import (
    LoginView,
    logout_view,
    DashboardHomeView,
    PlacementListView,
    PlacementCreateView,
    PlacementUpdateView,
    PlacementDeleteView,
    PlacementDetailView,
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    UserDetailView,
    ImportPlacementsView,
    DownloadTemplateView,
    ProfileView,
    SettingsView,
    analytics_data_api,
)
from .analytics_views import (
    DepartmentAnalyticsView,
    SpecialtyAnalyticsView,
    ShiftAnalyticsView,
    StatusAnalyticsView,
    TimelineAnalyticsView,
)

app_name = "dashboard"

urlpatterns = [
    # Authentication
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    # Main dashboard
    path("", DashboardHomeView.as_view(), name="home"),
    # Analytics pages
    path(
        "analytics/department/",
        DepartmentAnalyticsView.as_view(),
        name="analytics_department",
    ),
    path(
        "analytics/specialty/",
        SpecialtyAnalyticsView.as_view(),
        name="analytics_specialty",
    ),
    path("analytics/shifts/", ShiftAnalyticsView.as_view(), name="analytics_shifts"),
    path("analytics/status/", StatusAnalyticsView.as_view(), name="analytics_status"),
    path(
        "analytics/timeline/",
        TimelineAnalyticsView.as_view(),
        name="analytics_timeline",
    ),
    # API endpoints
    path("api/analytics/", analytics_data_api, name="analytics_api"),
    # Placement CRUD
    path("placements/", PlacementListView.as_view(), name="placement_list"),
    path("placements/create/", PlacementCreateView.as_view(), name="placement_create"),
    path(
        "placements/<int:pk>/", PlacementDetailView.as_view(), name="placement_detail"
    ),
    path(
        "placements/<int:pk>/edit/",
        PlacementUpdateView.as_view(),
        name="placement_update",
    ),
    path(
        "placements/<int:pk>/delete/",
        PlacementDeleteView.as_view(),
        name="placement_delete",
    ),
    path(
        "placements/import/",
        ImportPlacementsView.as_view(),
        name="placement_import",
    ),
    path(
        "placements/download-template/",
        DownloadTemplateView.as_view(),
        name="placement_download_template",
    ),
    # User CRUD
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/create/", UserCreateView.as_view(), name="user_create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("users/<int:pk>/edit/", UserUpdateView.as_view(), name="user_update"),
    path(
        "users/<int:pk>/delete/",
        UserDeleteView.as_view(),
        name="user_delete",
    ),
    # Profile and Settings
    path("profile/", ProfileView.as_view(), name="profile"),
    path("settings/", SettingsView.as_view(), name="settings"),
]
