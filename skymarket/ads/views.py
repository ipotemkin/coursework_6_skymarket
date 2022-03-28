from django.db.models import Q
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from ads.models import ADO, COMO
from ads.permissions import IsAdmin, IsAuthor
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
@extend_schema_view(
    list=extend_schema(description="Get all advertisements", summary="Advertisements"),
    retrieve=extend_schema(description="Get an advertisement with the specified id", summary="Advertisement by id"),
    create=extend_schema(description="Create a new advertisement", summary="Create a new advertisement"),
    update=extend_schema(description="Update an advertisement", summary="Update an advertisement"),
    partial_update=extend_schema(
        description="Partially update an advertisement",
        summary="Partially update an advertisement"
    ),
    destroy=extend_schema(description="Delete an advertisement", summary="Delete an advertisement"),
    me=extend_schema(description="Get current user's advertisements", summary="Current user's advertisements"),
)
class AdViewSet(viewsets.ModelViewSet):
    queryset = ADO.all()
    serializer_class = AdSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = AdDetailSerializer
        print(self.action)
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="search", description="Searching in the title", required=False, type=str)
        ]
    )
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

    def create(self, request, *args, **kwargs):
        """creates a new ad"""

        self.serializer_class = AdDetailSerializer
        request.data["author_id"] = request.user.id
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        self.queryset = ADO.filter(author_id=request.user.id)
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        """sets permissions for ads' views"""

        permissions = []
        if self.action in ("retrieve", "create", "me"):
            permissions = (IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            permissions = (IsAuthenticated & (IsAdmin | IsAuthor),)
        return [permission() for permission in permissions]


@extend_schema_view(
    list=extend_schema(description="Get all comments", summary="Comments to Ad with ad_pk"),
    retrieve=extend_schema(
        description="Get a comment with the specified id to Ad with ad_pk",
        summary="Comment by id to Ad with ad_pk"
    ),
    create=extend_schema(description="Create a new comment", summary="Create a new comment"),
    update=extend_schema(description="Update a comment", summary="Update a comment"),
    partial_update=extend_schema(
        description="Partially update a comment",
        summary="Partially update a comment"
    ),
    destroy=extend_schema(description="Delete a comment", summary="Delete a comment"),
    # me=extend_schema(description="Get current user's advertisements", summary="Current user's advertisements"),
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = COMO.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = COMO.filter(ad_id=kwargs["ad_pk"])
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """creates a new comments"""

        request.data["author_id"] = request.user.id
        request.data["ad_id"] = kwargs["ad_pk"]
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        """sets permissions for comments' views"""

        permissions = []
        if self.action in ("list", "retrieve", "create"):
            permissions = (IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            permissions = (IsAuthenticated & (IsAdmin | IsAuthor),)
        return [permission() for permission in permissions]
