#!/usr/bin/python3

from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.exceptions import PubNubException
from pubnub.pubnub import PubNub, SubscribeListener
import sys

pubconf = PNConfiguration()
pubconf.subscribe_key = 'sub-c-dbf66bda-16b9-11e8-8f67-36fe363f7ef0'
pubconf.publish_key = 'pub-c-14a6f403-3bab-4945-8656-7cba4ca4bb1f'
secret_key = "sec-c-Nzk1ZWE3OTItNjdkOS00ZDVlLThiZjAtODBmMWU2MjI2Y2Ji"
pubconf.ssl = False
pubnub = PubNub(pubconf)

# assign a channel
my_channel = 'pi-weather-station'

my_listener = SubscribeListener()
pubnub.add_listener(my_listener)

#
# pubnub.subscribe(my_channel)
# pubnub.start()

def disconnect_channel():
    pubnub.unsubscribe().channels(my_channel).execute()
    my_listener.wait_for_disconnect()
    print('unsubscribed')

if __name__ == "__main__":

    try:
        message = pubnub.subscribe().channels(my_channel).execute()
        my_listener.wait_for_connect()
    except Exception as e:
        print("ERROR: {}".format(e.message))
    print("##### {} #####".format(my_channel))
    while True:
        try:
            result = my_listener.wait_for_message_on(my_channel)
            data = result.message
            # print("{}".format(data).encode('utf-8'))
            dt = data["date_time"].encode("utf-8")
            t = float(data["temperature"].encode("utf-8"))
            p = round(float(data["pressure"].encode("utf-8")),5)
            print("sensor sent-time {}: Temperature {} F, Pressure {} bar".format(dt, t, p))
        except (IOError, TypeError) as e:
            # and since we got a type error
            # disconnect_channel()
            print(str(e))
        except KeyboardInterrupt as e:
            # since we're exiting the program
            print(str(e))
            disconnect_channel()
            sys.exit()

