from django.urls import include, path
from rest_framework import routers
from subscriber import views
from django.contrib import admin
from category.views import CategoryViewSet

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'channel', views.ChannelViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'message', views.MessageViewSet)
router.register(r'notifications', views.NotificationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
