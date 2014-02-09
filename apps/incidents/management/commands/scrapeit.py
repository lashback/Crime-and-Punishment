#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
import csv
import requests
import os
#from pattern.web import URL
from BeautifulSoup import BeautifulSoup
#import lxml.html, urllib2, urlparse
import glob


from time import strptime, strftime
from string import split
from django.core.management.base import BaseCommand
from apps.incidents.models import *
from settings.common import SITE_ROOT

import datetime

working_dir = os.path.join(SITE_ROOT, '../data')
#directory = os.path.join(working_dir, 'test/archive.ci.chamapign.il.us/cpd-reports/arms/')
list_date = []
today = datetime.date.today()
list_date.append(today)
directory = os.path.join(working_dir, str(list_date[0]))
print directory
class Command(BaseCommand):

	def handle(self, *args, **options):
	#get most recent
	#save the pdf off the wesbite:
	#####HOW HOW DO I DO THIS?#####
	#requests. Get. Fuck. get most recent via Beautiful Soup#
	
	#url = URL(pdf_url)
	#f = open('url', 'wb')
	#f.write(url.download(cached=False))
	#f.close()

	#run a quick pdftotext script
	#subprocess.call
	#or os.system. let's do that. Basically get path of that fucker, and FUCK IT UP.

		#but let's work with a test case for now. 

#		self.get_pdfs()
#		self.convert_to_text()
		self.load_into_db()

	#def get_most_recent_pdf(self):
		#pass

	def get_pdfs(self):
		champaign_base = 'http://archive.ci.champaign.il.us/cpd-reports/'

		os.system('wget --random-wait -nd -r -e robots=off -A.PDF -P %s %s' % (directory, champaign_base))
		#maybe this can just be an os.system command
		#make it a date
		# fetch the page
		#res = urllib2.urlopen(champaign_base)

		# parse the response into an xml tree
		#tree = lxml.html.fromstring(res.read())

		# construct a namespace dictionary to pass to the xpath() call
		# this lets us use regular expressions in the xpath
		# iterate over all <a> tags whose href ends in ".pdf" (case-insensitive)
		#for node in tree.xpath('//a[re:test(@href, "\.PDF$", "i")]'):
		    # print the href, joining it to the base_url
		 #   pdf = urlparse.urljoin(base_url, node.attrib['href'])
		  #  os.system('wget -P %s ')
		#r = requests.get(champaign_base)
		#pdf_soup = BeautifulSoup(r.text)

		#maketoday's date 



		###########################################
		##Alternatively, I can set up a function through Soup that will grab the urls
		##DEFINITELY need some way to see whether it's already been crawled. Could bite us in the ass. 
		##


	def convert_to_text(self):
		pdfs_list = glob.glob(directory + '/*.PDF')
		for pdf in pdfs_list:
			print pdf 
			os.system('pdftotext %s -layout'%pdf)

		print "hopefully not in here"

		#first check to see if it has been turned into text



	
	def load_into_db(self):			
		
		def clean(string):
			line = re.compile('\n')
			excess_spaces = re.compile('\s{2,}')
			string = re.sub(line, "", string)
			string = re.sub(excess_spaces, " ", string)

			return string
		
		#print "i'm in something"
		text_files = glob.glob(directory + '/*.txt')
	#	print text_files
		for t in text_files:
			#print t
			with open (t, "r") as livefile:
				data = livefile.read()

			header_pattern = re.compile('\f.*\n.*')
			strip_headers = re.sub(header_pattern,'', data)
		#	print strip_headers
			#print strip_headers

			pattern = re.compile('(?=(\d{5}\s+)((.|\n)*?)(LOCATION: )((.|\n)*?)(OCCURRED: )(.*?)(REPORTED: )((.|\n)*?)(OFFICER: )((.|\n)*?)(SUMMARY: )((.|\n)*?)((PROPERTY: )((.|\n)*?))?(PEOPLE: )((.|\n)*?)((ARRESTS: )((.|\n)*?))?(C\d{2}-\d{5}|\Z))')
			#currently, when people is NOT followed by an arrest, shit goes to shit. 
	#with properties.. (nonfunctional)
	#(?=(\d{5}\s+)((.|\n)*?)(LOCATION: )((.|\n)*?)(OCCURRED: )(.*?)(REPORTED: )((.|\n)*?)(OFFICER: )((.|\n)*?)(SUMMARY: )((.|\n)*?)((PROPERTY: )((.|\n)*?))?(PEOPLE: )((.|\n)*?)((ARRESTS: )((.|\n)*?))?(C13-\d{5}|\Z))
	#no property
	#(?=(\d{5}\s+)((.|\n)*?)(LOCATION: )((.|\n)*?)(OCCURRED: )(.*?)(REPORTED: )((.|\n)*?)(OFFICER: )((.|\n)*?)(SUMMARY: )((.|\n)*?)(PEOPLE: )((.|\n)*?)((ARRESTS: )((.|\n)*?))?(C13-\d{5}|\Z))
			#print strip_headers
			incidents = pattern.findall(strip_headers)
			#print incidents

			j = 0
			#write function that eats extra whitespace characters. 

			for i in incidents:
		#		print i
				j += 1
			#	print ('This is the whole thing<<<<<<<<<<<<<<<<<<<<<< \n %s \n  >>>>>>>>>>>>>>that is the end' % (i,))
		#		print j
				code = clean(i[0].strip())
#				print code
				description = clean(i[1].strip())
#				print description
				location = clean(i[4].strip())
#				print location
				datetime_occurred = clean(clean(i[7].strip()))
#				print datetime_occurred
				datetime_reported = clean(i[9].strip())
#				print datetime_reported
				reporting_officer = clean(i[12].strip())
#				print reporting_officer
				summary = clean(i[15].strip())
#				print "Summary"
				#use re to get rid of \n
			#	print summary

				properties = i[19].strip()
		#		print properties
				#### TEST REGION!!!
			#	people = i[23].strip()
			#	arrests = i[27].strip()
			#	arrests += i[28].strip()
				#########

				
				people = i[22].strip()
			#	print ('PEOPLE THIS IS THE START OF PEOPLE \n %s \n AND THIS IS THE END OF THE PEOPLE SELECTOR!!!' % people)
				arrests = i[26].strip()
				arrests += i[27].strip()
				#print arrests


				#arrest_pattern = re.compile('(.*)(AGE: )(\d+)\s+(SEX: )(M|F)(\s+)(.*)\n(.*)(CHARGE: )(\w+)\s+(.*)\n(.*)(AT: )(.*)(BY: )(.*)')
				arrest_pattern = re.compile('(.*)(AGE: )(\d+)\s+(SEX: )(M|F)(\s+)(.*)\n(.*)(CHARGE: )(\w+)\s+(.*)\n(.*)(AT: )(.*)(BY: )(.*)')
				arrests_re = arrest_pattern.findall(arrests)
				for a in arrests_re:
					arrestee = 	clean(a[0].strip())
					age = 		clean(a[2].strip())
					sex = 		clean(a[4].strip())
					address = 	clean(a[6].strip())
					charge_text=clean(a[9].strip())
					charge_code=clean(a[10].strip())
					arrest_location = clean(a[13].strip())
					arresting_officer = clean(a[15].strip())

					print arresting_officer
					print arrest_location
					#print a



			# (C\d{2}-\d{5}\s+)(.*?)(\s{3,})(.*?)(LOCATION: )(.*?)(\n)

			#(C\d{2}-\d{5}\s+)(.*?)(\s{3,})(.*?)(LOCATION: )(.*?)(\n+)(\s+)(OCCURRED: )(.*?)(REPORTED: )(.*?)(\n+)(\s+)(OFFICER: )(.*?)(\n+)(\s+)(SUMMARY: )

			#

#Pe

#arrests
	#(.*)(AGE: )(\d+)\s+(SEX: )(M|F)(\s+)(.*)\n(.*)(CHARGE: )(\w+)\s+(.*)\n(.*)(AT: )(.*)(BY: )(.*)

#how do we parse people?
#have Victim pattern. Repeat as necessary. Victim is mandatory at least once.


#((VICTIM)\s+AGE: (.*)SEX: (M|F)(.*))|(VICTIM|OFFENDER)(.*)

#Have offender hattern

#TODO:
#ARRESTS: (.*)(AGE: )(\d+)\s+(SEX: )(M|F)(\s+)(.*)\n(.*)(CHARGE: )(\w+)\s+(.*)\n(.*)(AT: )(.*)(BY: )(.*)
#PEOPLE: ((VICTIM)\s+AGE: (.*)SEX: (M|F)(.*))|(VICTIM|OFFENDER)(.*)
#PROPERTY: (DAMAGED|BURNED|STOLEN|LOST|NONE)(.*)(\d+)(.*)




'''

(?=
0	(\d{5}\s+)
1	(
2		(.|\n) *?)
3	(LOCATION: )
4	(
5		(.|\n) *?)
6	(OCCURRED: )
7	(.*?)
8	(REPORTED: )
9	(
10		(.|\n)*?)
11	(OFFICER: )
12	(
13		(.|\n)*?)
14	(SUMMARY: )
15	(
16		(.|\n)*?)
17	(
18		(PROPERTY: )
19		(
20			(.|\n)*?) )?
21	(PEOPLE: )
22	(
23		(.|\n)*?)
24	(
25		(ARRESTS: )
26		(
27			(.|\n)*?))?
28	(C13-\d{5}|\Z))?


'''