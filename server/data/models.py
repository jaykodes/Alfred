from django.db import models

# Create your models here.
class coeff(models.Model):
	coeff_zero = models.DecimalField(blank=False, default=1, max_digits=19, decimal_places=9)
	coeff_one = models.DecimalField(blank=False, default=1, max_digits=19, decimal_places=9)
	coeff_two = models.DecimalField(blank=False, default=1, max_digits=19, decimal_places=9)
	coeff_three = models.DecimalField(blank=False, default=1, max_digits=19, decimal_places=9)
	coeff_four = models.DecimalField(blank=False, default=1, max_digits=19, decimal_places=9)
	coeff_five = models.DecimalField(blank=False, default=1, max_digits=19, decimal_places=9)

class current(models.Model):
	sentence = models.CharField(max_length=2500, blank=False, default='')
	be_subjects = models.IntegerField(blank=False, default=1)
	aux_subjects = models.IntegerField(blank=False, default=1)
	question_words = models.IntegerField(blank=False, default=1)
	verbs = models.IntegerField(blank=False, default=1)
	subjects = models.IntegerField(blank=False, default=1)
	sen_type = models.IntegerField(blank=False, default=1)

class new(models.Model):
	sentence = models.CharField(max_length=2500, blank=False, default='')
	be_subjects = models.IntegerField(blank=False, default=1)
	aux_subjects = models.IntegerField(blank=False, default=1)
	question_words = models.IntegerField(blank=False, default=1)
	verbs = models.IntegerField(blank=False, default=1)
	subjects = models.IntegerField(blank=False, default=1)
	sen_type = models.IntegerField(blank=False, default=1)