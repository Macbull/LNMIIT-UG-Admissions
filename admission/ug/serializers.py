from ug import models
from rest_framework import serializers
from django.contrib.auth.models import User


class ApplicantSerializer(serializers.ModelSerializer):
	jee_main_marks = serializers.SerializerMethodField()
	jee_main_rank = serializers.SerializerMethodField()
	dob =serializers.SerializerMethodField()

	def get_jee_main_marks(self,obj):
		if obj.application_set.count():
			return obj.application_set.order_by('-date_applied')[0].jee_main_marks 
		else:
			return '-'
	def get_jee_main_rank(self,obj):
		if obj.application_set.count():
			return obj.application_set.order_by('-date_applied')[0].jee_main_rank
		else:
			return '-'
	def get_dob(self,obj):
		if obj.application_set.count():
			return obj.application_set.order_by('-date_applied')[0].date_of_birth
		else:
			return '-'
	class Meta:
		model = models.Applicant
		fields = ('name','address','email','mobile','father_name','jee_main_marks','jee_main_rank','dob')
		read_only_fields = ('jee_main_rank','jee_main_marks','dob')
class BranchSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Branch

class ApplicationSerializer(serializers.ModelSerializer):
	applicant = ApplicantSerializer(many=False)
	class Meta:
		model = models.Application

class PreferenceSerializer(serializers.ModelSerializer):
	branch = BranchSerializer(many=False)
	current_status = serializers.SerializerMethodField()

	def get_current_status(self,obj):
		return obj.getCurrentStatus()
	class Meta:
		model = models.Preference

class RoundSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Round

class AllotedSeatSerializer(serializers.ModelSerializer):
	branch = BranchSerializer(many = False)
	application = ApplicationSerializer()
	class Meta:
		model = models.AllotedSeat

class WaitingListSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.WaitingList

class AdmissionDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.AddmissionDetail
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User