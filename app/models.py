from django.db import models
import os
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.contrib.auth.hashers import make_password

class User(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # store hashed password here
    phone = models.BigIntegerField()  # Changed to BigIntegerField for larger phone numbers

    def save(self, *args, **kwargs):
        # Hash the password before saving if not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'User'


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.FileField(upload_to=os.path.join('static', 'UserProfiles'))
    bio = models.TextField(null=True, blank=True)
    game = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    game_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = 'UserProfile'


class Grounds(models.Model):
    groundname = models.CharField(max_length=100)
    gamename = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
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
    start_time = models.CharField(max_length=20, null=True, blank=True)
    end_time = models.CharField(max_length=20, null=True, blank=True)
    groundName = models.CharField(max_length=100, null=True, blank=True)
    gameName = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    slotPrice = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.slotId)

    class Meta:
        db_table = 'groundSlotsModel'


class slotPaymentModel(models.Model):
    paymentID = models.AutoField(primary_key=True)
    cardNumber = models.CharField(max_length=100, null=True, blank=True)
    cardHolderName = models.CharField(max_length=50, null=True, blank=True)
    groundName = models.CharField(max_length=50, null=True, blank=True)
    gameName = models.CharField(max_length=50, null=True, blank=True)
    userEmail = models.EmailField(null=True, blank=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    paymentDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    start_time = models.CharField(max_length=20, null=True, blank=True)
    end_time = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Payment #{self.paymentID} - {self.userEmail}"

    class Meta:
        db_table = 'slotPaymentModel'


class teamModel(models.Model):
    teamID = models.AutoField(primary_key=True)
    teamLeaderName = models.CharField(max_length=50, null=True, blank=True)
    teamLeaderMail = models.EmailField(null=True, blank=True)
    team = models.JSONField(default=list)
    groundName = models.CharField(max_length=50, null=True, blank=True)
    gameName = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.teamLeaderName} - {self.teamID}"

    class Meta:
        db_table = 'teamModel'


class userRequestModel(models.Model):
    requestID = models.AutoField(primary_key=True)
    requestReciever = models.EmailField(null=True, blank=True)
    requestSender = models.EmailField(null=True, blank=True)
    requestStatus = models.CharField(max_length=50, default='not accepted')
    recieverTeamId = models.CharField(max_length=50, null=True, blank=True)
    groundName = models.CharField(max_length=50, null=True, blank=True)
    gameName = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Request #{self.requestID} - {self.requestSender}"

    class Meta:
        db_table = 'userRequestModel'
