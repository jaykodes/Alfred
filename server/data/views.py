from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.response import Response
 
from data.models import coeff
from data.models import new
from data.serializers import CoeffSerializer
from data.serializers import NewSerializer
from rest_framework.decorators import api_view

import spacy
import pandas as pd
import numpy as np
import math
import json

# Create your views here.

def commands(text):

	if ".com" in text or ".ca" in text or ".org" in text or ".io" in text:
		return "website"
	elif "google" in text or "search" in text:
		return "google false"
	elif "youtube" in text:
		return "youtube"
	elif "play" in text:
		return "play"
	elif "open" in text:
		return "open"
	else:
		return False

#POS tag list:

	# CC 	coordinating conjunction
	# CD	cardinal digit
	# DT	determiner
	# EX	existential there (like: "there is" ... think of it like "there exists")
	# FW	foreign word
	# IN	preposition/subordinating conjunction
	# JJ	adjective	'big'
	# JJR	adjective, comparative	'bigger'
	# JJS	adjective, superlative	'biggest'
	# LS	list marker	1)
	# MD	modal	could, will
	# NN	noun, singular 'desk'
	# NNS	noun plural	'desks'
	# NNP	proper noun, singular	'Harrison'
	# NNPS	proper noun, plural	'Americans'
	# PDT	predeterminer	'all the kids'
	# POS	possessive ending	parent\'s
	# PRP	personal pronoun	I, he, she
	# PRP$	possessive pronoun	my, his , hers
	# RB	adverb	very, silently,
	# RBR	adverb, comparative	better
	# RBS	adverb, superlative	best
	# RP	particle	give up
	# TO	to	go 'to' the store.
	# UH	interjection	errrrrrrrm
	# VB	verb, base form	take
	# VBD	verb, past tense	took
	# VBG	verb, gerund/present participle	taking
	# VBN	verb, past participle	taken
	# VBP	verb, sing. present, non-3d	take
	# VBZ	verb, 3rd person sing. present	takes
	# WDT	wh-determiner	which
	# WP	wh-pronoun	who, what
	# WP$	possessive wh-pronoun	whose
	# WRB	wh-abverb	where, when

be = {"am", "are", "is", "was", "were"}
aux = {"can", "could", "do", "does", "did", "have", "has", "had", "may", "should", "will", "would"}
question = {"WDT", "WP", "WP$", "WRB"}
verbs = {"VB", "VBD", "VBN", "VBP", "VBZ", "MD"}
description = {"RB", "RBR", "RBS", "JJ", "JJR", "JJS"}
subjects = {"NN", "NNS", "NNP", "NNPS", "PRP", "PRP$", "VBG", "POS", "CD", "DT", "PDT"}
other = {"CC", "UH", "FW", "IN", "RP", "EX", "LS", "TO"}

nlp = spacy.load("en")

# returns value of num in the sigmoid function
def sigmoid(num):
	return (1 / (1 + math.exp(num * -1)))

def x_parts(text):
	
	parts = {}
	parts["be_sub"] = 0
	parts["aux_sub"] = 0
	parts["ques"] = 0
	parts["verb"] = 0
	parts["sub"] = 0

	tokens = nlp(text)

	i = 0
	sub_part = True
	# figures out how many of each POS are in the sentence
	while i < len(tokens):
		last_one = (i < (len(tokens) - 1))
		last_two = (i < (len(tokens) - 2))

		if last_two and tokens[i].text in be and tokens[i+1].tag_ == "RB" and tokens[i+2].tag_ in subjects:
			parts["be_sub"] = parts.get("be_sub") + 1
			i += 3
			sub_part = True
		elif last_two and tokens[i].text in aux and tokens[i+1].tag_ == "RB" and tokens[i+2].tag_ in subjects:
			parts["aux_sub"] = parts.get("aux_sub") + 1
			i += 3
			sub_part = True
		elif last_one and tokens[i].text in be and tokens[i+1].tag_ in subjects:
			parts["be_sub"] = parts.get("be_sub") + 1
			i += 2
			sub_part = True
		elif last_one and tokens[i].text in aux and tokens[i+1].tag_ in subjects:
			parts["aux_sub"] = parts.get("aux_sub") + 1
			i += 2
			sub_part = True
		elif tokens[i].tag_ in question:
			parts["ques"] = parts.get("ques") + 1
			i += 1
			sub_part = True
		elif tokens[i].tag_ in verbs:
			parts["verb"] = parts.get("verb") + 1
			i += 1
			sub_part = True
		elif sub_part:
			parts["sub"] = parts.get("sub") + 1
			i += 1
			sub_part = False
		else:
			i += 1

	return parts

@api_view(['GET', ])
def new_data(request, sentence):

	if request.method == 'GET':

		sentence = sentence.replace("_", " ")
		sentence = sentence.lower()
		is_command = commands(sentence)

		if is_command != False:
			return Response(is_command)

		coeff_vals = coeff.objects.get(id=1)
		coeff_serializer = CoeffSerializer(coeff_vals)
		coeff_data = JsonResponse(coeff_serializer.data, safe=False)

		json_data = json.loads(coeff_data.content)

		coeff_set = [float(json_data['coeff_zero']), float(json_data['coeff_one']), float(json_data['coeff_two']), float(json_data['coeff_three']), float(json_data['coeff_four']), float(json_data['coeff_five'])]
		coeff_set = np.asmatrix(coeff_set)

		parts = x_parts(sentence)
		
		# get the x and coeff values
		x = [1, parts.get("be_sub"), parts.get("aux_sub"), parts.get("ques"), parts.get("verb"), parts.get("sub")]
		x = np.asmatrix(x)
		
		actual_val = x.dot(coeff_set.transpose())
		actual_val = sigmoid(actual_val.flat[0])

		if actual_val > 0.5:
			actual_val = 1
			is_command = "I don't understand"
		else:
			actual_val = 0
			is_command = "google true"

		new_datas = {
			'sentence': sentence,
			'be_subjects': parts.get("be_sub"),
			'aux_subjects': parts.get("aux_sub"),
			'question_words': parts.get("ques"),
			'verbs': parts.get("verb"),
			'subjects': parts.get("sub"),
			'sen_type': actual_val
		}

		new_serializer = NewSerializer(data=new_datas)

		if new_serializer.is_valid():
			new_serializer.save()
			return Response(is_command)
		return JsonResponse(new_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

