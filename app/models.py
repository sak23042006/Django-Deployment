from django.db import models
import os

# Create your models here.


class User(models.Model):
    firstname =  models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.IntegerField()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'User'


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.FileField(upload_to=os.path.join('static', 'UserProfiles'))
    bio = models.TextField(null=True)
    game = models.CharField(max_length=100, null=True)
    address =  models.CharField(max_length=100, null=True)
    game_type = models.CharField(max_length=100, null=True)

    def __str__(self):
        self.user

    class Meta:
        db_table = 'UserProfile'


class Grounds(models.Model):
    groundname = models.CharField(max_length=100)
    gamename = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.IntegerField()
    slots = models.IntegerField()
    image = models.FileField(upload_to=os.path.join('static', 'GroundImages'))
    status = models.CharField(max_length=100, default='Available')

    def __str__(self):
        return self.groundname
    
    class Meta:
        db_table = 'Grounds'

class groundSlotsModel(models.Model):
    slotId = models.AutoField(primary_key=True)
    is_available = models.BooleanField(default=True)
    start_time = models.CharField(max_length=20, null=True)
    end_time = models.CharField(max_length=20, null=True)
    weatherReport = models.CharField(max_length=100, null=True)
    groundName = models.CharField(max_length=100, null=True)
    gameName = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)
    slotPrice = models.IntegerField(null=True)
    date = models.DateField(null=True)

    def __str__(self):
        return self.slotId
    
    class Meta:
        db_table = 'groundSlotsModel'


class slotPaymentModel(models.Model):
    paymentID = models.AutoField(primary_key=True)
    cardNumber = models.CharField(max_length=100, null=True)
    cardHolderName = models.CharField(max_length=50, null=True)
    groundName = models.CharField(max_length=50, null=True)
    gameName = models.CharField(max_length=50, null=True)
    userEmail = models.EmailField(null=True)
    paid = models.CharField(max_length=50, null=True)
    paymentDate = models.DateTimeField(auto_now_add=True, null=True)
    location = models.CharField(max_length=50, null=True)
    start_time = models.CharField(max_length=20, null=True)
    end_time = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'slotPaymentModel'


class teamModel(models.Model):
    teamID = models.AutoField(primary_key=True)
    teamLeaderName = models.CharField(max_length=50, null=True)
    teamLeaderMail = models.EmailField(null=True)
    team = models.JSONField(default=list)
    groundName = models.CharField(max_length=50, null=True)
    gameName = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.teamLeaderName

    class Meta:
        db_table = 'teamModel'

class userRequestModel(models.Model):
    requestID = models.AutoField(primary_key=True)
    requestReciever = models.EmailField(null=True)
    requestSender = models.EmailField(null=True)
    requestStatus = models.CharField(max_length=50, default='not accepted')
    recieverTeamId = models.CharField(max_length=50, null=True)
    groundName = models.CharField(max_length=50, null=True)
    gameName = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'userRequestModel'

