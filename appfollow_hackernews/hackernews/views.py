from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from rest_framework import generics
from rest_framework import filters
from rest_framework import exceptions

from .constants import SOURCE_URL, MAX_PAGE_SIZE
from .tasks import update_posts
from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'url', 'created')


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('id', 'title', 'url', 'created')

    def get_paginated_response(self, data):
        order, limit, offset = map(self.request.query_params.get, ['order', 'limit', 'offset'])

        if order is not None and order.lstrip('-') not in self.ordering_fields:
            raise exceptions.ValidationError(
                f'Paramater order must be one of {", ".join(self.ordering_fields)}'
            )

        try:
            limit, offset = map(lambda param: int(param) if param is not None else None, [limit, offset])
        except ValueError:
            raise exceptions.ValidationError(
                f'Parameters limit and offset must be integer numbers'
            )
        if limit is not None and not (0 <= limit <= MAX_PAGE_SIZE):
            raise exceptions.ValidationError(
                f'Parameter limit must be between 0 and {MAX_PAGE_SIZE}'
            )
        if offset is not None and offset < 0:
            raise serializers.ValidationError(
                f'Parameter offset must be greater than zero'
            )

        return JsonResponse(data, safe=False)


def update(request):
    try:
        update_posts(SOURCE_URL)
    except Exception as e:
        return HttpResponse(f'Update failed. Error {str(e)}.', status=500)

    return HttpResponse(f'Update has been finished.')
