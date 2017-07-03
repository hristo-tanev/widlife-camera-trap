from __future__ import unicode_literals

from django.db import models


class Bird(models.Model):
    image_name = models.CharField(max_length=20)
    daym = models.CharField(max_length=20)
    month = models.CharField(max_length=20)
    year = models.CharField(max_length=20)
    birdsDetected = models.IntegerField()
    flew_in = models.IntegerField()
    flew_away = models.IntegerField()


class AdvancedStatsForMonth(models.Model):
    startDate = models.CharField(max_length=20)
    endDate = models.CharField(max_length=20)
    averageNumberOfBirdsForAPeriod = models.DecimalField(
        max_digits=20, decimal_places=2)
    averageOfBirdsFlewIn = models.DecimalField(max_digits=20, decimal_places=2)
    averageOfBirdsFlewAway = models.DecimalField(
        max_digits=20, decimal_places=2)
    leastBirdsDate = models.CharField(max_length=20)


class AdvancedStatsForWeek(models.Model):
    startDate = models.CharField(max_length=20)
    endDate = models.CharField(max_length=20)
    averageNumberOfBirdsForAPeriod = models.DecimalField(
        max_digits=20, decimal_places=2)
    averageOfBirdsFlewIn = models.DecimalField(max_digits=20, decimal_places=2)
    averageOfBirdsFlewAway = models.DecimalField(
        max_digits=20, decimal_places=2)
    leastBirdsDate = models.CharField(max_length=20)


class Size(models.Model):
    db_size = models.IntegerField()
