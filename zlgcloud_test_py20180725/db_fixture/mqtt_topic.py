#coding=utf_8
#设备上线的主题，设备 --> 服务器
STR_TOPIC_ONLINE = "/d2s/%s/%s/online"

#设备下线的主题，设备 --> 服务器
STR_TOPIC_OFFLINE = "/d2s/%s/%s/offline"

#设备注册的主题，设备 --> 服务器
STR_TOPIC_REGISTER ="/d2s/%s/%s/register"

#设备上报数据的主题，设备 --> 服务器
STR_TOPIC_REPORT_DATA = "/d2s/%s/%s/data"

#设备上报透传数据的主题，设备 --> 服务器
STR_TOPIC_REPORT_RAW = "/d2s/%s/%s/raw"

#设备上报错误的主题，设备 --> 服务器
STR_TOPIC_REPORT_ERROR = "/d2s/%s/%s/error"

#设备上报状态的主题，设备 --> 服务器
STR_TOPIC_REPORT_STATUS = "/d2s/%s/%s/status"

#设备上报警告的主题，设备 --> 服务器
STR_TOPIC_REPORT_WARNING = "/d2s/%s/%s/warning"

#设备上报命令执行结果的主题，设备 --> 服务器
STR_TOPIC_REPORT_RESULT = "/d2s/%s/%s/result"

#服务器发送广播到所有的主题， 服务器 --> 设备
STR_TOPIC_BROADCAST  = "/s2d/b/all"
STR_TOPIC_BROADCAST_PREFIX ="/s2d/b/"

#服务器发送广播到指定类型的设备的主题， 服务器 --> 设备
STR_TOPIC_BROADCAST_DEVTYPE ="/s2d/b/%s"

#服务器发送消息到指定设备的主题， 服务器 --> 设备
STR_TOPIC_DEVICE  = "/s2d/d/%s/%s"
STR_TOPIC_DEVICE_PREFIX = "/s2d/d/"

QOS = 1