# Alfred

Alfred is a desktop assistant that able to identify and fulfill user needs using Natural Language Processing and speech recognition. The way Alfred is able to decipher commands is by using a custom logistic regression model. This model is able to identify between declarative and interrogative setences with 96% accuracy.

<h2> About the model </h2>

The model takes in a sentence as input. It then transforms that sentence into bits breaking it into the eight parts of speech in the English language (noun, pronoun, verb, adjective, adverb, preposition, conjunction, and interjection) using the spaCy and NLTK libraries. Then, depending on the frequency and ordering of each part of speech, the model is able to dictate whether a sentence is declarative or interrogative.

<h2> Training the model </h2>

To train the model, I took a bunch of sentences online and manually classified each sentence type. Afterwards, the model would train on this dataset. It was very cool to see the patterns that the model used to help dictate if a sentence is declarative or interrogative. One pattern I noticed was that the model would give a higher probability of interrogative if it saw question words (who, what, where, when, why, how) in the front.

<h2> Abilities of Alfred </h2>

Depending on the sentence type, Alfred executes different commands. If the sentence is interrogative, Alfred would search the question online and present you with a google search. If the sentence is declarative, Alfred will do different commands.

If Alfred sees any of the following commands, it will perform such commands. Otherwise, Alfred will simply state that he did not understand the instruction and await for the next command.

  1. Open: If Alfred notices the word "Open" in the sentence, it will take the next few words and attempt to open an application with those words.
  2. Youtube: If Alfred notices the word "Youtube" in the sentence, it will take the rest of the sentence and put it into a Youtube search. Afterwards, Alfred will automatically play the first video.
  3. Google/Search: If Alfred notices the word "Google" or "Search" in the sentence, it will take the rest of the sentence and put it into a Google Search and display the information to you.
