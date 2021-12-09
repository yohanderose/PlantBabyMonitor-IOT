
import sys
import time
import RPi.GPIO as GPIO
import signal

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def signal_handler(sig, frame):

    print("Exiting ")
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
motor = 21
GPIO.setup(motor, GPIO.OUT)
activ = False

def waterer(self, params, packet):
    global activ
    print(packet.payload)

    activ = not activ
    print("Motor activity:", activ)
    if activ:
        GPIO.output(motor, 1)
    else:
        GPIO.output(motor, 0)



# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("yohan")

# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
# Configurations
# For TLS mutual authentication
myMQTTClient.configureEndpoint(
    "a3ektg1mpkm182-ats.iot.ap-southeast-2.amazonaws.com", 8883)

# For Websocket
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
# For TLS mutual authentication with TLS ALPN extension
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
myMQTTClient.configureCredentials(
    "/greengrass/certs/root-ca.pem", "/greengrass/certs/private.key", "/greengrass/certs/cert.pem")

# For Websocket, we only need to configure the root CA
# myMQTTClient.configureCredentials("YOUR/ROOT/CA/PATH")
# Infinite offline Publish queueing
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

print("Connecting, listening for calls...")
myMQTTClient.connect()
myMQTTClient.subscribe("home/waterer", 1, waterer)


while True:
    time.sleep(3) 

