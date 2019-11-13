from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from . import main
import serial
from bs4 import BeautifulSoup
import requests
res = requests.get('https://www.indiatoday.in/top-stories')
print(res)
try:
    soup = BeautifulSoup(res.text, 'lxml')

    news_box = soup.find('div', {'class': 'may-be-suggest-container'})
    all_news = news_box.find_all('a')

    for news in all_news:
        newsdata=news.text
except:
    newsdata="oops some error occoured"
ser = serial.Serial("COM5",baudrate=9600,timeout=1)
def index(request):
    return render(request,'index.html',{"newsData":newsdata})

def sendajax(request):
    if request.method == 'POST':
        dat=main.chat(request.POST['user'])
        return HttpResponse(dat)
def getValue(val):
    ser.write(val)
    arduinoData = ser.readline().decode('ascii')
    return arduinoData
def lightson(request):
    if request.method == 'POST':
        allup = getValue(b'1')
        allup += getValue(b'3')
        return HttpResponse(allup)
def lightsoff(request):
    if request.method == 'POST':
        allup = getValue(b'2')
        allup += getValue(b'4')
        return HttpResponse(allup)
def light1on(request):
    if request.method == 'POST':
        allup = getValue(b'1')
        return HttpResponse(allup)
def light2on(request):
    if request.method == 'POST':
        allup = getValue(b'3')
        return HttpResponse(allup)
def light1off(request):
    if request.method == 'POST':
        allup = getValue(b'2')
        return HttpResponse(allup)
def light2off(request):
    if request.method == 'POST':
        allup = getValue(b'4')
        return HttpResponse(allup)
