import urllib
import json
import time

serviceurl = 'https://api.havenondemand.com/1/api/async/'
sevice_sec_url = 'https://api.havenondemand.com/1/job/status/'
api_key = 'ec5e8362-5ec3-453e-a5ee-3062e8c79d77'

#audio files 
sample_audio = 'https%3A%2F%2Fwww.havenondemand.com%2Fsample-content%2Fvideos%2Fhpnext.mp4'
sample_audio1 = 'http://www.answeringserviceunited.com/wp-content/uploads/2011/06/UCC_PIPER_PETS1.mp3'
sample_audio2 = 'http://www.answeringserviceunited.com/wp-content/uploads/2011/06/abby-heating-and-air.mp3'
sample_audio3 = 'http://www.answeringserviceunited.com/wp-content/uploads/2011/06/ucc_LAKES_CABINETS.mp3'
#sample_audio4 = 'http://empowerzone.me/wp-content/uploads/2016/05/angry-ANGRY-BT-customer-Very-Funny.mp3'
sample_audio5 = 'http://empowerzone.me/wp-content/uploads/2016/05/Angry-Customer-yells-at-Dell-Rep.mp3'

test_job_id1 =''
test_job_id2 =''
test_job_id3 =''

#JSON
url = serviceurl+'recognizespeech/v1?'+'url='+sample_audio1+'&apikey='+api_key
print 'Retrieving', url

#jobID getting created
uh = urllib.urlopen(url)
data = uh.read()
js = json.loads(str(data))
job_id_created = json.dumps(js)

#getting jobID  
ex_job_id = js["jobID"][0:]
#print 'extracted job id=',ex_job_id

#change job ID
sec_url = sevice_sec_url+ex_job_id+'?apikey='+api_key
uhs = urllib.urlopen(sec_url)
data_s = uhs.read()

try: sec_js = json.loads(str(data_s))
except: sec_js = None
while sec_js['status'] != 'finished':
	time.sleep(3)
	print 'waiting'
	print sec_js['status']
	sec_url = sevice_sec_url+ex_job_id+'?apikey='+api_key
	uhs = urllib.urlopen(sec_url)
	data_s = uhs.read()
	sec_js = json.loads(str(data_s))

try: sec_js = json.loads(str(data_s))
except: sec_js = None

#extracting converted text content
ext_content = sec_js['actions'][0]['result']['document'][0]['content']
print ext_content

#sentimental API
senti_url = 'https://api.havenondemand.com/1/api/sync/analyzesentiment/v1?text='+ext_content+'&language=eng&apikey=ec5e8362-5ec3-453e-a5ee-3062e8c79d77'
s_uh = urllib.urlopen(senti_url)
senti_data = s_uh.read()

senti_js = json.loads(str(senti_data))
js_th= json.dumps(senti_js, indent=4)

#extracting sentiments and score from converted text
ext_sentiment = senti_js['aggregate']['sentiment']
if ext_sentiment == 'positive':
	#check score
	ext_score = senti_js['aggregate']['score']
	ext_score = (ext_score*100)
	ext_score = int(ext_score)
	if ext_score <= 45:
		ext_score = 100-ext_score
		print 'Customer is ',ext_score,'% dissatisfied'
	else:	
		print 'Customer is ',ext_score,'% satisfied'
		
elif ext_sentiment == 'negative':
	#check score
	ext_score = senti_js['aggregate']['score']
	ext_score = (ext_score*100*(-1))
	ext_score = int(ext_score)
	if ext_score <= 45:
		ext_score = 100-ext_score
		print 'Customer is ',ext_score,'% satisfied'
	else:	
		print 'Customer is ',ext_score,'% dissatisfied'
		
else:
	print "neutral conversation"
		








