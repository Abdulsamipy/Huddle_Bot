import requests
import json
import pandas as pd
from datetime import date   
import schedule 
import time 
from pandas.io.json import json_normalize
import datetime
import os 
import smtplib
from email.message import EmailMessage

api = ''
def get_last_name():
    url = f"https://api.telegram.org/{api}/getUpdates"
    re = requests.get(url)
    data = json.loads(re.text)
    d1 = data['result']
    d2 = len(d1)
    d3 = d1[int(d2-1)]
    d3 = str(d3)
    try:
        d4 = d3['message']['from']['first_name']
        d5 = d3['message']['text']
    except:
        d4 = "The message is a reply"
        d5 = "No log"

    if d4 == "The message is a reply":
        try:
            d4 = d3['edited_message']['from']['first_name']
            d5 = d3['edited_message']['text']
        except:
            d4 = str("The message is a reply")
            d5 - str("No log")

    return d4, d5



#check and update the attendence
def check_user():
    with open("temp_black.txt" , 'r') as t:
        ts = t.readlines()
        if len(ts) != 0:
            ts = ts[0]
            if x[0] == ts:
                
                print("No New User Found")
            else:
                with open("temp_black.txt" , 'w') as t:
                    t.write(x[0])

                #open Attendence File
                with open("Attendence.json", 'r+', encoding='utf') as f:
                    json_data = json.load(f)

                #Look for the user in list
                for j in json_data['employee']:
                    if x[0] == (j['name']):
                        num = int(j['Attendence']) + 1
                        j['Attendence']=j['Attendence'].replace(str(j['Attendence']), str(num))
                    
                        with open("Attendence.json", 'w', encoding='utf') as f:
                            json.dump(json_data, f, indent=2)
                        break


def send_mail(data, name):
    msg = EmailMessage()
    todays = date.today()
    msg['Subject'] = "Attendence - {}".format(todays.strftime("%d-%b-%Y"))
    msg['From'] = 'Huddle Bot'
    msg['To'] = ", "
    msg.set_content("Hey, The attendance for past two weeks is attached below :)")
    msg.add_attachment(data, maintype='application', subtype='csv', filename="{}".format(name))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  
        server.login("", "")
        server.send_message(msg)



#Reset Values every 1st and 15th
def reset():
    print("resetting")
    #open Attendence File
    with open("Attendence.json", 'r+', encoding='utf') as f:
        json_data = json.load(f)

    #Look for the user in list
    for j in json_data['employee']:         
        num = 0
        j['Attendence']=j['Attendence'].replace(str(j['Attendence']), str(num))
    
        with open("Attendence.json", 'w', encoding='utf') as f:
            json.dump(json_data, f, indent=2)
    


#send message on telegrams
def send_message():
    x = get_last_name()
    #Add the user to blacklist
    with open("temp_black.txt" , 'r') as t:
        ts = t.readlines()

    if len(ts) != 0:
        ts = ts[0]
    if x[0] == ts:
        print("Requested Report is sent to the user")
    else:
        with open("temp_black.txt" , 'w') as t:
            t.write(x[0])
    todays = date.today()
    today = todays.strftime("%d-%b-%Y")
    with open('Attendence.json', "r+") as json_data:
        data = json.load(json_data)
    

            
    current_path = os.getcwd()

    path = todays.strftime("%b-%Y")
    new_path = ('Attendance_History/' +path)

    exist = os.path.exists(new_path)

    if exist == False:
        os.makedirs("Attendance_History/" + path)
        df = pd.DataFrame(data['employee'])
        df.to_csv("Attendance_History/" + path+ "/" + todays.strftime("%d-%b-%Y") +".csv")
    else:    
        df = pd.DataFrame(data['employee'])
        df.to_csv("Attendance_History/" + path+ "/" + todays.strftime("%d-%b-%Y") +".csv")

    
    with open("Attendance_History/" + path+ "/" + todays.strftime("%d-%b-%Y") +".csv", "rb") as f:
            file_data = f.read()
            filename = f.name
    send_mail(file_data, filename)


    text = (str(today) +"\n" + "\n" +str(df.to_string()))

    users = ['1085230034','1372390818', '1689460227', ]
    for u in users:
        url = "https://api.telegram.org/{}/sendMessage?chat_id={}&text=Date: {}".format(api,u,text) 
        requests.get(url)

reset()
    
#send message on telegrams
def send_message_requested():
    #Add the user to blacklist
    with open("temp_black.txt" , 'r') as t:
        ts = t.readlines()

    if len(ts) != 0:
        ts = ts[0]
    if x[0] == ts:
        print("Requested Report is sent to the user")
    else:
        with open("temp_black.txt" , 'w') as t:
            t.write(x[0])
        today = date.today()
        with open('Attendence.json', "r+") as json_data:
            data = json.load(json_data)

        df = pd.DataFrame(data['employee'])
        text = (str(today) +"\n" + "\n" +str(df.to_string()))
        users = ['1085230034','1372390818', '424751615']
        for u in users:
            url = "https://api.telegram.org/{api}/sendMessage?chat_id={}&text=Date: {}".format(api,u,text)  
            requests.get(url)



    

    


def callfunction():
    global x   
    x = get_last_name()

    print("Last message from : " + x[0])
    time.sleep(2)
    #Check users
    if "#my_report" in x[1]:
        print("Found report") 
        check_user()

    #open Attendence File
    with open("Attendence.json", 'r+', encoding='utf') as f:
        json_data_allowed = json.load(f)

    if "#show_report" in x[1]:
        for a in json_data_allowed['Allowed']:
            if x[0] == a['name']:
                print("Message sent from" + a['name'])
                send_message_requested()

def sch():
    if datetime.datetime.today().strftime('%d') == "05":
            if datetime.datetime.now().strftime('%H:%M') == "00:00":
                send_message()
    if datetime.datetime.today().strftime('%d') == "16":
            if datetime.datetime.now().strftime('%H:%M') == "20:21":
                send_message()


send_message()