from django.db.models import Q
from rest_framework import pagination, viewsets
from rest_framework.decorators import action

from ads.models import ADO, COMO
from ads.serializers import AdSerializer, AdDetailSerializer, CommentSerializer  # , CommentCreateSerializer


class AdPagination(pagination.PageNumberPagination):
    pass


def build_query(request):
    """builds a query with the specified query params"""

    query = Q()

    if search := request.GET.get('search'):
        query |= Q(title__icontains=search)

    # if search_loc := request.GET.get('location'):
    #     query &= Q(author__locations__name__icontains=search_loc)
    #
    # if search_price_from := request.GET.get('price_from'):
    #     query &= Q(price__gte=search_price_from)
    #
    # if search_price_to := request.GET.get('price_to'):
    #     query &= Q(price__lte=search_price_to)
    #
    # if username := request.GET.get('username'):
    #     query &= Q(author__username__icontains=username)

    return query


# TODO view функции. Предлагаем Вам следующую структуру - но Вы всегда можете использовать свою
class AdViewSet(viewsets.ModelViewSet):
    queryset = ADO.all()
    serializer_class = AdSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = AdDetailSerializer
        print(self.action)
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """shows a list of ads"""

        if query := build_query(request):
            self.queryset = (
                self.get_queryset()
                    .select_related("author")
                    .filter(query)
                    .distinct()
            )
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        # print(self.action)
        self.queryset = ADO.filter(author_id=request.user.id)
        return super().list(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = COMO.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = COMO.filter(ad_id=kwargs["ad_pk"])
        # print(f'pk={kwargs["ad_pk"]}')
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """creates a new comments"""

        # self.serializer_class = CommentCreateSerializer
        request.data["author_id"] = request.user.id
        request.data["ad_id"] = kwargs["ad_pk"]
        print(f'ad_id={kwargs["ad_pk"]}')
        print(f'author_id={request.user.id}')
        return super().create(request, *args, **kwargs)
