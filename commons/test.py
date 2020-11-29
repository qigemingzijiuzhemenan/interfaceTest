import os
import time
a='2020/11/21 8:00:00'
timeArray = time.strptime(a,"%Y/%m/%d %H:%M:%S")
timeStamp = int(time.mktime(timeArray))*1000
print(timeStamp)