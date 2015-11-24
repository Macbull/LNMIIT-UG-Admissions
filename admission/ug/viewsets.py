from ug.serializers import *
from ug import models
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route



class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = models.Applicant.objects.all()
    serializer_class = ApplicantSerializer

    @detail_route(methods=['GET'])
    def status(self, request, **kwargs):
    	preferences = self.request.user.applicant.application_set.order_by('-date_applied')[0].preference_set.order_by('priority').objects.all()
    	serializer = PreferenceSerializer(instance = preferences,many=True)
    	return Response(serializer.data, 200)

    @list_route(methods=['GET'])
    def info(self, request, **kwargs):
    	appl = self.request.user.applicant
    	serializer = ApplicantSerializer(instance = appl,many=False)
    	return Response(serializer.data, 200)

class TestViewSet(viewsets.ModelViewSet):
	queryset = models.Applicant.objects.all()
	serializer_class = ApplicantSerializer


class BranchViewSet(viewsets.ModelViewSet):
	queryset = models.Branch.objects.all()
	serializer_class = BranchSerializer

class PreferenceViewSet(viewsets.ModelViewSet):
	queryset = models.Preference.objects.all()
	serializer_class = WPreferenceSerializer

class RoundViewSet(viewsets.ModelViewSet):
	queryset = models.Round.objects.all()
	serializer_class = RoundSerializer
	@detail_route(methods=['GET'])
	def status(self,request, **kwargs):
		allotment=self.allotedSeat_set.all()
		serializer = AllotedSeatSerializer(instance = allotment,many=True)
		return Response(serializer.data, 200)

class AllotedSeatViewSet(viewsets.ModelViewSet):
	queryset = models.AllotedSeat.objects.all()
	serializer_class = WAllotedSeatSerializer

class WaitingListViewSet(viewsets.ModelViewSet):
	queryset = models.WaitingList.objects.all()
	serializer_class = WaitingListSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
	queryset = models.Application.objects.all()
	serializer_class = ApplicationSerializer



class AdmissionDetailViewSet(viewsets.ModelViewSet):
	queryset = models.AdmissionDetail.objects.all()
	serializer_class = AdmissionDetailSerializer

	@list_route(methods=['post'])
	def conductNextRound(self, request, **kwargs):
		admdet=models.AdmissionDetail.objects.all().order_by('-year')[0]
		cround = admdet.conductNextRound(self.request.data['date'])
		content = {'status': cround}
		return Response(content)




