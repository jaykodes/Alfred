from rest_framework import serializers
from data.models import coeff
from data.models import new

class CoeffSerializer(serializers.ModelSerializer):

	class Meta:
		model = coeff
		fields = ('id', 'coeff_zero', 'coeff_one', 'coeff_two', 'coeff_three', 'coeff_four', 'coeff_five')

class NewSerializer(serializers.ModelSerializer):

	class Meta:
		model = new
		fields = ('id', 'sentence', 'be_subjects', 'aux_subjects', 'question_words', 'verbs', 'subjects', 'sen_type')