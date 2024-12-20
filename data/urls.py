from django.urls import path
from .views import SearchAndSuffixAPIView, SuffixInfoAPIView, NewsListAPIView, LatestNewsAPIView, \
    UsefulLinkListAPIView, LatestUsefulLinkAPIView

urlpatterns = [
    path('api/search/', SearchAndSuffixAPIView.as_view(), name='search_and_suffix'),
    path('api/suffix-info/', SuffixInfoAPIView.as_view(), name='suffix_info'),
    path('api/news/', NewsListAPIView.as_view(), name='news-list'),
    path('api/news/latest/', LatestNewsAPIView.as_view(), name='latest-news'),
    path('api/useful-link/', UsefulLinkListAPIView.as_view(), name='useful-link-list'),
    path('api/useful-link/latest/', LatestUsefulLinkAPIView.as_view(), name='latest-useful-link'),
]
