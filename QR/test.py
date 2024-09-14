import YanAPI

ip_adr = "192.168.0.160"
YanAPI.yan_api_init(ip_adr)
# res = YanAPI.get_aprilTag_recognition_status()
res = YanAPI.start_aprilTag_recognition()
print(res)
