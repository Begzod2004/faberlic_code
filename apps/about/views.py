from drf_spectacular.utils import extend_schema
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from apps.about.models import *
from apps.about.serializers import (ContactUsSerializer, ServiceSerializer,
                                    SocialSerializer)


class ContactListCreateView(ListCreateAPIView):
    queryset = Contact.objects.all().order_by("-id")
    serializer_class = ContactUsSerializer

    @extend_schema(tags=["contact"])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response(serializer.data[0])
        return Response({})

    @extend_schema(tags=["contact"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ContactDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all().order_by("-id")
    serializer_class = ContactUsSerializer
    lookup_field = "id"

    @extend_schema(tags=["contact"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["contact"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["contact"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["contact"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class SocialsListCreateView(ListCreateAPIView):
    queryset = Social.objects.all().order_by("-id")
    serializer_class = SocialSerializer

    @extend_schema(tags=["socials"])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response(serializer.data[0])
        return Response({})

    @extend_schema(tags=["socials"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SocialsDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Social.objects.all().order_by("-id")
    serializer_class = SocialSerializer
    lookup_field = "id"

    @extend_schema(tags=["socials"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["socials"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["socials"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["socials"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ServiceListCreateView(ListCreateAPIView):
    queryset = Service.objects.all().order_by("-id")
    serializer_class = ServiceSerializer

    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(tags=["services"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["services"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ServiceDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all().order_by("-id")
    serializer_class = ServiceSerializer
    lookup_field = "id"
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(tags=["services"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["services"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["services"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["services"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
