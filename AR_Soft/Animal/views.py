# animal/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Animal, Group, AnimalGroup
from .serializers import AnimalSerializer, AnimalGroupSerializer, GroupSerializer

class AnimalListView(generics.ListCreateAPIView):
    """
    API view to list all animals or create a new one (or multiple).
    Includes filtering by company_id, race, gender, and is_slaughtered.
    """
    serializer_class = AnimalSerializer

    def get_queryset(self):
        queryset = Animal.objects.all()

        # Filter by company_id if provided
        company_id = self.request.query_params.get('company_id')
        if company_id:
            queryset = queryset.filter(company_id=company_id)

        # Filter by race if provided (case-insensitive match)
        race = self.request.query_params.get('race')
        if race:
            queryset = queryset.filter(race__iexact=race)

        # Filter by gender if provided (convert 0/1 to Boolean)
        gender = self.request.query_params.get('gender')
        if gender is not None:
            try:
                gender_bool = bool(int(gender))  # Convert '0' or '1' to a Boolean
                queryset = queryset.filter(gender=gender_bool)
            except ValueError:
                pass  # Ignore invalid gender filter

        # Filter by is_slaughtered if provided
        is_slaughtered = self.request.query_params.get('is_slaughtered')
        if is_slaughtered is not None:
            # Convert '0', 'False' or similar values to False, and '1', 'True' to True
            is_slaughtered_bool = is_slaughtered.lower() in ['true', '1']
            queryset = queryset.filter(is_slaughtered=is_slaughtered_bool)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Override create to support both single and bulk creates.
        """
        # Check if the incoming data is a list (bulk create) or a single object
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        # Validate and save
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Return the created object(s)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnimalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific animal by ID.
    """
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


############################
## GROUP ##
############################

class GroupListView(generics.ListCreateAPIView):
    """
    API view to list all groups or create a new group.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific group by ID.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class AnimalGroupListView(generics.ListCreateAPIView):
    """
    API view to list all animal-group relationships or add a new animal to a group.
    """
    queryset = AnimalGroup.objects.all()
    serializer_class = AnimalGroupSerializer

    def get_queryset(self):
        queryset = AnimalGroup.objects.all()

        # Filter by animal_id if provided
        animal_id = self.request.query_params.get('animal_id')
        if animal_id:
            queryset = queryset.filter(animal_id=animal_id)

        # Filter by group_id if provided
        group_id = self.request.query_params.get('group_id')
        if group_id:
            queryset = queryset.filter(group_id=group_id)

        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Override create to handle both single and bulk creation of AnimalGroup.
        """
        # If the request data is a list => bulk create
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class AnimalGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific animal-group assignment by ID.
    """
    queryset = AnimalGroup.objects.all()
    serializer_class = AnimalGroupSerializer
