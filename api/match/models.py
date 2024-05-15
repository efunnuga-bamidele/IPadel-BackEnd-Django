from django.db import models
from api.user.models import CustomUser
from api.court.models import Court


class Match(models.Model):
    displayName = models.CharField(
        max_length=100, null=True, blank=True)
    bookedBy = models.CharField(
        max_length=100, null=True, blank=True)
    phoneNumber = models.CharField(
        max_length=100, null=True, blank=True)
    referenceId = models.CharField(
        max_length=50, default=0)
    court = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(max_length=100)
    time = models.CharField(
        max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=20, default=60)
    private = models.BooleanField(default=False)
    paymentType = models.CharField(max_length=200, default='Full Payment')
    players = models.IntegerField(default=2)
    registeredPlayers = models.JSONField(blank=True, null=True)
    matchStatus = models.JSONField(blank=True, null=True, default=[
                                   {"team1": "Team A", "team2": "Team B", "score1": 0, "score2": 0}])
    genders = models.CharField(
        max_length=20, default='Mixed', blank=True, null=True)
    status = models.CharField(
        max_length=20, blank=True, null=True, default="Open")
    paymentStatus = models.CharField(
        max_length=500, blank=True, null=True, default="Unpaid")
    bookingCost = models.CharField(
        max_length=100, blank=True, default=0)
    amountPaid = models.CharField(
        max_length=100, blank=True, null=True, default=0)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.court)+' | '+str(self.created_at.strftime("%m/%d/%Y | %H:%M:%S"))
