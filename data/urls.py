from django.urls import path
from .views import SearchAndSuffixAPIView, NewsListAPIView, LatestNewsAPIView, \
    UsefulLinkListAPIView, LatestUsefulLinkAPIView, NewsDetailAPIView, EmployeesListAPIView, \
    TopSearchHistoryView, RegionStatisticsAPIView, ContactCreateView, PublicationsAPIView, TopSearchDetailAPIView, \
    LatestAboutAPIView, CategoryListAPIView, CategoryDetailAPIView

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

    # Employees
    path('api/employees/', EmployeesListAPIView.as_view(), name='news-list'),

    # Top Search History
    path('api/top-search/', TopSearchHistoryView.as_view(), name='top-search'),
    path('api/top-search/<int:pk>/', TopSearchDetailAPIView.as_view(), name='text-detail'),

    # Region Statistic
    path('api/regions/statistics/', RegionStatisticsAPIView.as_view(), name='region-statistics'),

    # Contact
    path('api/contact/create/', ContactCreateView.as_view(), name='contact-create'),
    path('api/contact/about/', LatestAboutAPIView.as_view(), name='about_latest'),

    # Publications
    path('api/publications/', PublicationsAPIView.as_view(), name='publications-list'),

    # About Project
    path('api/project/categories/', CategoryListAPIView.as_view(), name='category-list'),  # Barcha kategoriyalar
    path('api/project/category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),  # Tanlangan kategoriya
]
