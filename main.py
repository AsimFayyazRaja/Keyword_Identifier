import identify_keywords as identify

#list of keywords with which the given sentence is matched
given_keywords=["AI Algorithms", "Crazy Website", "MEAN website", "AI Hype", "AI", "My Crazy Website", "AI Module",
"New York", "Egg York", "Italian:Pizza", "French-Pizza", "Super_AI","The Dark Knight", "The Dark Knight Rises"]

#can be populated from DB, can be name of people, project names or anything.


sentence="I want an Italian Pizza"

keys_identified=identify.identify_keywords(given_keywords,sentence)

print("Keywords fuzzily matched are: ", keys_identified)