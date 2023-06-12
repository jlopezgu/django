from .models import Category
from rest_framework import viewsets
from .serializers import CategorySerializer


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-created')
    serializer_class = CategorySerializer
