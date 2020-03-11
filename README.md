# Keyword_Identifier
Identifies keyword or part of keyword from a given list of keywords and a sentence

## Usage Example

The module "identify_keywords" takes a list of keywords that can be person names, movie names, project names or anything
and a sentence in which it will identify the list of keywords found in the setence that match the ones present in the keywords list given

```
#list of keywords from which the sentence's keywords are matched

given_keywords=["AI Algorithms", "Crazy Website", "MEAN website", "AI Hype", "AI", 
"My Crazy Website", "AI Module", "New York", "Egg York", "Italian:Pizza", "French-Pizza", 
"Super_AI", "The Dark Knight", "The Dark Knight Rises"]



#given sentences

sentence1="I want an Italian Pizza"        
# due to exact match with "Italian:Pizza"


sentence2="show me my website"             
# returning all keywords having the word "Website" because no exact match is found


sentence3="I like the darki"               
# fuzzy matched with "The Dark" knight and "The Dark" Knight Rises


#The respective output for each sentence will be
Keywords fuzzily matched are:  ['Italian:Pizza']
Keywords fuzzily matched are:  ['Crazy Website', 'MEAN website', 'My Crazy Website']
Keywords fuzzily matched are:  ['The Dark Knight', 'The Dark Knight Rises']
```

The module is very simple to use like:

```
import identify_keywords as identify

#list of keywords with which the given sentence is matched
given_keywords=["AI Algorithms", "Crazy Website", "MEAN website", "AI Hype", "AI", "My Crazy Website", "AI Module",
"New York", "Egg York", "Italian:Pizza", "French-Pizza", "Super_AI","The Dark Knight", "The Dark Knight Rises"]

#can be populated from DB, can be name of people, project names or anything.


sentence="I want an Italian Pizza"

keys_identified=identify.identify_keywords(given_keywords,sentence)

print("Keywords fuzzily matched are: ", keys_identified)
```

## How to use

- Clone the repo
- pip3 install -r requirements.txt
- python3 main.py

## Requirements
- Python3
- Pip3
- Fuzzywuzzy
- NLTK

## License
It is a free public tool to use
