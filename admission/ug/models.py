from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max


class AdmissionDetail(models.Model):
	year = models.CharField(max_length=4)
	commence_date = models.DateField(auto_now_add=True)
	application_deadline = models.DateField()
	cutoff_marks = models.IntegerField()
	no_of_rounds = models.IntegerField()
	def getAllRounds(self):
		return self.round_set.all()
	def conductNextRound():		
		previous_round=self.round_set.order_by('-round_set')[0].roundNumber
		Round.create(previous_round+1,self.application_set)
	def concludeCurrentRound():
		current_round=self.round_set.order_by('-round_set')[0]
		current_round.conclude()

class AdminProfile(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=30)
	staff_id = models.IntegerField()
	email_id = models.EmailField()
	designation = models.CharField(max_length=15)
	session = models.ForeignKey(AdmissionDetail)

class Branch(models.Model):
	session = models.ForeignKey(AdmissionDetail,null=False)
	name = models.CharField(max_length=30,null=False)
	seats_left = models.IntegerField()
	abbreviation = models.CharField(max_length=3)
	no_of_seats = models.IntegerField(null=False)
	closingrank = models.IntegerField()
	def updateClosingRank(self,value):
		self.closingrank = value
	def getSeatsLeft(self):
		return self.seats_left
	def updateSeatsLeft(self,value):
		self.seats_left = self.seats_left + value

class Round(models.Model):
	roundNumber = models.IntegerField(null=False)
	timestamp = models.DateTimeField(auto_now=True)
	fees_deadline = models.DateField(null=False)
	part_of = models.ForeignKey(AdmissionDetail)
	conducted_by = models.ForeignKey(AdminProfile)
	concluded = models.BooleanField(default=False)
  #  def conduct(self):
 #   def conclude(self):


class Applicant(models.Model):
	# user = models.OneToOneField(User)
	name = models.CharField(max_length=30,null=False)
	address = models.CharField(max_length=100)
	email = models.EmailField()
	mobile = models.CharField(max_length = 10)
	father_name = models.CharField(max_length=30,null=True)

class Application(models.Model):
	applicant = models.ForeignKey(Applicant) 
	#date_applied = models.DateTimeField(auto_now_add=True)
	#an applicant can apply again next year, but will need to create new application
	date_of_birth = models.DateField(null=False)
	jee_main_marks = models.IntegerField(null=False)
	jee_main_rank = models.IntegerField(null=False)
	high_school_marks = models.IntegerField()
	is_valid = models.BooleanField()
	eligible_for_next_round = models.BooleanField()
	session = models.ForeignKey(AdmissionDetail)
	fees_status = models.IntegerField()
	def modifyFeesStatus(self,value):
		fees_status = value
	def getFeesStatus():
		return fees_status
	def checkStatus():
		for preference in preference_set.all():
			preference.getCurrentStatus()

#	def getInfo():
#	def is_eligible_for_next_round():
	class Meta:
		unique_together = ('applicant','session')



class Preference(models.Model):
	application = models.ForeignKey(Application,null=False)
	priority = models.IntegerField(null=False)
	branch = models.ForeignKey(Branch,null=False)
	status = models.BooleanField(default=False)
	def getCurrentStatus(self):
		alloted = AllotedSeat.is_currently_alloted(self.application,self.branch)
		if alloted==1:
			return 0
		else:
			return WaitingList.is_currently_waiting(self.application,self.branch)
	class Meta:
		unique_together = ('application','priority')
		unique_together = ('application','branch')


class AllotedSeat(models.Model):
	branch = models.ForeignKey(Branch,null=False)
	councelling_round = models.ForeignKey(Round,null=False)
	application = models.ForeignKey(Application,null=False)
	@staticmethod
	def is_currently_alloted(application,branch):
		return AllotedSeat.objects.filter(application=application,branch=branch)==AllotedSeat.objects.filter(application=application).order_by('-councelling_round__roundNumber')[0]

class WaitingList(models.Model):
	branch = models.ForeignKey(Branch,null=False)
	councelling_round = models.ForeignKey(Round,null=False)
	waiting = models.IntegerField(null = False)
	application = models.ForeignKey(Application,null=False)
	@staticmethod
	def is_currently_waiting(application,branch):
		return WaitingList.objects.filter(application=application,branch=branch).order_by('-councelling_round__roundNumber')[0].waiting





