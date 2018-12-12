from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from django_filters.rest_framework import DjangoFilterBackend

from .models import HostProfile
from .serializer import UserSerializer,HostSerializer

User = get_user_model()

class CommonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    page_query_param = "page"
    max_page_size = 500

class UserViewset(mixins.ListModelMixin,mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('is_staff',)
    search_fields = ('username', 'nickname')
    # permission_classes = (permissions.IsAuthenticated, )
    def get_permissions(self):
        if self.action == "retrieve" or self.action == "update":
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_superuser:
            return Response("超级用户不允许删除",status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        if self.request.user.is_staff:
            return super(UserViewset,self).get_object()
        else:
            return self.request.user

    def perform_create(self, serializer):
        return serializer.save()

class HostViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    资产
    """
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    queryset = HostProfile.objects.get_queryset().order_by('ip')
    serializer_class = HostSerializer
    pagination_class = CommonPagination

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "update":
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

class HostIPListViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = HostProfile.objects.filter(parent=None)
    serializer_class = HostSerializer