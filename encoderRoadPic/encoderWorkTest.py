import gaugette.rotary_encoder
import gaugette.switch
 
A_PIN  = 7
B_PIN  = 9
SW_PIN = 8
 
encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(A_PIN, B_PIN)
encoder.start()
switch = gaugette.switch.Switch(SW_PIN)
last_state = None
 
while 1:
    delta = encoder.get_delta()
    if delta!=0:
        print "rotate %d" % delta
 
    sw_state = switch.get_state()
    if sw_state != last_state:
        print "switch %d" % sw_state
        last_state = sw_state
