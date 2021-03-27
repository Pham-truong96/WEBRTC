# video_url = "https://youtu.be/rhXAdST3S2c?list=RDrhXAdST3S2c"
# import vlc
import time

# vlc_ins = vlc.Instance()
# player = vlc_ins.media_player_new()
# player.set_mrl(video_url)
# player.play()
# time.sleep(4)
# fps = player.get_fps()
# player.stop()
# print('video fps is: ', fps)

# importing vlc module 
import vlc 
  
# importing pafy module 
import pafy 
  
# url of the video 
url = "https://meet.jit.si/ExoticFootagesGuessWhere"
  
# creating pafy object of the video 
video = pafy.new(url) 
  
# getting best stream 
best = video.getbest() 
  
# creating vlc media player object 
media = vlc.MediaPlayer(best.url) 
  
# start playing video 
media.play() 
# media.play()
print('video fps is: ', fps)
time.sleep(4)

fps = media.get_fps()

media.stop()

print('video fps is: ', fps)