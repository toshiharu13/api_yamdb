from rest_framework import mixins, viewsets


class ListPostDelMix(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet,
                     ):
    pass
