from rest_framework import filters, generics, permissions
from rest_framework.response import Response

from .models import School
from .serializers import SchoolSerializer


class SchoolListCreateView(generics.ListCreateAPIView):
    """
    A view to list and create school
    """

    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "state", "address"]

    def get_queryset(self):
        queryset = super().get_queryset()
        for field in self.search_fields:
            search_term = self.request.query_params.get(field, None)
            if search_term:
                queryset = queryset.filter(**{f"{field}__icontains": search_term})
        return queryset


class SchoolRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view for retrieving, updating, and deleting a school account.
    """

    serializer_class = SchoolSerializer
    permission_classes = [permissions.AllowAny]

    error_response = Response(
        {
            "message": "School with this id does not exist",
            "error": "Not Found",
            "statusCode": 404,
        },
        status=404,
    )

    def get_object(self):
        """retrieve school object"""

        school_id = self.kwargs["id"]
        return School.objects.filter(id=school_id).first()

    def get(self, request, *args, **kwargs):
        """Override default get method to include custom error message"""

        if self.get_object() is None:
            return self.error_response
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Override default update method to include custom error message"""

        instance = self.get_object()
        if instance is None:
            return self.error_response
        serializer = self.serializer_class(
            instance,
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=200)

    def delete(self, request, *args, **kwargs):
        """
        Override default delete method to include custom error and
        success message
        """

        instance = self.get_object()
        if instance is None:
            return self.error_response
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Successful",
            },
            status=204,
        )
