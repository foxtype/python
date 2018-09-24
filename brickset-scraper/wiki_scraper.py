#import Dependencies
#BS helps with parsing data from the web.
from bs4 inport BeautifulSoup
#python Lybrary, used for deailing with HTML CSS and other web technologies
import requests
# Helps us perform regular expressions
import re
#a wrapper around functions that already exist in python ie. addition subtraction
import operator
#help parse our json
import json
#creates nice table in terminal
from tabulate import tabulate
#system calls to take user input
import sys
#words that don't matter in natural laguage like 'the', and 'to'
from stop_words import get_stop_words

#get Data from wikipedia
#create link to wiki api
wikipedia_api_link = "https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch="
wikipedia_link = "https://en.wikipedia.org/wiki/"

if (len(sys.argv) < 2):
	print("Enter Valid String")
	exit()

#get the search word
string_query = sys.argv[1]
if (len(sys.argv) > 2):
	search_mode = True
else:
	search_mode = False

#create url
url = wikipedia_api_link + string_query

try:
	response = requests.get(url)
	data = json.loads(response.content.decode('utf-8'))

	#format this data
	wikipedia_page_tag = data['query']['search'][0]['title']
	
	#create our new url
	url = wikipedia_link + wikipedia_page_tag
	page_word_list = getWordList(url)

	#create table of word counts
	page_word_count = CreateFrequencyTable(page_word_list)
	sorted_word_frequency_list = sorted(page_word_count.items(), key = operator.itemgetter(1), reverse = True)
	
	#remove stop words
	if(search_mode): 
		sorted_word_frequency_list = remove_stop_words(sorted_word_frequency_list)

	#sum total words to calculate frequencies
	total_words_sum = 0
	for key, value in sorted_word_frequency_list:
		total_words_sum += value

	#get top 20 words to display in table
	if len(sorted_word_frequency_list) > 20 :
		sorted_word_frequency_list = sorted_word_frequency_list[:20]

	#create our final list, words + frequency counts + percentage
	final_list = []
	for key, vale in sorted_word_frequency_list:
		percentage_value = float(value * 100) / total_words_sum
		final_list.append(key, value, round(percentage_value, 4))

	print_headers = ['Word', 'Frequency', 'Frequency Percentage']

	


#parse & format Data
