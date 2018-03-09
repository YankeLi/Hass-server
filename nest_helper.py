import requests
import json
import operator
import glob
import os
import threading

class nest_function:
	def __init__(self,host,device_name,tts):
		self.device_name = device_name
		self.host=host
		self.tts=tts

	def snap_shot_image(self,name='now'):
			response=requests.get('http://localhost:8123/api/camera_proxy/camera.{}'.format(self.device_name))
			with open('./picture/nest_{}.jpg'.format(name),'wb') as file:     
				file.write(response.content)
			#self.tts.talk("Saving the picture of {}".format(name))
	def snap_shot_response(self,width=-1):
			self.snap_shot_image()
			#response=requests.get('http://{0}:8123/api/camera_proxy/camera.{1}'.format(host,self.device_name))
			#response.content.set_header("Content_Type","image/jpeg")
			#image.writeto(response)
			self.snap_shot_image()
			img = open('./picture/nest_now.jpg')
			return img
	def face_detect_response(self):
			#改了名字和注释
			self.snap_shot_image("now")
	
			def find_max_key(dict_in):
				return max(dict_in.items(),	key=operator.itemgetter(1))[0]
	
			def get_token():
				headers = {'Authorization': 'Basic YXBwOio='}
				token = requests.post(
					'http://######/oauth/token?username=admin&password=admin&grant_type=password',
					headers=headers
					)
				resp=token.json()["access_token"]
				return resp
	
			def face_detect(token):
				headers = {'Authorization': 'Bearer {}'.format(token)
							}
				files = {
				'image': ('./nest_now.jpg', open('./picture/nest_now.jpg', 'rb')),
				#'image': ('./picture/nest_now.jpg', open('./picture/nest_yanke.jpg', 'rb')),
				'return_landmark': (None, '0'),
				'return_attributes': (None, 'age,gender,smiling,ethnicity,emotion,headpose')
				}
				resp = requests.post(
					'http://######//faceplusplus/facepp/detect',
					headers=headers,
					files=files
					)
				return resp
			while(1):
				token=get_token()
				json_resp=face_detect(token).json()
				print("trying")
				if(json_resp!=None and json_resp["data"]!=None):
					break
	
			print('json_resp=',json_resp)
#			if(json_resp["data"]==None):
#				self.tts.talk("Please try again")
#				return "Please try again"
	
			faces = json_resp["data"]["faces"]
			cnt=len(json_resp["data"]["faces"])
			res=""
			if(cnt==0):
				self.tts.talk("No face detected")
				return "No face detected"
			if(cnt>1):
				res+="I see {} of people,".format(cnt)
			for i in range(cnt):
				if(i==0):
					tail='st'
				elif(i==1):
					tail='nd'
				elif(i==2):
					tail='rd'
				else:
					tail='th'
				gender 		= faces[i]["attributes"]["gender"]["value"]
				age 		= int(faces[i]["attributes"]["age"]["value"])
				sex			= gender=='Male' and 'he' or 'she'
				emotion	= find_max_key(faces[i]["attributes"]["emotion"])
				likely 		= int(faces[i]["attributes"]["emotion"]["{}".format(emotion)])
				ethnicity 	= faces[i]["attributes"]["ethnicity"]["value"]
				if(emotion=="happiness"):
					emotion="happy"
				if(emotion=="disgust"):
					emotion="disgusted"
				if(emotion=="sadness"):
					emotion="sad"
				if(emotion=="surprise"):
					emotion="surprised"
				if(emotion=="fear"):
					emotion="afraid"
				if(emotion=="anger"):
					emotion="angry"
				if(cnt>1):
					res+="the {0}{1} person is likely a {2} year old {3} {4}, \
					and there is a {5}% chance that {6} looks {7}."	\
					.format(i+1,tail,age,ethnicity,gender,likely,sex,emotion)
				else:
					res+="I see a {0} {1}, who is about {2} years of age, there is a {3}% chance that {4} looks {5}.".format(ethnicity,gender,age,likely,sex,emotion)
			self.tts.talk(res)
			return json_resp
	
	def face_compare_response(self):
			res_name=""
			flag=0
			cnt_final=0
			self.snap_shot_image("now")
			def get_token():
				headers = {'Authorization': 'Basic YXBwOio='}
				token = requests.post(
					'http://######//oauth/token?username=admin&password=admin&grant_type=password',
					headers=headers
					)
				resp=token.json()["access_token"]
				return resp
	
			def face_compare(token,name):
				headers = {'Authorization': 'Bearer {}'.format(token)
							}
				files = {
					'image1': (	'./picture/nest_now.jpg', open('./picture/nest_now.jpg', 'rb')),
					'image2': (	'./picture/nest_{}.jpg'.format(name), open('./picture/nest_{}.jpg'.format(name), 'rb'))
				}
				resp = requests.post(
					'http://######/faceplusplus/facepp/compare',
					headers=headers,
					files=files
					)
				json_resp=resp.json()["data"]
				print("compareresp=",json_resp)
				if(json_resp==None):
					return -1
				if(json_resp["faces1"]==[]):
					return -2
				return json_resp["confidence"]
	
	
			#confidence=face_compare(token)
			threads = []
			def compare(name):
				nonlocal res_name
				nonlocal flag
				while(1):
					token=get_token()
					confidence=face_compare(token,name)
					if(confidence!=-1):
						break
				if(confidence==-2):
					#self.tts.talk("no face detected")
					flag=-1
					return "no face detected"
				if(confidence>70):
					res_name+=name
					print(name)
					print(confidence)
					#self.tts.talk("this is {}".format(name))
					return name
				print(name)
				print(confidence)
	
			for fullname in glob.glob(os.path.join('./picture/', '*.jpg')):
				name=fullname.split('/')[-1].split('_')[-1].split('.')[0]
				if(name=="now"):
					continue
	
				t1 = threading.Thread(target=compare,args=[name])
				threads.append(t1)
			for t in threads:
				cnt_final=cnt_final+1
				t.setDaemon(False)
				t.start()
			while(1):
				if(flag!=-1):
					if(res_name!=""):
						return "This is {}".format(res_name)
				else:#no face detected
					return "No face detected"
					break

			# for t in threads:
			# 	t.join()
			return res_name
	
