import json
from django.forms import model_to_dict
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from .models import Movie, Genres


class MovieData(View):

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(MovieData, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk=None):
        queryset = Movie.objects.all().prefetch_related()
        # print(queryset)
        if queryset:
            main_json = list()
            for i in queryset:
                data = model_to_dict(i)
                data['genres_movie'] = list()
                for d in i.genres_movie.all():
                    data['genres_movie'].append(model_to_dict(d))
                main_json.append(data)
            print(main_json)
            result = {
                'message': main_json
            }
            return JsonResponse(result, status=200)
        else:
            result = {
                'message': 'Movie not able to fetch.'
            }
            return JsonResponse(result, status=204)

    # def post(self, request):
    #     pass

    def delete(self, request):
        body_data = request.data
        # movie = self.get_object(body_data.get('title'))
        # movie.delete()
        queryset = Movie.objects.get(title=body_data.get('title'))
        if queryset:
            queryset.delete()
            response = {
                'message': 'movie delete'
            }
            return JsonResponse(response, status=200)
        else:
            response = {
                'message': 'movie not found'
            }
            return JsonResponse(response, status=204)

    def post(self, request):
        # print(json.loads(request.body))
        body_data = json.loads(request.body)
        gen = None
        if body_data.get('genres'):
            genres = body_data.pop('genres')
            movie = Movie.objects.create(**body_data)
            bulk_genres = [Genres(name=data, movie_id=movie.id) for data in genres]
            gen = Genres.objects.bulk_create(bulk_genres)
        else:
            try:
                del body_data['genres']
            except Exception as e:
                pass
            movie = Movie.objects.create(**body_data)
        if movie and gen:
            response = {
                'message': 'movie created'
            }
            return JsonResponse(response, status=200)
        elif movie:
            response = {
                'message': 'movie created'
            }
            return JsonResponse(response, status=200)
        else:
            response = {
                'message': 'movie does not created.'
            }
            return JsonResponse(response, status=204)


class MovieTitleSearch(View):

    def get(self, request):
        if request.GET.get('title'):
            query_args = {
                'title__icontains': request.GET.get('title')
            }
            # queryset = Movie.objects.filter(**query_args).values()
            queryset = Movie.objects.filter(**query_args).prefetch_related()
            if queryset:
                main_json = list()
                for i in queryset:
                    data = model_to_dict(i)
                    data['genres_movie'] = list()
                    for d in i.genres_movie.all():
                        data['genres_movie'].append(model_to_dict(d))
                    main_json.append(data)
                print(main_json)
                response = {
                    'message': main_json
                }
                return JsonResponse(response, status=200)
            else:
                request_url = "http://www.omdbapi.com/?t={0}&apikey=b63f7e7e".format(request.GET.get('title'))
                response = requests.get(request_url)
                if response.status_code == 200:
                    raw_data = json.loads(response.text)
                    # raw_data if len(raw_data) > 1 else
                    # print(raw_data)
                    body_data = {
                        'title': raw_data.get('Title'),
                        'released_year': raw_data.get('Released')[-4:],
                        'rating': raw_data.get('imdbRating'),
                        'genres': raw_data.get('Genre').split(',') if raw_data.get('Genre') else []
                    }
                    # print(body_data)
                    gen = None
                    if body_data.get('genres'):
                        # print('genre found')
                        genres = body_data.pop('genres')
                        movie = Movie.objects.create(**body_data)
                        bulk_genres = [Genres(name=data, movie_id=movie.id) for data in genres]
                        gen = Genres.objects.bulk_create(bulk_genres)
                        body_data.update({'genres': genres})
                        result = {
                            'message': body_data
                        }
                        return JsonResponse(result, status=200)
                    else:
                        # print('genre not found')
                        try:
                            del body_data['genres']
                        except Exception as e:
                            pass
                        movie = Movie.objects.create(**body_data)
                        result = {
                            'message': body_data
                        }
                        return JsonResponse(result, status=200)


class MovieSearch(View):

    def get(self, request, *args, **kwargs):
        # print(request.GET)
        try:
            fields_name = [i.name for i in Movie._meta.get_fields()]
            queryset = None
            if kwargs.get('pk'):
                # queryset = Movie.objects.filter(id=kwargs.get('pk')).values()
                queryset = Movie.objects.filter(id=kwargs.get('pk')).prefetch_related()
                print(queryset)
                main_json = list()
                for i in queryset:
                    data = model_to_dict(i)
                    data['genres_movie'] = list()
                    for d in i.genres_movie.all():
                        data['genres_movie'].append(model_to_dict(d))
                    main_json.append(data)
                print(main_json)
            elif request.GET.get('search_field') == 'year':
                if len(request.GET.get('search_term')) > 4:
                    query_args = {
                        'released_year__range': request.GET.get(
                            'search_term').split('-')
                    }
                else:
                    query_args = {
                        'released_year': request.GET.get(
                            'search_term')
                    }
                print(query_args)
                # queryset = Movie.objects.filter(**query_args).values()
                queryset = Movie.objects.filter(**query_args).prefetch_related()
                print(queryset)
                main_json = list()
                for i in queryset:
                    data = model_to_dict(i)
                    data['genres_movie'] = list()
                    for d in i.genres_movie.all():
                        data['genres_movie'].append(model_to_dict(d))
                    main_json.append(data)
                print(main_json)
            elif request.GET.get('search_field') == 'rating':
                if request.GET.get('condition') == 'higher':
                    query_args = {
                        '{0}__gte'.format(request.GET.get('search_field')): request.GET.get(
                            'search_term')
                    }
                else:
                    query_args = {
                        '{0}__lte'.format(request.GET.get('search_field')): request.GET.get(
                            'search_term')
                    }
                queryset = Movie.objects.filter(**query_args).prefetch_related()
                print(queryset)
                main_json = list()
                for i in queryset:
                    data = model_to_dict(i)
                    data['genres_movie'] = list()
                    for d in i.genres_movie.all():
                        data['genres_movie'].append(model_to_dict(d))
                    main_json.append(data)
                print(main_json)
            elif request.GET.get('search_field') in fields_name:
                query_args = {
                    '{0}__icontains'.format(request.GET.get('search_field')): request.GET.get('search_term')
                }
                # queryset = Movie.objects.filter(**query_args).values()
                queryset = Movie.objects.filter(**query_args).prefetch_related()
                print(queryset)
                main_json = list()
                for i in queryset:
                    data = model_to_dict(i)
                    data['genres_movie'] = list()
                    for d in i.genres_movie.all():
                        data['genres_movie'].append(model_to_dict(d))
                    main_json.append(data)
                print(main_json)
            else:
                response = {
                    'message': 'Field name not matched.'
                }
                return JsonResponse(response, status=200)
            # print(queryset)
            if queryset:
                response = {
                    'message': main_json
                }
                return JsonResponse(response, status=200)
            else:
                response = {
                    'message': 'Not found'
                }
                return JsonResponse(response, status=206)
        except Exception as e:
            print(e)
            response = {
                'message': 'Internal server error'
            }
            return JsonResponse(response, status=500)
