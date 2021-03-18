import MetaTrader5 as mt5
import simple_http_server.server as server

import data

print("Connecting to MofidTrader...")
data.get_config()
if not mt5.initialize(data.config["mofid_path"],
                      login=data.config["mofid_login"],
                      password=data.config["mofid_pass"],
                      server="MofidSecurities-Server"):
    print("Could not connect to MofidTrader!!")
    quit()
print("DONE!")

print("Connecting to MySQL...")
data.do_connect()
if not data.connect:
    print("Could not connect to MySQL!!")
    print(data.connect)
    quit()
print("DONE!")

data.init_analyzer()
data.init_watcher()

print("Initializing local server...")
try:
    import netifaces as ni
    my_ip = ni.ifaddresses(ni.gateways()['default'][ni.AF_INET][1])[ni.AF_INET][0]['addr']
except:
    my_ip = "192.168.1.8"  # 127.0.0.1

print("\nhttp://" + str(my_ip) + ":1399/\n")
try:
    server.scan("", r".*controller.*")
    server.start(host=my_ip, port=1399)
except Exception as e:
    if str(e) == "[WinError 10022] Windows Error 0x2726":
        print("ERROR STARTING SERVER: ", "آی پی بدست آمده مخصوص دستگاه شما نیست!")
    else:
        print("ERROR STARTING SERVER: ", e)
