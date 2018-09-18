from django.conf.urls import url
from .views import MovieData, MovieSearch, MovieTitleSearch

urlpatterns = [
    url(r'^$', MovieData.as_view(), name='movie'),
    url(r'^search_title/$', MovieTitleSearch.as_view(), name='movie_by_title'),
    url(r'^(?P<pk>\d+)/$', MovieSearch.as_view(), name='movie_by_id'),
    url(r'^search/$', MovieSearch.as_view(), name="movie_search")
]
