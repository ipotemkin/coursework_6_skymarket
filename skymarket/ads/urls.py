from django.urls import include, path

from rest_framework.routers import DefaultRouter

from ads.views import AdViewSet, CommentViewSet

router = DefaultRouter()  # SimpleRouter
router.register('ads', AdViewSet)
router.register(r'ads/(?P<ad_pk>\d+)/comments', CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
