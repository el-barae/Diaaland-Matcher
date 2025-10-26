import requests
import socket
import threading
import time

EUREKA_SERVER = "http://localhost:8761/eureka"
APP_NAME = "PYTHON-AI-SERVICE"
PORT = 8000

def get_host_ip():
    return socket.gethostbyname(socket.gethostname())

def register_with_eureka():
    instance_id = f"{get_host_ip()}:{APP_NAME}:{PORT}"
    data = f"""
    <instance>
        <instanceId>{get_host_ip()}:{APP_NAME}:{PORT}</instanceId>
        <hostName>{get_host_ip()}</hostName>
        <app>{APP_NAME}</app>
        <ipAddr>{get_host_ip()}</ipAddr>
        <status>UP</status>
        <port enabled="true">{PORT}</port>
        <vipAddress>{APP_NAME}</vipAddress>
        <secureVipAddress>{APP_NAME}</secureVipAddress>
        <dataCenterInfo class="com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo">
            <name>MyOwn</name>
        </dataCenterInfo>
    </instance>
    """

    headers = {'Content-Type': 'application/xml'}
    url = f"{EUREKA_SERVER}/apps/{APP_NAME}"
    response = requests.post(url, data=data.strip(), headers=headers)
    print("✅ Registered with Eureka:", response.status_code)
    print("✅ APP NAME:", APP_NAME)

    # Start heartbeat (renew registration every 30 seconds)
    def send_heartbeat():
        while True:
            time.sleep(30)
            renew_url = f"{EUREKA_SERVER}/apps/{APP_NAME}/{instance_id}"
            requests.put(renew_url, headers=headers)

    threading.Thread(target=send_heartbeat, daemon=True).start()
