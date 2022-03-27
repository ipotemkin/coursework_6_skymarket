from django.urls import include, path

# TODO настройка роутов для модели
from rest_framework.routers import DefaultRouter

from ads.views import AdViewSet, CommentViewSet

# urlpatterns = [
#
# ]


router = DefaultRouter()  # SimpleRouter
# router.register('cats', categories.CatAPIViewSet)
router.register('ads', AdViewSet)
router.register(r'ads/(?P<ad_pk>\d+)/comments', CommentViewSet)
# router.register('selections', selections.SelectionViewSet)
# router.register('users', users.UserViewSet)
# router.register('locations', users.LocAPIViewSet)

urlpatterns = [
    # path("ads/<int:pk>/upload_image", ads.AdImageUpdateView.as_view()),
    # path("users/token/refresh/", TokenRefreshView.as_view()),
    # path("users/token/", TokenObtainPairView.as_view()),
    path("", include(router.urls)),

    # additional urls
    # path("ads/html/<int:pk>/", ads.AdHTMLDetailView.as_view(), name="ad_http_detail"),
    # path("ads/html/", ads.AdHTMLView.as_view(), name="ad_http"),
]
