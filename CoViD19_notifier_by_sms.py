import requests
from bs4 import BeautifulSoup as bsp
from collections import defaultdict as dfd
import time

OLD_DATA=dfd(str)
OLD_DATA={"Total Confirmed cases (Indian)":"3491 *","Total Confirmed cases (Foreign)":"41 *","Cured/Discharged":"24","Death":"7"}

def updateDATA(oldData,newData):
    oldData["Total Confirmed cases (Indian)"]=newData["Total Confirmed cases (Indian)"]
    oldData["Total Confirmed cases (Foreign)"]=newData["Total Confirmed cases (Foreign)"]
    oldData["Cured/Discharged"]=newData["Cured/Discharged"]
    oldData["Death"]=newData["Death"]



def sendSMS(msg):
    import requests
    #SMS service: https://www.fast2sms.com/
    url = "https://www.fast2sms.com/dev/bulk"
    #API_KEY="YOUR_API_KEY"
    API_KEY="60doIbMQSJGsW1275UZpxm8FHXw39eliVfucvP4KTNCqyahAtztLbrzVkeJZQDIpdNBO56cAoFPHT1i71" #its not correct key paste you KEY after signup fast2sms.com
    querystring = {"authorization":API_KEY,"sender_id":"FSTSMS","message":msg,"language":"english","route":"p","numbers":"8287798091,988998***"}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def compareData(oldData,newData):
    msg=".\n.**CoViD-19 updation (India) **\n\n"
    set1=set(oldData.values())
    set2=set(newData.values())
   
    if len(set1.union(set2))!=len(set2):
        newMSG="NEW DATA:"+generateSMS(newData)
        oldMSG="\n\n\nOLD DATA:"+generateSMS(oldData)
        updateDATA(oldData,newData)
        msg+=newMSG+oldMSG+"\n\nData from: https://www.mohfw.gov.in\nScript link: https://github.com/subahanii/CoViD19-notifier"
        print(msg)
        sendSMS(msg)

def generateSMS(data):
    msg=""
    
    msg+="\nTotal Confirmed cases (Indian):"+data["Total Confirmed cases (Indian)"]+"\nTotal Confirmed cases (Foreign): "+data["Total Confirmed cases (Foreign)"]+"\nCured/Discharged: "+data["Cured/Discharged"]+"\nDeath: "+data["Death"]
    return msg
    

while 1:
    URL = 'https://www.mohfw.gov.in/'
    page = requests.get(URL)

    soup = bsp(page.content, 'html.parser')
    data=[]
    for i in soup.find_all('tbody')[1].find_all('tr'):
        data.append(i.get_text().split("\n")[1::])

    sumData= data[-1]
    datafinal=dfd(list)

    for i in data:
        datafinal[i[0]].append(i[1])
        datafinal[i[0]].append(i[2])
        datafinal[i[0]].append(i[3])
        datafinal[i[0]].append(i[4])
        datafinal[i[0]].append(i[5])


    finalFilterData=[i  for i in sumData if i!=""]

    NEW_DATA=dfd(str)
    NEW_DATA={"Total Confirmed cases (Indian)":finalFilterData[1],"Total Confirmed cases (Foreign)":finalFilterData[2],"Cured/Discharged":finalFilterData[3],"Death":finalFilterData[4]}
    compareData(OLD_DATA,NEW_DATA)
    print("Data comming from www.mohfw.gov.in")
    time.sleep(10)



