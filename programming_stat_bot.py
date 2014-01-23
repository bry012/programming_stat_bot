
import praw
import re
import time
import datetime
import calendar
class programming_stat_bot(object):
	def __init__(self,username,password):
		self.user_agent = ("First Bot 0.1 by /u/bry012")
		self.r = praw.Reddit(user_agent=self.user_agent)
		self.r.login(username,password)
		self.last_day_of_current_month = 0
		self.month_of_last_submission = 0
		self.submission_for_month = False
		self.main()
		
		
	def create_language_dict(self):
		f = open("./languages.txt","r")
		#[mentions,submissions,regex]
		self.language_dict = {x.strip().lower(): [0,{},""] for x in f.readlines()}

	def modify_all_languages(self):
		for language in self.language_dict.keys():
			self.language_dict[language][2] = self.modify_languages_for_regex(language)
		
	
	def modify_languages_for_regex(self,language):
			if "+" in language:
				language = language.replace("+","\+")
			elif language == "c":
				language = language.replace("c",r'(?<!objective-)\bc\b([^\+#\w\d]|$)')
			elif len(language) == 1:
	
				language = language.replace(language,r"[^']\b"+language+r'\b[^.]')
			return language
			
	def get_subreddit_subs(self,subreddit,request_limit):
		programming = self.r.get_subreddit(subreddit)
		self.submissions = programming.get_top_from_month(limit=request_limit)
		
	def create_submission_list(self):
		for submission in self.submissions:
			
			self.populate_language_dict(submission)
		

	def populate_language_dict(self, submission):
		title = submission.title.lower()
		ups = submission.ups
		url = submission.url	
		for key in self.language_dict.keys():
			ups_list = self.language_dict[key][1].keys()
			
			if len(key) > 1:
				key_regex = "(^|\\W)" + self.language_dict[key][2] + "(\\W|$)"	
			else:
				key_regex = self.language_dict[key][2]

			if(re.search(key_regex,title)):
				self.language_dict[key][0] += 1
				if len(self.language_dict[key][1]) < 10:
					self.language_dict[key][1][ups] = (title,url)

				elif(ups > min(ups_list)):
					
					del self.language_dict[key][1][min(ups_list)]
					self.language_dict[key][1][ups] = (title,url)

	def produce_language_stats(self,language):	
		counter = 1
		output = ""
		output +="""%s Mentions: %d  \n\n"""%(language.title(),self.language_dict[language][0])

		for ups in sorted(self.language_dict[language][1].keys(), reverse=True):
				output += "%d. [%s](%s) : %d  \n"% (counter,self.language_dict[language][1][ups][0],self.language_dict[language][1][ups][1],ups)
				counter+=1
		return output + "\n"

	def sort_language_mentions(self):
		self.language_mentions = [self.language_dict[x][0] for x in self.language_dict.keys()]
		self.language_mentions.sort()

	def calculate_top_six(self):
		six_most_mentioned = min(self.language_mentions[-5:])
		self.top_six = six_most_mentioned

	def create_submission_text(self):
		submission_text = self.submission_intro
		for key in self.language_dict.keys():
			limit = min(self.language_mentions[-5:])
			if self.language_dict[key][0] >= limit and self.language_dict[key][0] != 0:
				submission_text += self.produce_language_stats(key)
		return submission_text

	def create_submission(self,subreddit,title,url,submission_text):
		self.submission = self.r.submit(subreddit,title,url=url)
		self.submission.add_comment(submission_text)
		self.submission_for_month = True
		f = open("./submission_id.txt","w")
		f.write(self.submission.id)
		f.close()

	def read_in_submission_id(self):
		f = open("./submission_id.txt", "r")
		self.submission_id = f.readline()

	def monitor_submission(self, submission_id):
		search = re.compile("^programming_stat_bot:\w+")
		submission = self.r.get_submission(submission_id = submission_id)
		submitted = True
		while(True):
			comments = submission.comments
			day = datetime.datetime.now().day
			month = datetime.datetime.now().month
			year = datetime.datetime.now().year
			last_day_of_month = calendar.monthrange(year,month)[1]
			
			for comment in comments:
				if comment.id not in self.comment_ids:
					self.comment_ids.append(comment.id)
					if search.search(comment.body):
						splitted = comment.body.split(":")
						if len(splitted) == 2:
							language = splitted[1].strip().lower()
							if language in self.language_dict.keys():
								comment.reply(self.produce_language_stats(language))
							else:
								comment.reply("Sorry, language not supported. Please, PM this bot or make an issue at my Github repository [programming_stat_bot](https://github.com/bry012/programming_stat_bot)")
			if submission_id != self.submission_id:
				return False
			elif last_day_of_month == day and self.month_of_last_submission != month:
				self.month_of_last_submission = month
				self.submission.delete()
				self.main()
			else:	
				submission.refresh()
				time.sleep(10)


	def main(self):
		self.language_mentions = []
		self.top_six = []
		self.comment_ids = []
		self.submissions = ""
		self.submission = ""
		self.submission_id = ""
		self.submission_intro = """
	Hello, /r/programming! My name is /u/programming_stat_bot and my job is to keep track of how 
	often a programming language is mentioned in the title of a submission to /r/programming. I then sort 
	through the months top submissions for each language and list the top 10 submissions for each language based on upvotes. 
	This bot is still in the infant stages so if you have any questions or suggestions send me a personal message or head to 
	my github repository, [programming_stat_bot](https://github.com/bry012/programming_stat_bot).

	"""

		self.create_language_dict()
		self.modify_all_languages()
		self.get_subreddit_subs("programming",1000)
		self.create_submission_list()
		self.sort_language_mentions()
		self.calculate_top_six()
		self.create_submission("bry012test","testPost","http://www.google.com",self.create_submission_text())
		self.read_in_submission_id()
		self.monitor_submission(self.submission_id)

if __name__ == "__main__":
	f = open("user_info.txt","r")
	username, password = f.readlines()
	bot = programming_stat_bot(username.strip(),password.strip())




	

