from ug import models
from rest_framework import serializers


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

class PreferenceSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Preference

class RoundSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Round

class AllotedSeatSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.AllotedSeat

class WaitingListSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.WaitingList

