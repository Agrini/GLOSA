from tkinter import *
import requests
import json
from math import radians, sin, cos, acos
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)
sheet = client.open("MP6").sheet1  # Open the spreadhseet

def map(x,a,b,c,d):
    y=c+((x-a)*(d-c)/(b-a))
    return int(y)

def traffic_display(p,q,r,s,tr):        #to display traffic density at ech corridor
    e = canvas.create_rectangle(q, r + 15, q + tr[3], s - 2, width=0, fill="#A9A9A9")
    n=canvas.create_rectangle(q-15,r-tr[0],q-2,r,width=0,fill="#A9A9A9")
    w=canvas.create_rectangle(p-tr[1],r+2,p,r+15,width=0,fill="#A9A9A9")
    s=canvas.create_rectangle(p+2,s,p+15,s+tr[2],width=0,fill="#A9A9A9")


send_url = "http://api.ipstack.com/check?access_key=437ae9badeb5aa656506b32b2fc1522d"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
X=slat = geo_json['latitude']
Y=slon =geo_json['longitude']

# coordinates of all corners
Xmin=X-0.0030909
Xmax=X+0.00191
Ymin=Y-0.0042
Ymax=Y+0.0018

coord=[[X,Y-0.00067],[X-0.00238,Y-0.00067],[X,Y-0.003433],[X-0.00238,Y-0.003433]]

x=curlat=map(slat,Xmin,Xmax,0,600)    ##gives latitude maping on x axis
y=curlon=1000-map(slon,Ymin,Ymax,0,900)  #longitude maping on y axis

slat=radians(slat)
slon=radians(slon)

root = Tk()
root.geometry('1500x900')

canvas = Canvas(root,width=600,height=900,bg="#121229")
canvas.pack()
canvas.create_rectangle(356, 0, 386, 900,fill="#F3DDF9",width=0)
canvas.create_rectangle(70, 0, 100, 900,fill="#F3DDF9",width=0)
canvas.create_rectangle(0, 100, 600, 130,fill="#F3DDF9",width=0)
canvas.create_rectangle(0, 520, 600, 550,fill="#F3DDF9",width=0)


def Display() :
    traffic = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    m = 0
    while (m != 4):
        i = 5 * m + 1
        t = 0
        while (t != 4):
            i = i + 1  # m=row of traffic      t=column of traffic     i= row in google sheets
            traffic[m][t] = float(sheet.cell(i, 2).value)  # takes value of similarity from google sheets
            t = t + 1

        m = m + 1

    traffic_display(70, 100, 100, 130, traffic[3])
    traffic_display(356, 386, 100, 130, traffic[2])
    traffic_display(70, 100, 520, 550, traffic[1])
    traffic_display(356, 386, 520, 550, traffic[0])

    dist = [0, 0, 0, 0]
    i = 0
    while (i != 4):
        elat = radians(coord[i][0])
        elon = radians(coord[i][1])
        dist[i] = 6371.01 * acos(sin(slat) * sin(elat) + cos(slat) * cos(elat) * cos(slon - elon))
        i = i + 1

    d = min(dist)
    i = 0
    while (i != 4):
        if (dist[i] == d):
            tmp = i
        i = i + 1

    X = map(coord[tmp][0], Xmin, Xmax, 0, 600)
    Y = map(coord[tmp][1], Ymin, Ymax, 0, 900)
    r = canvas.create_rectangle(X - 15, Y - 15, X + 15, Y + 15, width=3, dash=(4, 2))

    if abs(x - X) > abs(y - Y):
        if (X - x) > 0:
            current_corr = 1
        else:
            current_corr = 3
    else:
        if (Y - y) > 0:
            current_corr = 0
        else:
            current_corr = 2

    num2corr = ['North', 'West', 'South', 'East']
    oc = int(sheet.cell(1, 2).value)
    print(oc)
    print(current_corr)
    display = 'For the upcoming intersection\nOpen Corridor: ' + num2corr[oc] + '\nYour corridor: ' + num2corr[
        current_corr];
    label1 = Label(root, text=display, bg='DarkSeaGreen3', width=25, height=3, font="Times 20", relief="raised")
    label1.place(x=10, y=160)

    time = 0

    if oc==current_corr:
        time=int(sheet.cell(oc + 2, 3).value)
    else:
        while (oc != current_corr):
            time = time + int(sheet.cell(oc + 2, 3).value)
            oc = (oc + 1) % 4



    ltime = time
    utime = time + 10
    lt = ltime / 3600
    ut = utime / 3600
    uspeed = int(d / lt)
    lspeed = int(d / ut)

    label2 = Label(root, text=('Distance till intersection :\n' + str(round(d, 1)) + ' km'), bg='DarkSeaGreen3',
                   width=25, height=3, font="Times 20", relief="raised")
    label2.place(x=10, y=260)

    label3 = Label(root, text=('Time till the corridor opens :\n' + str(ltime) + ' - ' + str(utime) + ' seconds'),
                   bg='DarkSeaGreen3', width=25, height=3, font="Times 20", relief="raised")
    label3.place(x=10, y=360)

    var = StringVar()
    label4 = Label(root, textvariable=var, bg='DarkSeaGreen3', width=25, height=3, font="Times 20", relief="raised")
    label4.place(x=10, y=460)

    if (uspeed > 40) & (lspeed > 40):
        var.set("You need to wait till the traffic clears. ")
    elif uspeed > 40:
        var.set("Drive safely with speed :\n" + str(lspeed) + " - 40 km/hr")
    else:
        var.set("Drive safely with speed :\n" + str(lspeed) + " - " + str(uspeed) + " km/hr")

    o = canvas.create_oval(curlat - 7, curlon - 7, curlat + 7, curlon + 7, fill="red", width=0)

    B = Button(root, text="  Refresh  ", command=Display, width=12, height=1, relief="raised", bg='DarkSeaGreen3',font="Times 20")
    B.place(x=1100, y=510)

    root.mainloop()

Display()

