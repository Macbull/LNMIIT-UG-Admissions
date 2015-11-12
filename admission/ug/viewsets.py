from ug.serializers import *
from ug import models
from rest_framework import viewsets


class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = models.Applicant.objects.all()
    serializer_class = ApplicantSerializer

class BranchViewSet(viewsets.ModelViewSet):
	queryset = models.Branch.objects.all()
	serializer_class = BranchSerializer

class PreferenceViewSet(viewsets.ModelViewSet):
	queryset = models.Preference.objects.all()
	serializer_class = PreferenceSerializer

class RoundViewSet(viewsets.ModelViewSet):
	queryset = models.Round.objects.all()
	serializer_class = RoundSerializer

class AllotedSeatViewSet(viewsets.ModelViewSet):
	queryset = models.AllotedSeat.objects.all()
	serializer_class = AllotedSeatSerializer

class WaitingListViewSet(viewsets.ModelViewSet):
	queryset = models.WaitingList.objects.all()
	serializer_class = WaitingListSerializer

