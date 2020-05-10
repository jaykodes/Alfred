import mysql.connector
import spacy
import pandas as pd

# establishing connection to database
db = mysql.connector.connect(
	host="YOUR-MYSQL-HOST",
	user="YOUR-MYSQL-USER",
	passwd="YOUR-MYSQL-PASSWORD",
	database="YOUR-DATABASE-NAME"
)

nlp = spacy.load("en")

cursor = db.cursor()
sql_temp = "INSERT INTO YOUR-TABLE (id, sentence, be_subjects, aux_subjects, question_words, verbs, subjects, sen_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

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

def identify_parts(id_val, text, text_type):
	
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

	row = (id_val, text, parts.get("be_sub"), parts.get("aux_sub"), parts.get("ques"), parts.get("verb"), parts.get("sub"), text_type)
	cursor.execute(sql_temp, row)
	db.commit()


data = pd.read_csv('sentence.csv', header=0)
data = data.dropna()

for i in range(len(data)):
	row = data.values[i]
	id_val = i+1
	identify_parts(id_val, row[0].lower(), row[1])

print("Finished Importing")
