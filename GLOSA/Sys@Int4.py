import numpy as np
import time
import cv2 as cv
from matplotlib import pyplot as plt
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)

client = gspread.authorize(creds)

sheet = client.open("MP6").sheet1  # Open the spreadhseet

while (1):

    ####-----------North
    p = 17
    sheet.update_cell(1, 2, 0)
    sheet.update_cell(3, 3, 20)  # update non open corridors as open time =20
    sheet.update_cell(4, 3, 20)
    sheet.update_cell(5, 3, 20)
    edge = cv.imread('NRef.png', 0)
    now = sum(sum(edge))
    print(now)

    i = random.choice([1, 2, 3])
    print(i)
    j = str(i)
    file = 'North/NStage' + j + '.png'
    print(file)
    img1 = cv.imread(file, 0)
    edges1 = cv.Canny(img1, 150, 250)
    now1 = sum(sum(edges1))

    sim = (now / now1) * 100
    print(sim)

    if (sim > 37):
        nt = 20
    elif (sim > 34):
        nt = 40
    else:
        nt = 30

    sheet.update_cell(p, 2, 100 - sim)
    while nt > 0:
        sheet.update_cell(p, 3, nt)
        time.sleep(3)
        nt = nt - 3

    ####-----------West
    p = p + 1
    sheet.update_cell(1, 2, 1)
    sheet.update_cell(2, 3, 20)  # update non open corridors as open time =20
    sheet.update_cell(4, 3, 20)
    sheet.update_cell(5, 3, 20)
    edge = cv.imread('WRef.jpg', 0)
    now = sum(sum(edge))
    print(now)

    i = random.choice([1, 2, 3])
    print(i)

    j = str(i)
    file = 'West/WStage' + j + '.jpg'
    print(file)
    img1 = cv.imread(file, 0)
    edges1 = cv.Canny(img1, 150, 250)
    now1 = sum(sum(edges1))

    sim = (now / now1) * 100
    print(sim)

    if (sim > 58):
        wt = 40
    elif (sim > 52):
        wt = 20
    else:
        wt = 30

    sheet.update_cell(p, 2, 100 - sim)
    while wt > 0:
        sheet.update_cell(p, 3, wt)
        time.sleep(3)
        wt = wt - 3

    ####-----------South
    p = p + 1
    sheet.update_cell(1, 2, 2)
    sheet.update_cell(2, 3, 20)  # update non open corridors as open time =20
    sheet.update_cell(3, 3, 20)
    sheet.update_cell(5, 3, 20)
    edge = cv.imread('SRef.jpg', 0)
    now = sum(sum(edge))
    print(now)

    i = random.choice([1, 2, 3])
    print(i)
    j = str(i)
    file = 'South/SStage' + j + '.jpg'
    print(file)
    img1 = cv.imread(file, 0)
    edges1 = cv.Canny(img1, 150, 250)
    now1 = sum(sum(edges1))

    sim = (now / now1) * 100
    print(sim)

    if (sim > 15):
        st = 20
    elif (sim > 14.5):
        st = 40
    else:
        st = 30

    sheet.update_cell(p, 2, 100 - sim)
    while st > 0:
        sheet.update_cell(p, 3, st)
        time.sleep(3)
        st = st - 3

    ####-----------East
    p = p + 1
    sheet.update_cell(1, 2, 3)
    sheet.update_cell(2, 3, 20)  # update non open corridors as open time =20
    sheet.update_cell(3, 3, 20)
    sheet.update_cell(4, 3, 20)
    edge = cv.imread('ERef.jpg', 0)
    now = sum(sum(edge))
    print(now)

    i = random.choice([1, 2, 3])
    print(i)
    j = str(i)
    file = 'East/EStage' + j + '.jpg'
    print(file)
    img1 = cv.imread(file, 0)
    edges1 = cv.Canny(img1, 150, 250)
    now1 = sum(sum(edges1))

    sim = (now / now1) * 100
    print(sim)

    if (sim > 18.9):
        et = 30
    elif (sim > 18.4):
        et = 40
    else:
        et = 20

    sheet.update_cell(p, 2, 100 - sim)
    while et > 0:
        sheet.update_cell(p, 3, et)
        time.sleep(3)
        et = et - 3










