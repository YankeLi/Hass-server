import homeassistant.remote as remote
import nest_helper

host = "0.0.0.0" #"192.168.1.177"
api = remote.API(host)

class tts:
	def __init__(self,name):
		self.device_name = name
	def talk(self,message):
		remote.call_service(api,'tts','google_say',\
		{"entity_id":"media_player.{0}".format(self.device_name),"message":message, "language":"en"})

#sonos api
class sonos:
	def __init__(self,name):
		self.device_name = name
	def play_pause(self):
		remote.call_service(api,'media_player','media_play_pause',\
		{'entity_id':'media_player.{0}'.format(self.device_name)})
	def play(self):
		remote.call_service(api,'media_player','media_play',\
	{'entity_id':'media_player.{0}'.format(self.device_name)})
	def pause(self):
		remote.call_service(api,'media_player','media_pause',\
	{'entity_id':'media_player.{0}'.format(self.device_name)})
	def mute(self):
		#get the mute state of sonos, will be used in media_mute api.
		sonos_state = remote.get_state(api,'media_player.{0}'.format(self.device_name)) 
		mute_state  = "false" if sonos_state.attributes['is_volume_muted'] else "true"

		remote.call_service(api,'media_player','volume_mute',\
		{'entity_id':'media_player.{0}'.format(self.device_name),\
		"is_volume_muted":"{}".format(mute_state)})
	def volume_set(self,volume):
		remote.call_service(api,'media_player','volume_set',\
		{"entity_id":"media_player.{}".format(self.device_name),"volume_level":'{}'.format(int(volume)/100)})

	def play_url(self,url):
		'''play url from internet or local'''
		remote.call_service(api,'media_player','play_media',\
		{"entity_id":"media_player.{}".format(self.device_name),"media_content_id":"{}".format(url),"media_content_type":"VIDEO"})

class yeelight:
	def __init__(self,name):
		self.device_name = name
	def turn_on(self):
		remote.call_service(api,'light','turn_on',\
		{'entity_id':'light.{0}'.format(self.device_name)})
	def turn_off(self):
		remote.call_service(api,'light','turn_off',\
		{'entity_id':'light.{0}'.format(self.device_name)})
	def toggle(self):
		remote.call_service(api,'light','toggle',\
		{'entity_id':'light.{0}'.format(self.device_name)})
	def brightness(self,brightness):
		remote.call_service(api,'light','turn_on',\
		{'entity_id':'light.{0}'.format(self.device_name),"brightness":"{}".format(brightness)})	
	def rgb_color(self,r,g,b):
		remote.call_service(api,'light','turn_on',\
		{'entity_id':'light.{0}'.format(self.device_name),"rgb_color":[r,g,b]})	
	def color_name(self,color_name):
		remote.call_service(api,'light','turn_on',\
		{'entity_id':'light.{0}'.format(self.device_name),"color_name":'{}'.format(color_name)})	
	def color_temp(self,temp):
		remote.call_service(api,'light','turn_on',\
		{'entity_id':'light.{0}'.format(self.device_name),"color_temp":'{}'.format(temp)})	
	def flash(self,duration):
		remote.call_service(api,'light','turn_on',\
		{'entity_id':'light.{0}'.format(self.device_name),"flash":'{}'.format(duration)})	
	'''	effect_list: Disco,Slow Temp,Strobe epilepsy!,Strobe color,Alarm,Police,Police2,Christmas,
		RGB,Random Loop,Fast Random Loop,Slowdown,WhatsApp,Facebook,Twitter,Stop'''
	def effect(self,effect):
		remote.call_service(api,'light','turn_on',\
		{'entity_id':'light.{0}'.format(self.device_name),"effect":'{}'.format(effect)})	
	def stop_effect(self):
		remote.call_service(api,'light','turn_on',\
		{'entity_id':'light.{0}'.format(self.device_name),"effect":'{}'.format('Stop')})

class nest_camera:
	def __init__(self,device_name,tts):
		self.helper = nest_helper.nest_function(host,device_name,tts)

	def snap_shot_image(self,name='now'):
		return self.helper.snap_shot_image(name)

	def snap_shot_response(self,width=-1):
		return self.helper.snap_shot_response(width)

	def face_detect_response(self):
		return self.helper.face_detect_response()
	
	def face_compare_response(self):
		return self.helper.face_compare_response()

class apple_tv:
	def __init__(self,name):
		self.device_name = name
	def play(self):
		remote.call_service(api,'remote','send_command',\
		{"entity_id":"remote.{}".format(self.device_name),"command":"play","device":""})
	def pause(self):
		remote.call_service(api,'remote','send_command',\
		{"entity_id":"remote.{}".format(self.device_name),"command":"pause","device":""})
	def menu(self):
		remote.call_service(api,'remote','send_command',\
		{"entity_id":"remote.{}".format(self.device_name),"command":"menu","device":""})
	def top_menu(self):
		remote.call_service(api,'remote','send_command',\
		{"entity_id":"remote.{}".format(self.device_name),"command":"top_menu","device":""})
	def select(self):
		remote.call_service(api,'remote','send_command',\
		{"entity_id":"remote.{}".format(self.device_name),"command":"select","device":""})
	def move(self,direction):
		'''left,right,up,down'''
		remote.call_service(api,'remote','send_command',\
		{"entity_id":"remote.{}".format(self.device_name),"command":direction,"device":""})
	def play_url(self,url):
		'''play url from internet or local'''
		remote.call_service(api,'media_player','play_media',\
		{"entity_id":"media_player.{}".format(self.device_name),"media_content_id":"{}".format(url),"media_content_type":"VIDEO"})
class harmony:
	def __init__(self,name):
		self.device_name = name
	def turn_on(self,device):
		remote.call_service(api,'remote','send_command',\
		{"entity_id":"remote.{}".format(self.device_name),"command":"PowerOn","device":device})
	def turn_off(self,device):
		remote.call_service(api,'remote','send_command',\
		{"entity_id":"remote.{}".format(self.device_name),"command":"PowerOff","device":device})
	def volume_up(self,device,volume):
		for repeat in range(int(volume)):
			remote.call_service(api,'remote','send_command',\
			{"entity_id":"remote.{}".format(self.device_name),"command":"VolumeUp","device":device})
	def volume_down(self,device,volume):
		for repeat in range(int(volume)):
			remote.call_service(api,'remote','send_command',\
			{"entity_id":"remote.{}".format(self.device_name),"command":"VolumeDown","device":device})
	def select_hdmi(self,device,hdmi):
		remote.call_service(api,'remote','send_command',\
		{"entity_id":"remote.{}".format(self.device_name),"command":hdmi,"device":device})
	def next_source(self,device):
		remote.call_service(api,'remote','send_command',\
		{"entity_id":"remote.{}".format(self.device_name),"command":"InputNext","device":device})
	def mute(self,device):
		print("TV mute")
		remote.call_service(api,'remote','send_command',\
		{"entity_id":"remote.{}".format(self.device_name),"command":"Mute","device":device})

class wemo_switch:
	device_name = ''
	def __init__(self,name):
		self.device_name = name
	def turn_on(self):
		remote.call_service(api,'switch','turn_on',\
		{'entity_id':'switch.{0}'.format(self.device_name)})
	def turn_off(self):
		remote.call_service(api,'switch','turn_off',\
		{'entity_id':'switch.{0}'.format(self.device_name)})
	def toggle(self):
		remote.call_service(api,'switch','toggle',\
		{'entity_id':'switch.{0}'.format(self.device_name)})

class xiaomi_vacuum:
	device_name = ''
	def __init__(self,name):
		self.device_name = name
	def clean_spot(self):
		remote.call_service(api,'vacuum','clean_spot',\
		{'entity_id':'vacuum.{0}'.format(self.device_name)})
	def return_to_base(self):
		remote.call_service(api,'vacuum','return_to_base',\
		{'entity_id':'vacuum.{0}'.format(self.device_name)})
	def start_pause(self):
		remote.call_service(api,'vacuum','start_pause',\
		{'entity_id':'vacuum.{0}'.format(self.device_name)})
	def set_fan_speed(self,speed):
		remote.call_service(api,'vacuum','set_fan_speed',\
		{'entity_id':'vacuum.{0}'.format(self.device_name),"fan_speed":speed})
	def stop(self):
		remote.call_service(api,'vacuum','stop',\
		{'entity_id':'vacuum.{0}'.format(self.device_name)})
	def turn_on(self):
		remote.call_service(api,'vacuum','turn_on',\
		{'entity_id':'vacuum.{0}'.format(self.device_name)})
	def turn_off(self):
		remote.call_service(api,'vacuum','turn_off',\
		{'entity_id':'vacuum.{0}'.format(self.device_name)})

