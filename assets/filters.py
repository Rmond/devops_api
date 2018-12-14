# -*- coding: utf-8 -*-
__author__ = 'zhangqi'

import django_filters
from django.db.models import Q

from .models import UserHost,UserProfile,HostProfile


class UserHostFilter(django_filters.rest_framework.FilterSet):
    """
    用户权限的过滤
    """

    user = django_filters.CharFilter(method='user_filter')
    host = django_filters.CharFilter(method='host_filter')


    def user_filter(self, queryset, name, value):
        user = UserProfile.objects.get(username=value)
        return queryset.filter(user=user.id)

    def host_filter(self, queryset, name, value):
        host = HostProfile.objects.get(ip=value)
        return queryset.filter(host=host.id)


    class Meta:
        model = UserHost
        fields = ['user', 'host']