import YanAPI

ip_adr = "192.168.0.160"
YanAPI.yan_api_init(ip_adr)
res = YanAPI.get_aprilTag_recognition_status()
print(res)
