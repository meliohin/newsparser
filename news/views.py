from rest_framework.response import Response
from rest_framework import generics, filters
from .serializers import NewsSerializer
from .models import News


class NewsList(generics.ListAPIView):
    """
    List all news.
    """
    serializer_class = NewsSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'title', 'url', 'created'] 

    def get_queryset(self):
    	return News.objects.all()