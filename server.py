import hug
import hassapi_rest
import json
import send_message

#tts
tts = hassapi_rest.tts("lounge")
@hug.get('/tts/say')
def google_tts(message):
	tts.talk(message)
	return "speak"

#sonos
sonos_client = hassapi_rest.sonos("lounge")
@hug.get('/sonos/play_pause')
def sonos_play_pause():
	sonos_client.play_pause()
	return "sonos:play_pause"
@hug.get('/sonos/play')
def sonos_play():
	sonos_client.play()
	return "sonos play"
@hug.get('/sonos/pause')
def sonos_pause():
	sonos_client.pause()
	return "sonos pause"
@hug.get('/sonos/mute')
def sonos_mute():
	sonos_client.mute()
	return "sonos mute"
@hug.get('/sonos/volume')
def sonos_volume_set(volume):
	sonos_client.volume_set(volume)
	return "sonos volume set to {}".format(volume)
@hug.get('/sonos/play_url')
def sonos_play_url(play_url):
	sonos_client.play_url(play_url)
	return "sonos play online resource"

#yeelight
yeelight_client = hassapi_rest.yeelight("light1")
@hug.get('/yeelight/turn_on')
def yeelight_turn_on():
	yeelight_client.turn_on()
	#tts.talk("light is on")
	return "light is on"

@hug.get('/yeelight/turn_off')
def yeelight_turn_off():
	yeelight_client.turn_off()
	#tts.talk("light is off")
	return "light is off"

@hug.get('/yeelight/toggle')
def yeelight_toggle():
	yeelight_client.toggle()
	return "light switch"
@hug.get('/yeelight/brightness')
def yeelight_brightness(brightness):
	yeelight_client.brightness(brightness)
	return "light brightness change to {}".format(brightness)
@hug.get('/yeelight/rgb_color')
def yeelight_rgb_color(r, g, b):
	yeelight_client.rgb_color(r, g, b)
	return "light RGB color set"
@hug.get('/yeelight/color_name')
def yeelight_color_name(color_name):
	yeelight_client.color_name(color_name)
	return "light color change to {}".format(color_name)
@hug.get('/yeelight/color_temp')
def yeelight_color_temp(temp):
	yeelight_client.color_temp(temp)
	return "light temperature change to {}".format(temp)
@hug.get('/yeelight/flash')
def yeelight_flash(duration):
	yeelight_client.flash(duration)
	return "light start flash"
@hug.get('/yeelight/effect')
def yeelight_effect(effect):
	yeelight_client.effect(effect)
	return "{} effect start".format(effect)
@hug.get('/yeelight/stop_effect')
def yeelight_stop_effect():
	yeelight_client.stop_effect()
	return "stop effect"
#nest camera
nest_camera_client = hassapi_rest.nest_camera("office",tts)
@hug.get('/nest_camera/snap_shot_image')
def nest_camera_snap_shot_image(name):
	return nest_camera_client.snap_shot_image(name)

@hug.get('/nest_camera/snap_shot_response', output=hug.output_format.image('jpeg'))
def nest_camera_snap_shot_response(width=-1):
	return nest_camera_client.snap_shot_response(int(width))

@hug.get('/nest_camera/face_detect_response')
def face_detect_response():
	json_resp=nest_camera_client.face_detect_response()
	send_message.face_detect_message(json_resp)
	return json_resp

@hug.get('/nest_camera/face_compare_response')
def face_compare_response():
	return nest_camera_client.face_compare_response()

#harmony
harmony_client = hassapi_rest.harmony("Harmony_Hub")
# LG device code	:49600853
#Vizio device code	:49600477
@hug.get('/harmony/turn_on')
def harmony_turn_on():
	harmony_client.turn_on("49600853")
	return "TV is on"
@hug.get('/harmony/turn_off')
def harmony_turn_off():
	harmony_client.turn_off("49600853")
	return "tv is off"
@hug.get('/harmony/volume_up')
def harmony_volume_up(volume_up):
	harmony_client.volume_up("49600853",volume_up)
	return "turn up the volume by {}".format(volume_up)
@hug.get('/harmony/volume_down')
def harmony_volume_down(volume_down):
	harmony_client.volume_down("49600853",volume_down)
	return "turn down the volume by {}".format(volume_down)
@hug.get('/harmony/hdmi')
def harmony_select_hdmi(hdmi):
	harmony_client.select_hdmi("49600853",hdmi)
	return "switch the HDMI input"
@hug.get('/harmony/next_source')
def harmony_next_source():
	harmony_client.next_source("49600853")
	return ""
@hug.get('/harmony/mute')
def harmony_mute():
	harmony_client.mute("49600853")
	return "mute"
#apple TV
apple_tv_client = hassapi_rest.apple_tv("apple_tv")
@hug.get('/apple_tv/play')
def apple_tv_play():
	apple_tv_client.play()
	return "apple TV play"
@hug.get('/apple_tv/pause')
def apple_tv_pause():
	apple_tv_client.pause()
	return "apple TV pause"
@hug.get('/apple_tv/menu')
def apple_tv_menu():
	apple_tv_client.menu()
	return "apple TV menu"
@hug.get('/apple_tv/top_menu')
def apple_tv_top_menu():
	apple_tv_client.top_menu()
	return "apple tv top menu"
@hug.get('/apple_tv/select')
def apple_tv_select():
	apple_tv_client.select()
	return "apple TV select"
@hug.get('/apple_tv/move')
def apple_tv_move(move):
	apple_tv_client.move(move)
	return "apple TV move"
@hug.get('/apple_tv/play_url')
def apple_tv_play_url(play_url):
	harmony_select_hdmi("InputHdmi3")
	apple_tv_client.play_url(play_url)
	return "apple TV play online resource"


#wemo
wemo_switch_client = hassapi_rest.wemo_switch("wemo1")
@hug.get('/wemo_switch/turn_on')
def wemo_switch_turn_on():
	wemo_switch_client.turn_on()
	#tts.talk("switch is on")
	return "switch is on"

@hug.get('/wemo_switch/turn_off')
def wemo_switch_turn_off():
	wemo_switch_client.turn_off()
	#tts.talk("switch is off")
	return "switch is off"
@hug.get('/wemo_switch/toggle')
def wemo_switch_toggle():
	wemo_switch_client.toggle()

#xiaomi_robot
xiaomi_vacuum_client = hassapi_rest.xiaomi_vacuum("xiaomi_vacuum_cleaner")
@hug.get('/xiaomi_vacuum/clean_spot')
def xiaomi_vacuum_clean_spot():
	xiaomi_vacuum_client.clean_spot()

@hug.get('/xiaomi_vacuum/return_to_base')
def xiaomi_vacuum_return_to_base():
	xiaomi_vacuum_client.return_to_base()

@hug.get('/xiaomi_vacuum/start_pause')
def xiaomi_vacuum_start_pause():
	xiaomi_vacuum_client.start_pause()
	return "robot start/pause"
@hug.get('/xiaomi_vacuum/fan_speed')
def xiaomi_vacuum_set_fan_speed(fan_speed):
	xiaomi_vacuum_client.set_fan_speed(fan_speed)
	return "set robot fan speed to {}".format(fan_speed)
@hug.get('/xiaomi_vacuum/stop')
def xiaomi_vacuum_stop():
	xiaomi_vacuum_client.stop()
	return "robot stop"
@hug.get('/xiaomi_vacuum/turn_on')
def xiaomi_vacuum_turn_on():
	xiaomi_vacuum_client.turn_on()
	#tts.talk("robot is on")
	return "robot is on"
@hug.get('/xiaomi_vacuum/turn_off')
def xiaomi_vacuum_turn_off():
	xiaomi_vacuum_client.turn_off()
	#tts.talk("robot is off")
	return "robot is off"
