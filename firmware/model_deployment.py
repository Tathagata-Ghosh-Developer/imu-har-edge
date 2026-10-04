
import time
import network
import socket
from machine import Pin, SPI, LED
from lsm6dsox import LSM6DSOX
import math

# --- Network Configuration ---
# Wi-Fi credentials and the PC's address live in wifi_secrets.py (gitignored);
# see wifi_secrets_example.py
from wifi_secrets import SSID, KEY, PC_IP
PORT = 5007  # Port for predictions (different from raw IMU data port 5006)
# -----------------------------

# --- Sampling and Prediction Configuration ---
SAMPLE_RATE_HZ = 60
SAMPLE_INTERVAL_MS = int(1000 / SAMPLE_RATE_HZ)  # ~16.67ms
MAJORITY_VOTE_WINDOW = 5  # Number of predictions to smooth over
SEND_INTERVAL_MS = 500  # Send prediction every 500ms (2 Hz) for stable display
# -----------------------------

spi = SPI(5)
cs = Pin("PF6", Pin.OUT_PP, Pin.PULL_UP)
lsm = LSM6DSOX(spi, cs=cs)
red_led = LED("LED_RED")
green_led = LED("LED_GREEN")
blue_led = LED("LED_BLUE")

def predict_activity_features(features):
    if features[76] <= 12.695316:
            if features[50] <= 0.776430:
                    if features[22] <= 0.339294:
                            if features[13] <= 0.706696:
                                    if features[39] <= 0.006490:
                                            if features[22] <= 0.189148:
                                                    if features[63] <= 7.659914:
                                                                return 1 # Leaf node, pred=1
                                                    else:
                                                                return 1 # Leaf node, pred=1
                                                
                                            else:
                                                    if features[3] <= 0.628785:
                                                                return 1 # Leaf node, pred=1
                                                    else:
                                                                return 1 # Leaf node, pred=1
                                                
                                        
                                    else:
                                            if features[88] <= 1179.198181:
                                                    if features[108] <= 118.643093:
                                                            if features[76] <= 8.605961:
                                                                        return 1 # Leaf node, pred=1
                                                            else:
                                                                    if features[20] <= -0.919794:
                                                                                return 1 # Leaf node, pred=1
                                                                    else:
                                                                            if features[93] <= -1.388550:
                                                                                        return 8 # Leaf node, pred=8
                                                                            else:
                                                                                    if features[41] <= 0.009776:
                                                                                                return 1 # Leaf node, pred=1
                                                                                    else:
                                                                                                return 1 # Leaf node, pred=1
                                                                                
                                                                        
                                                                
                                                        
                                                    else:
                                                            if features[2] <= 0.438354:
                                                                    if features[28] <= 16.510405:
                                                                                return 8 # Leaf node, pred=8
                                                                    else:
                                                                            if features[88] <= 469.582245:
                                                                                        return 1 # Leaf node, pred=1
                                                                            else:
                                                                                        return 1 # Leaf node, pred=1
                                                                        
                                                                
                                                            else:
                                                                    if features[119] <= 0.612663:
                                                                                return 1 # Leaf node, pred=1
                                                                    else:
                                                                                return 1 # Leaf node, pred=1
                                                                
                                                        
                                                
                                            else:
                                                    if features[80] <= 11.096194:
                                                            if features[26] <= 0.081449:
                                                                        return 8 # Leaf node, pred=8
                                                            else:
                                                                        return 8 # Leaf node, pred=8
                                                        
                                                    else:
                                                                return 7 # Leaf node, pred=7
                                                
                                        
                                
                            else:
                                    if features[10] <= 0.730345:
                                                return 10 # Leaf node, pred=10
                                    else:
                                                return 10 # Leaf node, pred=10
                                
                        
                    else:
                            if features[20] <= 0.369885:
                                        return 9 # Leaf node, pred=9
                            else:
                                        return 9 # Leaf node, pred=9
                        
                
            else:
                    if features[22] <= -0.229370:
                            if features[108] <= 14.700001:
                                        return 0 # Leaf node, pred=0
                            else:
                                    if features[13] <= 0.236023:
                                            if features[20] <= -0.368295:
                                                        return 8 # Leaf node, pred=8
                                            else:
                                                        return 8 # Leaf node, pred=8
                                        
                                    else:
                                            if features[88] <= 282.913475:
                                                        return 0 # Leaf node, pred=0
                                            else:
                                                        return 8 # Leaf node, pred=8
                                        
                                
                        
                    else:
                            if features[121] <= 0.263183:
                                    if features[92] <= 0.792694:
                                                return 11 # Leaf node, pred=11
                                    else:
                                                return 11 # Leaf node, pred=11
                                
                            else:
                                        return 10 # Leaf node, pred=10
                        
                
        
    else:
            if features[20] <= -0.717941:
                    if features[108] <= 50203.093750:
                            if features[38] <= 0.046148:
                                    if features[0] <= 0.157990:
                                            if features[43] <= -0.003784:
                                                    if features[44] <= 0.181763:
                                                            if features[2] <= 0.014954:
                                                                    if features[30] <= 0.874845:
                                                                                return 6 # Leaf node, pred=6
                                                                    else:
                                                                            if features[60] <= 2.882385:
                                                                                        return 7 # Leaf node, pred=7
                                                                            else:
                                                                                        return 6 # Leaf node, pred=6
                                                                        
                                                                
                                                            else:
                                                                    if features[42] <= -0.368592:
                                                                                return 6 # Leaf node, pred=6
                                                                    else:
                                                                            if features[103] <= 31.829838:
                                                                                    if features[28] <= 17.532637:
                                                                                            if features[93] <= -22.857672:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                            else:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                        
                                                                                    else:
                                                                                                return 6 # Leaf node, pred=6
                                                                                
                                                                            else:
                                                                                    if features[115] <= 0.989753:
                                                                                                return 6 # Leaf node, pred=6
                                                                                    else:
                                                                                                return 6 # Leaf node, pred=6
                                                                                
                                                                        
                                                                
                                                        
                                                    else:
                                                                return 6 # Leaf node, pred=6
                                                
                                            else:
                                                    if features[88] <= 83772.714844:
                                                                return 8 # Leaf node, pred=8
                                                    else:
                                                                return 6 # Leaf node, pred=6
                                                
                                        
                                    else:
                                            if features[35] <= 0.830982:
                                                    if features[15] <= 0.785928:
                                                            if features[108] <= 55.607426:
                                                                    if features[114] <= 1.213073:
                                                                                return 8 # Leaf node, pred=8
                                                                    else:
                                                                                return 1 # Leaf node, pred=1
                                                                
                                                            else:
                                                                    if features[35] <= 0.748849:
                                                                                return 8 # Leaf node, pred=8
                                                                    else:
                                                                            if features[3] <= 0.341492:
                                                                                    if features[119] <= 3.178939:
                                                                                                return 8 # Leaf node, pred=8
                                                                                    else:
                                                                                                return 7 # Leaf node, pred=7
                                                                                
                                                                            else:
                                                                                        return 8 # Leaf node, pred=8
                                                                        
                                                                
                                                        
                                                    else:
                                                            if features[104] <= 11.444094:
                                                                    if features[39] <= 0.008382:
                                                                            if features[68] <= 300.761429:
                                                                                        return 1 # Leaf node, pred=1
                                                                            else:
                                                                                        return 8 # Leaf node, pred=8
                                                                        
                                                                    else:
                                                                            if features[87] <= 1.604204:
                                                                                    if features[89] <= 2.137326:
                                                                                                return 8 # Leaf node, pred=8
                                                                                    else:
                                                                                                return 1 # Leaf node, pred=1
                                                                                
                                                                            else:
                                                                                        return 8 # Leaf node, pred=8
                                                                        
                                                                
                                                            else:
                                                                    if features[10] <= 0.328518:
                                                                            if features[50] <= 0.123021:
                                                                                    if features[82] <= -42.419441:
                                                                                                return 6 # Leaf node, pred=6
                                                                                    else:
                                                                                                return 8 # Leaf node, pred=8
                                                                                
                                                                            else:
                                                                                    if features[70] <= 14.495221:
                                                                                            if features[9] <= 1.876590:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                            else:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                        
                                                                                    else:
                                                                                            if features[123] <= -2.807617:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                            else:
                                                                                                    if features[95] <= 0.938590:
                                                                                                                return 8 # Leaf node, pred=8
                                                                                                    else:
                                                                                                            if features[114] <= 8.911133:
                                                                                                                        return 6 # Leaf node, pred=6
                                                                                                            else:
                                                                                                                        return 6 # Leaf node, pred=6
                                                                                                        
                                                                                                
                                                                                        
                                                                                
                                                                        
                                                                    else:
                                                                            if features[15] <= 0.959927:
                                                                                    if features[34] <= 0.106155:
                                                                                            if features[108] <= 20905.034180:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                            else:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                        
                                                                                    else:
                                                                                            if features[87] <= 1.933544:
                                                                                                    if features[72] <= 7.398378:
                                                                                                                return 8 # Leaf node, pred=8
                                                                                                    else:
                                                                                                                return 2 # Leaf node, pred=2
                                                                                                
                                                                                            else:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                        
                                                                                
                                                                            else:
                                                                                    if features[73] <= -5.340577:
                                                                                                return 7 # Leaf node, pred=7
                                                                                    else:
                                                                                                return 2 # Leaf node, pred=2
                                                                                
                                                                        
                                                                
                                                        
                                                
                                            else:
                                                    if features[82] <= -46.447769:
                                                            if features[80] <= -35.182194:
                                                                    if features[16] <= 0.527954:
                                                                                return 6 # Leaf node, pred=6
                                                                    else:
                                                                            if features[33] <= -0.961670:
                                                                                        return 6 # Leaf node, pred=6
                                                                            else:
                                                                                        return 8 # Leaf node, pred=8
                                                                        
                                                                
                                                            else:
                                                                    if features[40] <= -0.190472:
                                                                            if features[92] <= 28.904573:
                                                                                    if features[102] <= -23.803719:
                                                                                                return 7 # Leaf node, pred=7
                                                                                    else:
                                                                                                return 7 # Leaf node, pred=7
                                                                                
                                                                            else:
                                                                                        return 6 # Leaf node, pred=6
                                                                        
                                                                    else:
                                                                            if features[15] <= 0.938116:
                                                                                    if features[12] <= 0.033774:
                                                                                            if features[2] <= 0.210144:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                            else:
                                                                                                        return 6 # Leaf node, pred=6
                                                                                        
                                                                                    else:
                                                                                            if features[84] <= 117.858902:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                            else:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                        
                                                                                
                                                                            else:
                                                                                    if features[95] <= 0.983656:
                                                                                                return 6 # Leaf node, pred=6
                                                                                    else:
                                                                                                return 6 # Leaf node, pred=6
                                                                                
                                                                        
                                                                
                                                        
                                                    else:
                                                            if features[83] <= 23.895271:
                                                                    if features[48] <= 0.978248:
                                                                            if features[105] <= 159.768196:
                                                                                    if features[68] <= 334.851578:
                                                                                            if features[80] <= -2.777100:
                                                                                                    if features[23] <= -0.906311:
                                                                                                                return 8 # Leaf node, pred=8
                                                                                                    else:
                                                                                                                return 8 # Leaf node, pred=8
                                                                                                
                                                                                            else:
                                                                                                    if features[89] <= 1.962415:
                                                                                                                return 1 # Leaf node, pred=1
                                                                                                    else:
                                                                                                                return 1 # Leaf node, pred=1
                                                                                                
                                                                                        
                                                                                    else:
                                                                                            if features[3] <= 0.476562:
                                                                                                    if features[1] <= 0.014415:
                                                                                                                return 8 # Leaf node, pred=8
                                                                                                    else:
                                                                                                                return 8 # Leaf node, pred=8
                                                                                                
                                                                                            else:
                                                                                                    if features[65] <= 35.276055:
                                                                                                                return 1 # Leaf node, pred=1
                                                                                                    else:
                                                                                                                return 8 # Leaf node, pred=8
                                                                                                
                                                                                        
                                                                                
                                                                            else:
                                                                                    if features[124] <= 6.347657:
                                                                                            if features[13] <= 0.226562:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                            else:
                                                                                                    if features[64] <= 37.597662:
                                                                                                                return 6 # Leaf node, pred=6
                                                                                                    else:
                                                                                                                return 6 # Leaf node, pred=6
                                                                                                
                                                                                        
                                                                                    else:
                                                                                                return 7 # Leaf node, pred=7
                                                                                
                                                                        
                                                                    else:
                                                                            if features[8] <= 1.725380:
                                                                                    if features[50] <= 0.372530:
                                                                                                return 7 # Leaf node, pred=7
                                                                                    else:
                                                                                                return 6 # Leaf node, pred=6
                                                                                
                                                                            else:
                                                                                    if features[24] <= 0.130554:
                                                                                                return 8 # Leaf node, pred=8
                                                                                    else:
                                                                                            if features[16] <= 0.307985:
                                                                                                    if features[116] <= 23.315431:
                                                                                                                return 8 # Leaf node, pred=8
                                                                                                    else:
                                                                                                                return 7 # Leaf node, pred=7
                                                                                                
                                                                                            else:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                        
                                                                                
                                                                        
                                                                
                                                            else:
                                                                    if features[44] <= 0.170166:
                                                                            if features[82] <= 0.579834:
                                                                                    if features[0] <= 0.334406:
                                                                                            if features[122] <= -0.077210:
                                                                                                    if features[122] <= -0.332092:
                                                                                                            if features[79] <= 3.050890:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                            else:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                        
                                                                                                    else:
                                                                                                            if features[19] <= 0.021530:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                            else:
                                                                                                                    if features[122] <= -0.251648:
                                                                                                                                return 7 # Leaf node, pred=7
                                                                                                                    else:
                                                                                                                                return 8 # Leaf node, pred=8
                                                                                                                
                                                                                                        
                                                                                                
                                                                                            else:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                        
                                                                                    else:
                                                                                            if features[19] <= 0.018442:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                            else:
                                                                                                    if features[82] <= -9.490970:
                                                                                                                return 8 # Leaf node, pred=8
                                                                                                    else:
                                                                                                                return 8 # Leaf node, pred=8
                                                                                                
                                                                                        
                                                                                
                                                                            else:
                                                                                    if features[122] <= -0.098450:
                                                                                            if features[0] <= 0.170099:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                            else:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                        
                                                                                    else:
                                                                                                return 8 # Leaf node, pred=8
                                                                                
                                                                        
                                                                    else:
                                                                            if features[33] <= -0.839508:
                                                                                    if features[19] <= 0.024344:
                                                                                            if features[123] <= 16.632080:
                                                                                                    if features[26] <= -0.907283:
                                                                                                                return 6 # Leaf node, pred=6
                                                                                                    else:
                                                                                                                return 7 # Leaf node, pred=7
                                                                                                
                                                                                            else:
                                                                                                        return 6 # Leaf node, pred=6
                                                                                        
                                                                                    else:
                                                                                            if features[15] <= 0.887472:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                            else:
                                                                                                        return 6 # Leaf node, pred=6
                                                                                        
                                                                                
                                                                            else:
                                                                                    if features[0] <= 0.237302:
                                                                                            if features[84] <= 50.201420:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                            else:
                                                                                                        return 6 # Leaf node, pred=6
                                                                                        
                                                                                    else:
                                                                                            if features[62] <= 0.122070:
                                                                                                    if features[75] <= 0.972556:
                                                                                                            if features[55] <= 0.924709:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                            else:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                        
                                                                                                    else:
                                                                                                                return 7 # Leaf node, pred=7
                                                                                                
                                                                                            else:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                        
                                                                                
                                                                        
                                                                
                                                        
                                                
                                        
                                
                            else:
                                    if features[3] <= 0.568787:
                                            if features[2] <= 0.103210:
                                                    if features[40] <= -0.013495:
                                                            if features[110] <= 31.938300:
                                                                    if features[73] <= 7.446291:
                                                                            if features[58] <= 0.155705:
                                                                                    if features[56] <= 0.419861:
                                                                                            if features[13] <= 0.084717:
                                                                                                        return 6 # Leaf node, pred=6
                                                                                            else:
                                                                                                    if features[124] <= -31.890877:
                                                                                                                return 7 # Leaf node, pred=7
                                                                                                    else:
                                                                                                                return 7 # Leaf node, pred=7
                                                                                                
                                                                                        
                                                                                    else:
                                                                                                return 6 # Leaf node, pred=6
                                                                                
                                                                            else:
                                                                                    if features[43] <= -0.064148:
                                                                                            if features[100] <= 14.511110:
                                                                                                    if features[124] <= 10.559084:
                                                                                                            if features[7] <= 2.569051:
                                                                                                                        return 6 # Leaf node, pred=6
                                                                                                            else:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                        
                                                                                                    else:
                                                                                                                return 7 # Leaf node, pred=7
                                                                                                
                                                                                            else:
                                                                                                    if features[89] <= 2.169677:
                                                                                                                return 6 # Leaf node, pred=6
                                                                                                    else:
                                                                                                                return 6 # Leaf node, pred=6
                                                                                                
                                                                                        
                                                                                    else:
                                                                                            if features[102] <= -40.069580:
                                                                                                        return 2 # Leaf node, pred=2
                                                                                            else:
                                                                                                    if features[15] <= 0.847483:
                                                                                                                return 6 # Leaf node, pred=6
                                                                                                    else:
                                                                                                                return 6 # Leaf node, pred=6
                                                                                                
                                                                                        
                                                                                
                                                                        
                                                                    else:
                                                                            if features[28] <= 16.005305:
                                                                                    if features[84] <= 57.739273:
                                                                                                return 7 # Leaf node, pred=7
                                                                                    else:
                                                                                                return 6 # Leaf node, pred=6
                                                                                
                                                                            else:
                                                                                    if features[38] <= 0.106801:
                                                                                                return 6 # Leaf node, pred=6
                                                                                    else:
                                                                                            if features[102] <= -21.759033:
                                                                                                        return 6 # Leaf node, pred=6
                                                                                            else:
                                                                                                    if features[70] <= 21.747787:
                                                                                                            if features[15] <= 0.929362:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                            else:
                                                                                                                        return 6 # Leaf node, pred=6
                                                                                                        
                                                                                                    else:
                                                                                                                return 6 # Leaf node, pred=6
                                                                                                
                                                                                        
                                                                                
                                                                        
                                                                
                                                            else:
                                                                    if features[23] <= -0.631225:
                                                                            if features[0] <= 0.198837:
                                                                                    if features[123] <= 23.651131:
                                                                                            if features[13] <= 0.164185:
                                                                                                        return 6 # Leaf node, pred=6
                                                                                            else:
                                                                                                    if features[15] <= 0.912526:
                                                                                                                return 6 # Leaf node, pred=6
                                                                                                    else:
                                                                                                                return 6 # Leaf node, pred=6
                                                                                                
                                                                                        
                                                                                    else:
                                                                                            if features[42] <= -0.291870:
                                                                                                        return 3 # Leaf node, pred=3
                                                                                            else:
                                                                                                        return 6 # Leaf node, pred=6
                                                                                        
                                                                                
                                                                            else:
                                                                                    if features[28] <= 23.277911:
                                                                                            if features[35] <= 0.942699:
                                                                                                        return 2 # Leaf node, pred=2
                                                                                            else:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                        
                                                                                    else:
                                                                                            if features[119] <= 4.793021:
                                                                                                        return 6 # Leaf node, pred=6
                                                                                            else:
                                                                                                    if features[120] <= 0.219544:
                                                                                                                return 7 # Leaf node, pred=7
                                                                                                    else:
                                                                                                                return 3 # Leaf node, pred=3
                                                                                                
                                                                                        
                                                                                
                                                                        
                                                                    else:
                                                                            if features[73] <= -17.105103:
                                                                                        return 6 # Leaf node, pred=6
                                                                            else:
                                                                                    if features[60] <= -5.580140:
                                                                                                return 3 # Leaf node, pred=3
                                                                                    else:
                                                                                                return 3 # Leaf node, pred=3
                                                                                
                                                                        
                                                                
                                                        
                                                    else:
                                                            if features[125] <= 37.750244:
                                                                    if features[80] <= -31.419378:
                                                                                return 6 # Leaf node, pred=6
                                                                    else:
                                                                                return 8 # Leaf node, pred=8
                                                                
                                                            else:
                                                                    if features[10] <= 0.165724:
                                                                                return 3 # Leaf node, pred=3
                                                                    else:
                                                                                return 6 # Leaf node, pred=6
                                                                
                                                        
                                                
                                            else:
                                                    if features[108] <= 15757.097168:
                                                            if features[60] <= 17.837527:
                                                                    if features[120] <= 0.336975:
                                                                            if features[40] <= -0.134811:
                                                                                    if features[43] <= -0.115357:
                                                                                            if features[48] <= 3.952793:
                                                                                                    if features[19] <= 0.021248:
                                                                                                            if features[118] <= 0.229120:
                                                                                                                    if features[118] <= 0.180235:
                                                                                                                                return 7 # Leaf node, pred=7
                                                                                                                    else:
                                                                                                                                return 7 # Leaf node, pred=7
                                                                                                                
                                                                                                            else:
                                                                                                                    if features[16] <= 0.114868:
                                                                                                                                return 7 # Leaf node, pred=7
                                                                                                                    else:
                                                                                                                                return 7 # Leaf node, pred=7
                                                                                                                
                                                                                                        
                                                                                                    else:
                                                                                                            if features[124] <= 1.647949:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                            else:
                                                                                                                    if features[30] <= 1.045056:
                                                                                                                            if features[98] <= 0.793332:
                                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                                            else:
                                                                                                                                    if features[35] <= 0.944179:
                                                                                                                                            if features[108] <= 3154.828369:
                                                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                                                            else:
                                                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                                                        
                                                                                                                                    else:
                                                                                                                                            if features[23] <= -0.748291:
                                                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                                                            else:
                                                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                                                        
                                                                                                                                
                                                                                                                        
                                                                                                                    else:
                                                                                                                                return 7 # Leaf node, pred=7
                                                                                                                
                                                                                                        
                                                                                                
                                                                                            else:
                                                                                                    if features[102] <= -14.587404:
                                                                                                                return 6 # Leaf node, pred=6
                                                                                                    else:
                                                                                                                return 7 # Leaf node, pred=7
                                                                                                
                                                                                        
                                                                                    else:
                                                                                            if features[122] <= -0.164795:
                                                                                                    if features[39] <= 0.055176:
                                                                                                            if features[93] <= 11.337283:
                                                                                                                        return 6 # Leaf node, pred=6
                                                                                                            else:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                        
                                                                                                    else:
                                                                                                            if features[30] <= 1.092361:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                            else:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                        
                                                                                                
                                                                                            else:
                                                                                                    if features[12] <= 0.045061:
                                                                                                            if features[55] <= 0.890920:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                            else:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                        
                                                                                                    else:
                                                                                                            if features[33] <= -0.955994:
                                                                                                                    if features[64] <= 36.193850:
                                                                                                                                return 7 # Leaf node, pred=7
                                                                                                                    else:
                                                                                                                                return 7 # Leaf node, pred=7
                                                                                                                
                                                                                                            else:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                        
                                                                                                
                                                                                        
                                                                                
                                                                            else:
                                                                                    if features[93] <= -9.582520:
                                                                                            if features[124] <= -11.138918:
                                                                                                        return 6 # Leaf node, pred=6
                                                                                            else:
                                                                                                    if features[33] <= -0.895020:
                                                                                                                return 6 # Leaf node, pred=6
                                                                                                    else:
                                                                                                                return 2 # Leaf node, pred=2
                                                                                                
                                                                                        
                                                                                    else:
                                                                                            if features[82] <= -18.737793:
                                                                                                    if features[10] <= 0.256786:
                                                                                                            if features[87] <= 1.781706:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                            else:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                        
                                                                                                    else:
                                                                                                            if features[108] <= 7528.520752:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                            else:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                        
                                                                                                
                                                                                            else:
                                                                                                    if features[122] <= -0.068542:
                                                                                                                return 7 # Leaf node, pred=7
                                                                                                    else:
                                                                                                                return 7 # Leaf node, pred=7
                                                                                                
                                                                                        
                                                                                
                                                                        
                                                                    else:
                                                                            if features[33] <= -0.804840:
                                                                                    if features[121] <= -0.797241:
                                                                                            if features[43] <= -0.078125:
                                                                                                    if features[3] <= 0.517028:
                                                                                                            if features[47] <= 1.541671:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                            else:
                                                                                                                    if features[102] <= -22.430424:
                                                                                                                                return 7 # Leaf node, pred=7
                                                                                                                    else:
                                                                                                                                return 7 # Leaf node, pred=7
                                                                                                                
                                                                                                        
                                                                                                    else:
                                                                                                            if features[73] <= 5.706788:
                                                                                                                    if features[116] <= 54.290771:
                                                                                                                                return 7 # Leaf node, pred=7
                                                                                                                    else:
                                                                                                                                return 7 # Leaf node, pred=7
                                                                                                                
                                                                                                            else:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                        
                                                                                                
                                                                                            else:
                                                                                                    if features[125] <= 18.493652:
                                                                                                            if features[124] <= -3.051757:
                                                                                                                        return 6 # Leaf node, pred=6
                                                                                                            else:
                                                                                                                        return 8 # Leaf node, pred=8
                                                                                                        
                                                                                                    else:
                                                                                                            if features[27] <= 1.713430:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                            else:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                        
                                                                                                
                                                                                        
                                                                                    else:
                                                                                            if features[13] <= 0.378143:
                                                                                                        return 2 # Leaf node, pred=2
                                                                                            else:
                                                                                                    if features[1] <= 0.039318:
                                                                                                                return 7 # Leaf node, pred=7
                                                                                                    else:
                                                                                                                return 8 # Leaf node, pred=8
                                                                                                
                                                                                        
                                                                                
                                                                            else:
                                                                                    if features[41] <= 0.047126:
                                                                                            if features[15] <= 0.882479:
                                                                                                    if features[98] <= 1.301631:
                                                                                                                return 2 # Leaf node, pred=2
                                                                                                    else:
                                                                                                                return 2 # Leaf node, pred=2
                                                                                                
                                                                                            else:
                                                                                                    if features[23] <= -0.672302:
                                                                                                                return 7 # Leaf node, pred=7
                                                                                                    else:
                                                                                                                return 7 # Leaf node, pred=7
                                                                                                
                                                                                        
                                                                                    else:
                                                                                            if features[76] <= 45.471205:
                                                                                                        return 2 # Leaf node, pred=2
                                                                                            else:
                                                                                                        return 2 # Leaf node, pred=2
                                                                                        
                                                                                
                                                                        
                                                                
                                                            else:
                                                                    if features[30] <= 0.954494:
                                                                            if features[115] <= 0.982666:
                                                                                    if features[16] <= 0.374451:
                                                                                                return 7 # Leaf node, pred=7
                                                                                    else:
                                                                                                return 8 # Leaf node, pred=8
                                                                                
                                                                            else:
                                                                                        return 6 # Leaf node, pred=6
                                                                        
                                                                    else:
                                                                            if features[36] <= 1.066040:
                                                                                    if features[124] <= -9.552004:
                                                                                                return 6 # Leaf node, pred=6
                                                                                    else:
                                                                                                return 6 # Leaf node, pred=6
                                                                                
                                                                            else:
                                                                                        return 7 # Leaf node, pred=7
                                                                        
                                                                
                                                        
                                                    else:
                                                            if features[93] <= -19.912722:
                                                                    if features[73] <= -1.220703:
                                                                            if features[3] <= 0.447205:
                                                                                    if features[33] <= -0.820251:
                                                                                            if features[59] <= 0.016444:
                                                                                                        return 6 # Leaf node, pred=6
                                                                                            else:
                                                                                                        return 2 # Leaf node, pred=2
                                                                                        
                                                                                    else:
                                                                                                return 2 # Leaf node, pred=2
                                                                                
                                                                            else:
                                                                                    if features[110] <= 33.950676:
                                                                                                return 2 # Leaf node, pred=2
                                                                                    else:
                                                                                                return 2 # Leaf node, pred=2
                                                                                
                                                                        
                                                                    else:
                                                                            if features[43] <= -0.147095:
                                                                                        return 6 # Leaf node, pred=6
                                                                            else:
                                                                                    if features[121] <= -0.740479:
                                                                                                return 6 # Leaf node, pred=6
                                                                                    else:
                                                                                                return 6 # Leaf node, pred=6
                                                                                
                                                                        
                                                                
                                                            else:
                                                                    if features[30] <= 1.086501:
                                                                            if features[79] <= 2.087264:
                                                                                    if features[90] <= 28.988933:
                                                                                            if features[78] <= 1.234960:
                                                                                                        return 6 # Leaf node, pred=6
                                                                                            else:
                                                                                                        return 2 # Leaf node, pred=2
                                                                                        
                                                                                    else:
                                                                                                return 7 # Leaf node, pred=7
                                                                                
                                                                            else:
                                                                                    if features[80] <= 51.000986:
                                                                                            if features[23] <= -0.811219:
                                                                                                    if features[40] <= -0.216788:
                                                                                                            if features[108] <= 26501.598633:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                            else:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                        
                                                                                                    else:
                                                                                                            if features[115] <= 0.954940:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                            else:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                        
                                                                                                
                                                                                            else:
                                                                                                    if features[98] <= 0.573754:
                                                                                                            if features[26] <= -0.550229:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                            else:
                                                                                                                    if features[45] <= 0.001808:
                                                                                                                                return 2 # Leaf node, pred=2
                                                                                                                    else:
                                                                                                                                return 2 # Leaf node, pred=2
                                                                                                                
                                                                                                        
                                                                                                    else:
                                                                                                            if features[23] <= -0.581909:
                                                                                                                    if features[120] <= 0.228760:
                                                                                                                            if features[106] <= 0.775631:
                                                                                                                                    if features[50] <= 0.244263:
                                                                                                                                                return 2 # Leaf node, pred=2
                                                                                                                                    else:
                                                                                                                                                return 2 # Leaf node, pred=2
                                                                                                                                
                                                                                                                            else:
                                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                                        
                                                                                                                    else:
                                                                                                                            if features[54] <= 0.218765:
                                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                                            else:
                                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                                        
                                                                                                                
                                                                                                            else:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                        
                                                                                                
                                                                                        
                                                                                    else:
                                                                                            if features[67] <= 1.871027:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                            else:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                        
                                                                                
                                                                        
                                                                    else:
                                                                            if features[103] <= 4.577637:
                                                                                        return 6 # Leaf node, pred=6
                                                                            else:
                                                                                    if features[125] <= 7.965088:
                                                                                                return 7 # Leaf node, pred=7
                                                                                    else:
                                                                                                return 3 # Leaf node, pred=3
                                                                                
                                                                        
                                                                
                                                        
                                                
                                        
                                    else:
                                            if features[23] <= -0.604859:
                                                    if features[59] <= 0.044610:
                                                            if features[70] <= 33.608097:
                                                                    if features[3] <= 0.851196:
                                                                            if features[93] <= 29.617313:
                                                                                    if features[48] <= 3.503751:
                                                                                            if features[43] <= -0.178345:
                                                                                                    if features[73] <= -2.288819:
                                                                                                            if features[125] <= -10.345461:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                            else:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                        
                                                                                                    else:
                                                                                                            if features[23] <= -0.789429:
                                                                                                                        return 7 # Leaf node, pred=7
                                                                                                            else:
                                                                                                                    if features[93] <= 18.402100:
                                                                                                                                return 2 # Leaf node, pred=2
                                                                                                                    else:
                                                                                                                            if features[16] <= 0.646362:
                                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                                            else:
                                                                                                                                        return 3 # Leaf node, pred=3
                                                                                                                        
                                                                                                                
                                                                                                        
                                                                                                
                                                                                            else:
                                                                                                    if features[78] <= 1.846605:
                                                                                                            if features[32] <= 0.110891:
                                                                                                                    if features[98] <= 1.460433:
                                                                                                                                return 2 # Leaf node, pred=2
                                                                                                                    else:
                                                                                                                                return 2 # Leaf node, pred=2
                                                                                                                
                                                                                                            else:
                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                        
                                                                                                    else:
                                                                                                            if features[30] <= 1.102074:
                                                                                                                    if features[66] <= 0.697281:
                                                                                                                                return 2 # Leaf node, pred=2
                                                                                                                    else:
                                                                                                                            if features[96] <= 145.782478:
                                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                                            else:
                                                                                                                                        return 2 # Leaf node, pred=2
                                                                                                                        
                                                                                                                
                                                                                                            else:
                                                                                                                        return 3 # Leaf node, pred=3
                                                                                                        
                                                                                                
                                                                                        
                                                                                    else:
                                                                                                return 7 # Leaf node, pred=7
                                                                                
                                                                            else:
                                                                                    if features[20] <= -0.853510:
                                                                                            if features[90] <= 44.269550:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                            else:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                        
                                                                                    else:
                                                                                            if features[23] <= -0.625610:
                                                                                                    if features[70] <= 19.006535:
                                                                                                                return 2 # Leaf node, pred=2
                                                                                                    else:
                                                                                                                return 2 # Leaf node, pred=2
                                                                                                
                                                                                            else:
                                                                                                    if features[25] <= 0.016015:
                                                                                                                return 3 # Leaf node, pred=3
                                                                                                    else:
                                                                                                                return 3 # Leaf node, pred=3
                                                                                                
                                                                                        
                                                                                
                                                                        
                                                                    else:
                                                                            if features[53] <= -0.367462:
                                                                                        return 3 # Leaf node, pred=3
                                                                            else:
                                                                                    if features[62] <= -15.350346:
                                                                                                return 3 # Leaf node, pred=3
                                                                                    else:
                                                                                                return 2 # Leaf node, pred=2
                                                                                
                                                                        
                                                                
                                                            else:
                                                                    if features[23] <= -0.750549:
                                                                                return 6 # Leaf node, pred=6
                                                                    else:
                                                                                return 8 # Leaf node, pred=8
                                                                
                                                        
                                                    else:
                                                            if features[115] <= 0.936464:
                                                                    if features[32] <= 0.213491:
                                                                                return 8 # Leaf node, pred=8
                                                                    else:
                                                                                return 2 # Leaf node, pred=2
                                                                
                                                            else:
                                                                    if features[0] <= 0.572806:
                                                                            if features[125] <= 9.796146:
                                                                                        return 2 # Leaf node, pred=2
                                                                            else:
                                                                                        return 3 # Leaf node, pred=3
                                                                        
                                                                    else:
                                                                                return 3 # Leaf node, pred=3
                                                                
                                                        
                                                
                                            else:
                                                    if features[56] <= 1.544678:
                                                            if features[68] <= 28811.059570:
                                                                    if features[3] <= 0.786316:
                                                                            if features[100] <= 15.057376:
                                                                                    if features[2] <= 0.237732:
                                                                                                return 3 # Leaf node, pred=3
                                                                                    else:
                                                                                            if features[107] <= 1.957194:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                            else:
                                                                                                        return 2 # Leaf node, pred=2
                                                                                        
                                                                                
                                                                            else:
                                                                                    if features[83] <= 76.080322:
                                                                                                return 3 # Leaf node, pred=3
                                                                                    else:
                                                                                                return 3 # Leaf node, pred=3
                                                                                
                                                                        
                                                                    else:
                                                                                return 3 # Leaf node, pred=3
                                                                
                                                            else:
                                                                    if features[72] <= 21.687934:
                                                                                return 8 # Leaf node, pred=8
                                                                    else:
                                                                                return 8 # Leaf node, pred=8
                                                                
                                                        
                                                    else:
                                                            if features[100] <= 16.069033:
                                                                        return 5 # Leaf node, pred=5
                                                            else:
                                                                        return 5 # Leaf node, pred=5
                                                        
                                                
                                        
                                
                        
                    else:
                            if features[16] <= 0.579345:
                                    if features[125] <= 15.777592:
                                            if features[60] <= -14.352418:
                                                    if features[122] <= -0.052246:
                                                            if features[53] <= -0.141693:
                                                                        return 8 # Leaf node, pred=8
                                                            else:
                                                                        return 2 # Leaf node, pred=2
                                                        
                                                    else:
                                                            if features[4] <= 0.254577:
                                                                        return 6 # Leaf node, pred=6
                                                            else:
                                                                    if features[50] <= 0.055367:
                                                                                return 3 # Leaf node, pred=3
                                                                    else:
                                                                                return 8 # Leaf node, pred=8
                                                                
                                                        
                                                
                                            else:
                                                    if features[3] <= 0.468384:
                                                            if features[124] <= 29.052742:
                                                                        return 6 # Leaf node, pred=6
                                                            else:
                                                                        return 6 # Leaf node, pred=6
                                                        
                                                    else:
                                                            if features[113] <= -54.595963:
                                                                        return 6 # Leaf node, pred=6
                                                            else:
                                                                    if features[124] <= -39.520264:
                                                                                return 6 # Leaf node, pred=6
                                                                    else:
                                                                            if features[101] <= 24.054979:
                                                                                        return 2 # Leaf node, pred=2
                                                                            else:
                                                                                        return 2 # Leaf node, pred=2
                                                                        
                                                                
                                                        
                                                
                                        
                                    else:
                                            if features[123] <= -14.465336:
                                                    if features[93] <= 65.856937:
                                                                return 6 # Leaf node, pred=6
                                                    else:
                                                                return 6 # Leaf node, pred=6
                                                
                                            else:
                                                    if features[23] <= -0.768372:
                                                            if features[59] <= 0.016218:
                                                                        return 2 # Leaf node, pred=2
                                                            else:
                                                                        return 6 # Leaf node, pred=6
                                                        
                                                    else:
                                                            if features[13] <= 0.178040:
                                                                    if features[39] <= 0.045803:
                                                                                return 3 # Leaf node, pred=3
                                                                    else:
                                                                                return 3 # Leaf node, pred=3
                                                                
                                                            else:
                                                                    if features[80] <= 29.331977:
                                                                            if features[122] <= -0.144714:
                                                                                        return 2 # Leaf node, pred=2
                                                                            else:
                                                                                        return 6 # Leaf node, pred=6
                                                                        
                                                                    else:
                                                                            if features[81] <= 28.721744:
                                                                                        return 3 # Leaf node, pred=3
                                                                            else:
                                                                                        return 3 # Leaf node, pred=3
                                                                        
                                                                
                                                        
                                                
                                        
                                
                            else:
                                    if features[108] <= 86770.468750:
                                            if features[103] <= 1.098633:
                                                    if features[15] <= 0.911264:
                                                            if features[124] <= -54.229752:
                                                                        return 8 # Leaf node, pred=8
                                                            else:
                                                                        return 8 # Leaf node, pred=8
                                                        
                                                    else:
                                                            if features[2] <= 0.083985:
                                                                    if features[68] <= 7835.679688:
                                                                                return 6 # Leaf node, pred=6
                                                                    else:
                                                                                return 3 # Leaf node, pred=3
                                                                
                                                            else:
                                                                    if features[119] <= 5.836311:
                                                                                return 2 # Leaf node, pred=2
                                                                    else:
                                                                                return 2 # Leaf node, pred=2
                                                                
                                                        
                                                
                                            else:
                                                    if features[122] <= 0.079895:
                                                            if features[3] <= 0.404724:
                                                                    if features[36] <= 1.030519:
                                                                            if features[116] <= 163.391121:
                                                                                    if features[89] <= 2.182979:
                                                                                                return 6 # Leaf node, pred=6
                                                                                    else:
                                                                                                return 6 # Leaf node, pred=6
                                                                                
                                                                            else:
                                                                                        return 3 # Leaf node, pred=3
                                                                        
                                                                    else:
                                                                                return 3 # Leaf node, pred=3
                                                                
                                                            else:
                                                                    if features[32] <= 0.099159:
                                                                            if features[122] <= -0.110596:
                                                                                        return 2 # Leaf node, pred=2
                                                                            else:
                                                                                        return 8 # Leaf node, pred=8
                                                                        
                                                                    else:
                                                                            if features[5] <= 0.009773:
                                                                                    if features[63] <= 41.534424:
                                                                                                return 2 # Leaf node, pred=2
                                                                                    else:
                                                                                                return 3 # Leaf node, pred=3
                                                                                
                                                                            else:
                                                                                    if features[106] <= 0.512340:
                                                                                            if features[83] <= 18.859863:
                                                                                                    if features[46] <= -0.260319:
                                                                                                                return 3 # Leaf node, pred=3
                                                                                                    else:
                                                                                                                return 3 # Leaf node, pred=3
                                                                                                
                                                                                            else:
                                                                                                        return 3 # Leaf node, pred=3
                                                                                        
                                                                                    else:
                                                                                            if features[30] <= 0.911722:
                                                                                                        return 3 # Leaf node, pred=3
                                                                                            else:
                                                                                                    if features[54] <= 0.143723:
                                                                                                                return 3 # Leaf node, pred=3
                                                                                                    else:
                                                                                                                return 2 # Leaf node, pred=2
                                                                                                
                                                                                        
                                                                                
                                                                        
                                                                
                                                        
                                                    else:
                                                            if features[2] <= 0.112976:
                                                                        return 8 # Leaf node, pred=8
                                                            else:
                                                                        return 3 # Leaf node, pred=3
                                                        
                                                
                                        
                                    else:
                                            if features[43] <= 0.224670:
                                                    if features[21] <= 0.164290:
                                                            if features[125] <= -63.476570:
                                                                    if features[76] <= 93.566891:
                                                                                return 6 # Leaf node, pred=6
                                                                    else:
                                                                                return 6 # Leaf node, pred=6
                                                                
                                                            else:
                                                                    if features[15] <= 0.930481:
                                                                            if features[41] <= 0.087306:
                                                                                        return 6 # Leaf node, pred=6
                                                                            else:
                                                                                        return 3 # Leaf node, pred=3
                                                                        
                                                                    else:
                                                                                return 3 # Leaf node, pred=3
                                                                
                                                        
                                                    else:
                                                            if features[73] <= 55.877701:
                                                                    if features[110] <= 78.578739:
                                                                            if features[120] <= 0.262451:
                                                                                    if features[23] <= -0.798584:
                                                                                                return 6 # Leaf node, pred=6
                                                                                    else:
                                                                                            if features[104] <= 79.895042:
                                                                                                        return 3 # Leaf node, pred=3
                                                                                            else:
                                                                                                        return 3 # Leaf node, pred=3
                                                                                        
                                                                                
                                                                            else:
                                                                                        return 3 # Leaf node, pred=3
                                                                        
                                                                    else:
                                                                                return 3 # Leaf node, pred=3
                                                                
                                                            else:
                                                                        return 3 # Leaf node, pred=3
                                                        
                                                
                                            else:
                                                    if features[14] <= 0.258499:
                                                                return 6 # Leaf node, pred=6
                                                    else:
                                                            if features[16] <= 3.975342:
                                                                        return 3 # Leaf node, pred=3
                                                            else:
                                                                        return 4 # Leaf node, pred=4
                                                        
                                                
                                        
                                
                        
                
            else:
                    if features[36] <= 0.933165:
                            if features[20] <= 0.109250:
                                    if features[30] <= 0.232148:
                                            if features[50] <= 0.586801:
                                                    if features[122] <= -0.208313:
                                                                return 10 # Leaf node, pred=10
                                                    else:
                                                            if features[59] <= 0.070698:
                                                                        return 3 # Leaf node, pred=3
                                                            else:
                                                                        return 6 # Leaf node, pred=6
                                                        
                                                
                                            else:
                                                    if features[50] <= 0.747221:
                                                            if features[110] <= 27.670835:
                                                                    if features[43] <= -0.625244:
                                                                            if features[2] <= 0.593445:
                                                                                        return 1 # Leaf node, pred=1
                                                                            else:
                                                                                        return 1 # Leaf node, pred=1
                                                                        
                                                                    else:
                                                                                return 6 # Leaf node, pred=6
                                                                
                                                            else:
                                                                        return 11 # Leaf node, pred=11
                                                        
                                                    else:
                                                            if features[13] <= 0.194458:
                                                                    if features[50] <= 0.931892:
                                                                                return 8 # Leaf node, pred=8
                                                                    else:
                                                                            if features[116] <= 67.260746:
                                                                                        return 11 # Leaf node, pred=11
                                                                            else:
                                                                                        return 10 # Leaf node, pred=10
                                                                        
                                                                
                                                            else:
                                                                    if features[41] <= 0.088311:
                                                                            if features[13] <= 0.597625:
                                                                                        return 11 # Leaf node, pred=11
                                                                            else:
                                                                                    if features[30] <= 0.056042:
                                                                                                return 6 # Leaf node, pred=6
                                                                                    else:
                                                                                                return 11 # Leaf node, pred=11
                                                                                
                                                                        
                                                                    else:
                                                                            if features[123] <= -3.326416:
                                                                                        return 10 # Leaf node, pred=10
                                                                            else:
                                                                                        return 11 # Leaf node, pred=11
                                                                        
                                                                
                                                        
                                                
                                        
                                    else:
                                            if features[48] <= 4.523716:
                                                    if features[10] <= 0.519649:
                                                            if features[123] <= 9.735107:
                                                                        return 7 # Leaf node, pred=7
                                                            else:
                                                                    if features[42] <= -0.345764:
                                                                                return 6 # Leaf node, pred=6
                                                                    else:
                                                                                return 7 # Leaf node, pred=7
                                                                
                                                        
                                                    else:
                                                            if features[42] <= -0.311035:
                                                                    if features[36] <= 0.610351:
                                                                            if features[89] <= 2.210791:
                                                                                        return 8 # Leaf node, pred=8
                                                                            else:
                                                                                        return 8 # Leaf node, pred=8
                                                                        
                                                                    else:
                                                                            if features[70] <= 44.306181:
                                                                                    if features[15] <= 0.882625:
                                                                                                return 5 # Leaf node, pred=5
                                                                                    else:
                                                                                                return 3 # Leaf node, pred=3
                                                                                
                                                                            else:
                                                                                        return 8 # Leaf node, pred=8
                                                                        
                                                                
                                                            else:
                                                                    if features[98] <= 1.107301:
                                                                                return 3 # Leaf node, pred=3
                                                                    else:
                                                                                return 4 # Leaf node, pred=4
                                                                
                                                        
                                                
                                            else:
                                                    if features[108] <= 134.639473:
                                                            if features[2] <= 0.220031:
                                                                        return 8 # Leaf node, pred=8
                                                            else:
                                                                    if features[3] <= 0.374939:
                                                                                return 0 # Leaf node, pred=0
                                                                    else:
                                                                                return 8 # Leaf node, pred=8
                                                                
                                                        
                                                    else:
                                                            if features[102] <= 10.070801:
                                                                    if features[84] <= 109.954842:
                                                                            if features[61] <= 5.229218:
                                                                                    if features[33] <= -0.511322:
                                                                                            if features[85] <= 35.343088:
                                                                                                        return 7 # Leaf node, pred=7
                                                                                            else:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                        
                                                                                    else:
                                                                                            if features[103] <= 17.944338:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                            else:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                        
                                                                                
                                                                            else:
                                                                                    if features[40] <= -0.928357:
                                                                                                return 8 # Leaf node, pred=8
                                                                                    else:
                                                                                            if features[113] <= 16.616822:
                                                                                                        return 8 # Leaf node, pred=8
                                                                                            else:
                                                                                                    if features[26] <= -0.461240:
                                                                                                                return 8 # Leaf node, pred=8
                                                                                                    else:
                                                                                                                return 8 # Leaf node, pred=8
                                                                                                
                                                                                        
                                                                                
                                                                        
                                                                    else:
                                                                            if features[125] <= 1.770020:
                                                                                    if features[42] <= -0.842163:
                                                                                                return 8 # Leaf node, pred=8
                                                                                    else:
                                                                                                return 6 # Leaf node, pred=6
                                                                                
                                                                            else:
                                                                                        return 8 # Leaf node, pred=8
                                                                        
                                                                
                                                            else:
                                                                    if features[48] <= 8.964044:
                                                                                return 7 # Leaf node, pred=7
                                                                    else:
                                                                                return 7 # Leaf node, pred=7
                                                                
                                                        
                                                
                                        
                                
                            else:
                                    if features[22] <= 0.341126:
                                            if features[108] <= 21742.933594:
                                                    if features[70] <= 25.825427:
                                                            if features[116] <= 8.117676:
                                                                        return 1 # Leaf node, pred=1
                                                            else:
                                                                    if features[26] <= -1.533708:
                                                                            if features[98] <= 1.591673:
                                                                                        return 10 # Leaf node, pred=10
                                                                            else:
                                                                                    if features[53] <= -0.672424:
                                                                                                return 10 # Leaf node, pred=10
                                                                                    else:
                                                                                                return 9 # Leaf node, pred=9
                                                                                
                                                                        
                                                                    else:
                                                                            if features[62] <= 8.789062:
                                                                                    if features[20] <= 0.115469:
                                                                                            if features[94] <= 6.935122:
                                                                                                        return 10 # Leaf node, pred=10
                                                                                            else:
                                                                                                        return 10 # Leaf node, pred=10
                                                                                        
                                                                                    else:
                                                                                            if features[67] <= 1.601161:
                                                                                                    if features[28] <= 0.713194:
                                                                                                            if features[59] <= 0.018226:
                                                                                                                        return 10 # Leaf node, pred=10
                                                                                                            else:
                                                                                                                        return 1 # Leaf node, pred=1
                                                                                                        
                                                                                                    else:
                                                                                                                return 10 # Leaf node, pred=10
                                                                                                
                                                                                            else:
                                                                                                        return 10 # Leaf node, pred=10
                                                                                        
                                                                                
                                                                            else:
                                                                                    if features[103] <= 16.418459:
                                                                                                return 10 # Leaf node, pred=10
                                                                                    else:
                                                                                                return 6 # Leaf node, pred=6
                                                                                
                                                                        
                                                                
                                                        
                                                    else:
                                                            if features[113] <= 1.174927:
                                                                    if features[96] <= 103.698730:
                                                                                return 11 # Leaf node, pred=11
                                                                    else:
                                                                                return 6 # Leaf node, pred=6
                                                                
                                                            else:
                                                                    if features[83] <= 18.005377:
                                                                                return 10 # Leaf node, pred=10
                                                                    else:
                                                                                return 10 # Leaf node, pred=10
                                                                
                                                        
                                                
                                            else:
                                                    if features[23] <= 0.351929:
                                                            if features[118] <= 0.455576:
                                                                    if features[110] <= 41.774212:
                                                                                return 11 # Leaf node, pred=11
                                                                    else:
                                                                                return 11 # Leaf node, pred=11
                                                                
                                                            else:
                                                                    if features[103] <= 68.450928:
                                                                                return 10 # Leaf node, pred=10
                                                                    else:
                                                                                return 10 # Leaf node, pred=10
                                                                
                                                        
                                                    else:
                                                            if features[3] <= 1.528382:
                                                                    if features[70] <= 54.142420:
                                                                            if features[102] <= 54.321304:
                                                                                        return 10 # Leaf node, pred=10
                                                                            else:
                                                                                        return 10 # Leaf node, pred=10
                                                                        
                                                                    else:
                                                                                return 10 # Leaf node, pred=10
                                                                
                                                            else:
                                                                        return 4 # Leaf node, pred=4
                                                        
                                                
                                        
                                    else:
                                            if features[110] <= 13.390912:
                                                    if features[105] <= 43.666697:
                                                                return 9 # Leaf node, pred=9
                                                    else:
                                                            if features[93] <= -5.676270:
                                                                        return 10 # Leaf node, pred=10
                                                            else:
                                                                        return 9 # Leaf node, pred=9
                                                        
                                                
                                            else:
                                                    if features[43] <= -0.083740:
                                                            if features[22] <= 0.351379:
                                                                        return 10 # Leaf node, pred=10
                                                            else:
                                                                        return 10 # Leaf node, pred=10
                                                        
                                                    else:
                                                                return 9 # Leaf node, pred=9
                                                
                                        
                                
                        
                    else:
                            if features[68] <= 40872.601562:
                                    if features[30] <= 0.515530:
                                            if features[22] <= -0.276489:
                                                    if features[3] <= 1.009705:
                                                            if features[43] <= -0.595459:
                                                                        return 8 # Leaf node, pred=8
                                                            else:
                                                                        return 8 # Leaf node, pred=8
                                                        
                                                    else:
                                                            if features[96] <= 249.816917:
                                                                        return 5 # Leaf node, pred=5
                                                            else:
                                                                        return 6 # Leaf node, pred=6
                                                        
                                                
                                            else:
                                                    if features[20] <= 0.082700:
                                                                return 11 # Leaf node, pred=11
                                                    else:
                                                            if features[68] <= 16695.586914:
                                                                        return 10 # Leaf node, pred=10
                                                            else:
                                                                        return 4 # Leaf node, pred=4
                                                        
                                                
                                        
                                    else:
                                            if features[55] <= 0.752206:
                                                        return 5 # Leaf node, pred=5
                                            else:
                                                    if features[98] <= 1.352478:
                                                            if features[99] <= 12.110197:
                                                                        return 3 # Leaf node, pred=3
                                                            else:
                                                                        return 3 # Leaf node, pred=3
                                                        
                                                    else:
                                                                return 6 # Leaf node, pred=6
                                                
                                        
                                
                            else:
                                    if features[10] <= 0.721022:
                                            if features[121] <= -0.215332:
                                                    if features[102] <= 4.241943:
                                                                return 8 # Leaf node, pred=8
                                                    else:
                                                                return 6 # Leaf node, pred=6
                                                
                                            else:
                                                    if features[7] <= 3.159316:
                                                                return 11 # Leaf node, pred=11
                                                    else:
                                                                return 11 # Leaf node, pred=11
                                                
                                        
                                    else:
                                            if features[45] <= 0.298608:
                                                        return 4 # Leaf node, pred=4
                                            else:
                                                        return 5 # Leaf node, pred=5
                                        
                                
                        
                
        


def calculate_skew_manual(x_list):
    # Population moments, as in the training code (calculate_skew_kurt_manual).
    n = len(x_list)
    if n == 0:
        return 0.0
    mean_x = sum(x_list) / n
    m2 = sum((xi - mean_x) ** 2 for xi in x_list) / n
    m3 = sum((xi - mean_x) ** 3 for xi in x_list) / n
    if m2 == 0:
        return 0.0
    return m3 / (m2 ** 1.5)

def calculate_kurt_manual(x_list):
    # Non-excess kurtosis m4 / m2^2 from population moments, as in training.
    n = len(x_list)
    if n == 0:
        return 0.0
    mean_x = sum(x_list) / n
    m2 = sum((xi - mean_x) ** 2 for xi in x_list) / n
    m4 = sum((xi - mean_x) ** 4 for xi in x_list) / n
    if m2 == 0:
        return 0.0
    return m4 / (m2 ** 2)

def calculate_entropy_manual(x_list, num_bins=5):
    # Same binning as np.histogram(x, bins=num_bins): edges from linspace,
    # last bin closed, with numpy's edge corrections.
    min_x = min(x_list)
    max_x = max(x_list)
    if min_x == max_x:
        return 0.0
    span = max_x - min_x
    step = span / num_bins
    edges = [k * step + min_x for k in range(num_bins)] + [max_x]
    histogram = [0] * num_bins
    for val in x_list:
        idx = int((val - min_x) / span * num_bins)
        if idx >= num_bins:
            idx = num_bins - 1
        if val < edges[idx]:
            idx -= 1
        elif idx < num_bins - 1 and val >= edges[idx + 1]:
            idx += 1
        histogram[idx] += 1
    total = len(x_list)
    probabilities = [h / total for h in histogram if h > 0]
    return -sum(p * math.log2(p) for p in probabilities)

def calculate_dominant_freq_fft(x_list, num_bins=5):
    n = len(x_list)
    if n == 0 or num_bins <= 0:
        return 0.0
    effective_num_bins = min(num_bins, n)
    bin_magnitudes = []
    for k in range(effective_num_bins):
        real_part = 0.0
        imag_part = 0.0
        for t in range(n):
            angle = -2.0 * math.pi * k * t / n
            cos_val = math.cos(angle)
            sin_val = math.sin(angle)
            real_part += x_list[t] * cos_val
            imag_part += x_list[t] * sin_val
        magnitude = math.sqrt(real_part**2 + imag_part**2)
        bin_magnitudes.append(magnitude)
    max_magnitude = bin_magnitudes[0]
    dominant_bin_index = 0
    for i in range(1, len(bin_magnitudes)):
        if bin_magnitudes[i] > max_magnitude:
            max_magnitude = bin_magnitudes[i]
            dominant_bin_index = i
    return float(dominant_bin_index)

def calculate_spectral_entropy_manual(x_list, num_bins=5):
    n = len(x_list)
    if n == 0 or num_bins <= 0:
        return 0.0
    effective_num_bins = min(num_bins, n)
    bin_magnitudes = []
    for k in range(effective_num_bins):
        real_part = 0.0
        imag_part = 0.0
        for t in range(n):
            angle = -2.0 * math.pi * k * t / n
            cos_val = math.cos(angle)
            sin_val = math.sin(angle)
            real_part += x_list[t] * cos_val
            imag_part += x_list[t] * sin_val
        magnitude = math.sqrt(real_part**2 + imag_part**2)
        bin_magnitudes.append(magnitude)
    power_spectrum = [mag**2 for mag in bin_magnitudes]
    total_power = sum(power_spectrum)
    if total_power == 0.0:
        return 0.0
    probabilities = [power / total_power for power in power_spectrum]
    spectral_entropy = 0.0
    for p in probabilities:
        if p > 0.0:
            spectral_entropy -= p * math.log2(p)
    return spectral_entropy

def _sign(v):
    return 1 if v > 0 else (-1 if v < 0 else 0)

def calculate_zero_crossing_rate(x_list):
    # Changes of sign(x) with sign(0) = 0, like np.diff(np.sign(x)) != 0.
    if len(x_list) <= 1:
        return 0.0
    crossings = 0
    prev_sign = _sign(x_list[0])
    for val in x_list[1:]:
        curr_sign = _sign(val)
        if curr_sign != prev_sign:
            crossings += 1
        prev_sign = curr_sign
    return crossings / (len(x_list) - 1)

def calculate_autocorr_lag1(x_list):
    # Pearson correlation of x[:-1] and x[1:], like np.corrcoef(...)[0, 1].
    n = len(x_list)
    if n <= 2:
        return 0.0
    a = x_list[:-1]
    b = x_list[1:]
    mean_a = sum(a) / (n - 1)
    mean_b = sum(b) / (n - 1)
    s_ab = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(n - 1))
    s_aa = sum((v - mean_a) ** 2 for v in a)
    s_bb = sum((v - mean_b) ** 2 for v in b)
    if s_aa == 0 or s_bb == 0:
        return 0.0  # numpy gives nan for a constant window
    return s_ab / math.sqrt(s_aa * s_bb)

def _percentile_linear(sorted_x, q):
    # np.percentile's default 'linear' method on already sorted data.
    pos = q * (len(sorted_x) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(sorted_x) - 1)
    t = pos - lo
    a = sorted_x[lo]
    b = sorted_x[hi]
    if t >= 0.5:
        return b - (b - a) * (1 - t)
    return a + (b - a) * t

def extract_features_from_channel_manual(x_list):
    features = []
    n = len(x_list)
    mean_x = sum(x_list) / n
    std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x_list) / (n - 1)) if n > 1 else 0.0
    min_x = min(x_list)
    max_x = max(x_list)
    range_x = max_x - min_x
    var_x = sum((xi - mean_x)**2 for xi in x_list) / (n - 1) if n > 1 else 0.0
    features.extend([mean_x, std_x, min_x, max_x, range_x, var_x])

    skew_x = calculate_skew_manual(x_list)
    kurt_x = calculate_kurt_manual(x_list)
    energy_x = sum(xi**2 for xi in x_list)
    entropy_x = calculate_entropy_manual(x_list, num_bins=5)
    features.extend([skew_x, kurt_x, energy_x, entropy_x])

    rms_x = math.sqrt(sum(xi**2 for xi in x_list) / n)
    zcr_x = calculate_zero_crossing_rate(x_list)
    mad_x = sum(abs(xi - mean_x) for xi in x_list) / n
    sorted_x = sorted(x_list)
    median_x = sorted_x[n // 2] if n % 2 == 1 else (sorted_x[n // 2 - 1] + sorted_x[n // 2]) / 2
    iqr_x = _percentile_linear(sorted_x, 0.75) - _percentile_linear(sorted_x, 0.25)
    autocorr_x = calculate_autocorr_lag1(x_list)
    features.extend([rms_x, zcr_x, mad_x, median_x, iqr_x, autocorr_x])

    # population std of the first differences, like np.std(np.diff(x))
    jerk_diffs = [(x_list[i] - x_list[i-1]) for i in range(1, n)]
    if jerk_diffs:
        mean_jerk = sum(jerk_diffs) / len(jerk_diffs)
        std_jerk_x = math.sqrt(sum((d - mean_jerk) ** 2 for d in jerk_diffs) / len(jerk_diffs))
    else:
        std_jerk_x = 0.0
    wl_sum = 0.0
    for i in range(1, n):
        wl_sum += abs(x_list[i] - x_list[i-1])
    waveform_length_x = wl_sum
    dom_freq_x = calculate_dominant_freq_fft(x_list, num_bins=5)
    spec_ent_x = calculate_spectral_entropy_manual(x_list, num_bins=5)
    features.extend([waveform_length_x, dom_freq_x, spec_ent_x, std_jerk_x])
    return features

def extract_features_window_manual(window_data_list_of_lists):
    all_features = []
    for col_idx in range(6):
        channel_data = [window_data_list_of_lists[row_idx][col_idx] for row_idx in range(20)]
        channel_features = extract_features_from_channel_manual(channel_data)
        all_features.extend(channel_features)
    last_sample_raw = window_data_list_of_lists[-1]
    all_features.extend(last_sample_raw)
    return all_features

def majority_vote(prediction_history):
    """Return the most common prediction from recent history."""
    if len(prediction_history) == 0:
        return 0
    counts = {}
    for p in prediction_history:
        counts[p] = counts.get(p, 0) + 1
    return max(counts, key=counts.get)


ACTIVITY_MAP = {
    0: "sitting",
    1: "standing",
    2: "walking",
    3: "brisk_walking",
    4: "jogging",
    5: "cycling",
    6: "stair_up",
    7: "stair_down",
    8: "sit_stand_sit",
    9: "phone_interaction",
    10: "eating_with_spoon",
    11: "pick_and_place",
}

WINDOW_SIZE = 20
OVERLAP_FRAC = 0.5
STEP_SIZE = int(WINDOW_SIZE * (1 - OVERLAP_FRAC))

imu_buffer = []
prediction_history = []  # For majority voting

# --- Setup WiFi connection ---
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, KEY)

timeout = 10
while not wifi.isconnected() and timeout > 0:
    print('Trying to connect to "{:s}"...'.format(SSID))
    time.sleep_ms(1000)
    timeout -= 1
    red_led.toggle()
    time.sleep_ms(100)
    red_led.toggle()

if not wifi.isconnected():
    print('Failed to connect to Wi-Fi after timeout.')
    red_led.on()
    green_led.off()
    blue_led.off()
    while True:
        time.sleep_ms(1000)
else:
    print("WiFi Connected ", wifi.ifconfig())
    green_led.on()
    red_led.off()
    blue_led.off()
    time.sleep(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Nicla Vision: Multi-Class Activity Recognition Started")
print("Sending predictions to {}:{}".format(PC_IP, PORT))
print("Sampling at {} Hz, sending every {} ms".format(SAMPLE_RATE_HZ, SEND_INTERVAL_MS))

last_send_time = time.ticks_ms()
current_smoothed_prediction = 0
sample_count = 0

try:
    while True:
        loop_start = time.ticks_ms()

        # Read IMU data
        ax, ay, az = lsm.accel()
        gx, gy, gz = lsm.gyro()
        current_sample = [ax, ay, az, gx, gy, gz]
        imu_buffer.append(current_sample)
        sample_count += 1

        # Make prediction when we have enough samples
        if len(imu_buffer) >= WINDOW_SIZE:
            window_data = imu_buffer[-WINDOW_SIZE:]
            features_126 = extract_features_window_manual(window_data)
            raw_prediction = predict_activity_features(features_126)

            # Add to prediction history for smoothing
            prediction_history.append(raw_prediction)
            if len(prediction_history) > MAJORITY_VOTE_WINDOW:
                prediction_history.pop(0)

            # Get smoothed prediction via majority vote
            current_smoothed_prediction = majority_vote(prediction_history)

            # Slide the window
            if len(imu_buffer) > WINDOW_SIZE - STEP_SIZE:
                imu_buffer = imu_buffer[-(WINDOW_SIZE - STEP_SIZE):]

        # Send prediction at fixed interval (not every sample)
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, last_send_time) >= SEND_INTERVAL_MS:
            predicted_activity_str = ACTIVITY_MAP.get(current_smoothed_prediction, "unknown")

            # Update LEDs based on smoothed prediction
            red_led.off()
            green_led.off()
            blue_led.off()

            if current_smoothed_prediction in [0, 1]:  # sitting, standing
                green_led.on()
            elif current_smoothed_prediction in [2, 3, 4]:  # walking, brisk_walking, jogging
                red_led.on()
            else:
                blue_led.on()

            # Format and send prediction data
            ts_ms = time.ticks_ms()
            prediction_data = "{:d},{:d},{:s},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(
                ts_ms,
                current_smoothed_prediction,
                predicted_activity_str,
                ax, ay, az,
                gx, gy, gz
            )

            try:
                sock.sendto(prediction_data.encode(), (PC_IP, PORT))
            except Exception as e:
                print("UDP send error:", e)

            print(
                "Pred: {} ({:d}) | Samples: {} | "
                "Accel: x:{:>6.2f} y:{:>6.2f} z:{:>6.2f} "
                "Gyro: x:{:>6.2f} y:{:>6.2f} z:{:>6.2f}".format(
                    predicted_activity_str,
                    current_smoothed_prediction,
                    sample_count,
                    ax, ay, az,
                    gx, gy, gz
                )
            )

            last_send_time = current_time

        # Maintain sampling rate
        loop_end = time.ticks_ms()
        elapsed = time.ticks_diff(loop_end, loop_start)
        sleep_time = SAMPLE_INTERVAL_MS - elapsed
        if sleep_time > 0:
            time.sleep_ms(sleep_time)

except KeyboardInterrupt:
    red_led.off()
    green_led.off()
    blue_led.off()
    print("Activity Recognition Stopped. Total samples: {}".format(sample_count))

