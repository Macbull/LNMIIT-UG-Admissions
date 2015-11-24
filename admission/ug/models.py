from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.mail import send_mail

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class AdmissionDetail(models.Model):
	year = models.CharField(max_length=4)
	commence_date = models.DateField(auto_now_add=True)
	application_deadline = models.DateField()
	cutoff_marks = models.IntegerField()
	# no_of_rounds = models.IntegerField()

	def getAllRounds(self):
		return self.round_set.all()

	def conductNextRound(self,date):	

		
		if self.round_set.count():
			previous_round=self.round_set.order_by('-roundNumber')[0]
			previous_round.conclude()

			if date>previous_round.fees_deadline and previous_round.concluded==True:
				cround = Round(roundNumber = previous_round.roundNumber+1,fees_deadline=date,part_of=self)
				cround.save()
				cround.conduct(self.branch_set,self.application_set.filter(is_valid=True).filter(eligible_for_next_round = 0))
				return cround.id
			else:
				return -1
		else:
			cround = Round(roundNumber = 1,fees_deadline=date,part_of=self)
			cround.save()
			cround.conduct(self.branch_set,self.application_set.filter(is_valid=True).filter(eligible_for_next_round = 0))
			return cround.id


	def concludeCurrentRound(self):
		current_round=self.round_set.order_by('-roundNumber')[0]
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
	# closingrank = models.IntegerField()
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
	# conducted_by = models.ForeignKey(AdminProfile)
	concluded = models.BooleanField(default=False)

	def conduct(self,branches,appls):
		dictwait = {}
		for branch in branches.all():
			dictwait[branch.abbreviation]=0

		appls=appls.order_by('-jee_main_marks')
		for app in appls:
			prefs = app.preference_set.order_by('priority')
			alloted = False
			for pref in prefs:
				branch=pref.branch
				if branch.seats_left>0 and alloted==False:
					a=AllotedSeat(branch=branch,councelling_round=self,application=app)
					a.save()
					branch.updateSeatsLeft(-1)
					alloted=True
					app.sendConfirmation(branch,self)
				else:
					dictwait[branch.abbreviation]+=1
					w=WaitingList(branch=branch,councelling_round=self,waiting=dictwait[branch.abbreviation],application=app)
					w.save()

	def conclude(self):
		seats=self.allotedSeat_set.all()
		for seat in seats:
			app=seat.application
			if app.fees_status==0:
				app.eligible_for_next_round=-1
				seat.branch.updateSeatsLeft(1)
			if seat.branch==app.preference_set.get(priority=1).branch:
				app.eligible_for_next_round=1
		self.concluded=True




class Applicant(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=30,null=False)
	address = models.CharField(max_length=100)
	email = models.EmailField()
	mobile = models.CharField(max_length = 10)
	father_name = models.CharField(max_length=30,null=True)

class Application(models.Model):
	applicant = models.ForeignKey(Applicant) 
	date_applied = models.DateTimeField(auto_now_add=True)
	# an applicant can apply again next year, but will need to create new application
	date_of_birth = models.DateField(null=False)
	jee_main_marks = models.IntegerField(null=False,validators=[
            MaxValueValidator(360),
            MinValueValidator(-90)
        ])
	jee_main_rank = models.IntegerField(null=False)
	high_school_marks = models.IntegerField()
	is_valid = models.BooleanField()
	eligible_for_next_round = models.IntegerField(default=0)
	session = models.ForeignKey(AdmissionDetail)
	fees_status = models.IntegerField(default=0)
	def modifyFeesStatus(self,value):
		fees_status = value
	def getFeesStatus():
		return fees_status
	def checkStatus():
		for preference in preference_set.all():
			preference.getCurrentStatus()

	def sendConfirmation(self,branch,cround):
		message = "You have been alloted seat in The LNM-IIT in branch " + branch.abbreviation + ", in councelling round no "+str(cround.roundNumber)+"."
		if self.fees_status==0:
			message+=" You have to submit fees by "+str(cround.fees_deadline)+" otherwise your candidature will be cancelled."

			send_mail("Congratulations ", message,"LNMIIT <vnarwal95@gmail.com>", [self.applicant.email])
#	def getInfo():
#	def is_eligible_for_next_round():
	class Meta:
		unique_together = ('applicant','session')



class Preference(models.Model):
	application = models.ForeignKey(Application,null=False)
	priority = models.IntegerField(null=False)
	branch = models.ForeignKey(Branch,null=False)
	# status = models.BooleanField(default=False)
	def getCurrentStatus(self):
		alloted = AllotedSeat.is_currently_alloted(self.application,self.branch)
		if alloted==1:
			return 0
		elif WaitingList.is_currently_waiting(self.application,self.branch):
			return WaitingList.is_currently_waiting(self.application,self.branch)
		else:
			return -1
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





