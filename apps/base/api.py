from rest_framework import generics

class GeneralListAPIView(generics.ListAPIView):
    """General View for list Measure,Indicator,Category views in general_views,
       Used for read-only endpoints to represent a collection of model instances.
    """
    serializer_class = None

    def get_queryset(self):
        """Get the list of items for this view

        Returns:
            query: with objects-state=True
        """
        model = self.get_serializer().Meta.model
        return model.objects.filter(state = True)