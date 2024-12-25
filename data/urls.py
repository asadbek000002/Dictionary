from django.urls import path
from .views import SearchAndSuffixAPIView, NewsListAPIView, LatestNewsAPIView, \
    UsefulLinkListAPIView, LatestUsefulLinkAPIView, NewsDetailAPIView, UsefulLinkDetailAPIView, EmployeesListAPIView, \
    TopSearchHistoryView, RegionStatisticsAPIView, ContactCreateView, PublicationsAPIView, \
    EmployeesDetailAPIView

urlpatterns = [
    # text
    path('api/text/search/', SearchAndSuffixAPIView.as_view(), name='search_and_suffix'),

    # news
    path('api/news/latest/', LatestNewsAPIView.as_view(), name='latest-news'),
    path('api/news/', NewsListAPIView.as_view(), name='news-list'),
    path('api/news/<int:pk>/', NewsDetailAPIView.as_view(), name='news-detail'),

    # link
    path('api/useful-link/latest/', LatestUsefulLinkAPIView.as_view(), name='latest-useful-link'),
    path('api/useful-link/', UsefulLinkListAPIView.as_view(), name='useful-link-list'),
    path('api/useful-link/<int:pk>/', UsefulLinkDetailAPIView.as_view(), name='useful-link-detail'),

    # Employees
    path('api/employees/', EmployeesListAPIView.as_view(), name='news-list'),
    path('api/employees/<int:pk>/', EmployeesDetailAPIView.as_view(), name='news-detail'),

    # Top Search History
    path('api/top-search/', TopSearchHistoryView.as_view(), name='top-search'),

    # Region Statistic
    path('api/regions/statistics/', RegionStatisticsAPIView.as_view(), name='region-statistics'),

    # Contact
    path('api/contact/create/', ContactCreateView.as_view(), name='contact-create'),

    # Publications
    path('api/publications/', PublicationsAPIView.as_view(), name='publications-list'),
]
