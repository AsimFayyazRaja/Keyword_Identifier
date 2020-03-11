import identify_keywords as identify

#list of keywords with which the given sentence is matched
given_keywords=["AI Bot", "Jonathan BOT", "Chatbot", "AI Chatbot", "Bot", "Website chatbot", "AI Module",
"New York", "Egg York", "Italian:Pizza", "French-Pizza", "Super AI Bot"]
#can be populated from DB, can be name of people, project names or anything.


sentence="I want a Pizza"

keys_identified=identify.identify_keywords(given_keywords,sentence)

print("Keywords fuzzily matched are: ", keys_identified)