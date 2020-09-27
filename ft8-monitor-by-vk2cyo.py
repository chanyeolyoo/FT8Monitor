
import requests 
import os, sys
import xmltodict, json
import time
from datetime import datetime

mycallsign = 'VK2CYO'
timeout = 60*15

URL = "https://retrieve.pskreporter.info/query"
PARAMS = {'senderCallsign': mycallsign, 'appcontact':'vk2cyo@gmail.com'} 

def sort_receive(data):
    try:
        str_callsign = data['@senderCallsign']
    except:
        str_callsign = ''

    try:
        str_dB = data['@sNR']
    except:
        str_dB = ''

    try:
        str_localtime = datetime.fromtimestamp(float(data['@flowStartSeconds'])).strftime('%H:%M:%S')
    except:
        str_localtime = ''

    try:
        str_locator = data['@senderLocator']
    except:
        str_locator = ''

    try:
        # str_address = '%s, %s' % (data['@senderRegion'], data['@senderDXCC'])
        str_address = data['@senderRegion']
    except:
        str_address = ''

    try:
        # str_address = '%s, %s' % (data['@senderRegion'], data['@senderDXCC'])
        if len(str_address) > 0:
            str_address = '%s, %s' % (str_address, data['@senderDXCC'])
        else:
            str_address = data['@senderDXCC']
    except:
        pass

    return {'callsign': str_callsign, 'dB': str_dB, 'localtime':str_localtime, 'locator':str_locator, 'address': str_address}
    
def sort_send(data):
    try:
        str_callsign = data['@receiverCallsign']
    except:
        str_callsign = ''

    try:
        str_dB = data['@sNR']
    except:
        str_dB = ''

    try:
        str_localtime = datetime.fromtimestamp(float(data['@flowStartSeconds'])).strftime('%H:%M:%S')
    except:
        str_localtime = ''

    try:
        str_locator = data['@receiverLocator']
    except:
        str_locator = ''

    return {'callsign': str_callsign, 'dB': str_dB, 'localtime':str_localtime, 'locator':str_locator}

def print_dataset(dataset):
    dataset_send = list(filter(lambda d: d['@senderCallsign']==mycallsign, dataset))
    dataset_receive = list(filter(lambda d: d['@receiverCallsign']==mycallsign, dataset))

    lines_send = []
    lines_receive = []

    lines_send.append('====================')
    lines_send.append('Sent by %s' % mycallsign)
    lines_send.append('--------------------')
    for data in dataset_send:
        s = sort_send(data)
        line = '%s | %s | %s | %s' % (s['callsign'].ljust(7), s['dB'].ljust(3), s['localtime'].ljust(8), s['locator'].ljust(10))
        lines_send.append(line)
        # print(line)

    # print()
    lines_receive.append('====================')
    lines_receive.append('Received by %s' % mycallsign)
    lines_receive.append('--------------------')
    for data in dataset_receive:
        s = sort_receive(data)
        line = '%s | %s | %s | %s | %s' % (s['callsign'].ljust(7), s['dB'].ljust(3), s['localtime'].ljust(8), s['locator'].ljust(10), s['address'])
        lines_receive.append(line)
        # print(line)


    if sys.platform == 'linux':
        os.system('clear')
    else:
        os.system('cls')

    num_padd = max([len(line) for line in lines_send])

    for idx in range(max([len(lines_send), len(lines_receive)])):
        try:
            line_send = lines_send[idx]
        except:
            line_send = ''
        line_send = line_send.ljust(num_padd)

        try:
            line_receive = lines_receive[idx]
        except:
            line_receive = ''

        print('%s  ||  %s' % (line_send, line_receive))
    
    now = time.time()
    print('Last update: %s (every 5 minutes)' % datetime.fromtimestamp(now).strftime('%H:%M:%S'))

    print()
    print('Developed by Chanyeol Yoo (VK2CYO), v1.0')
    print('https://github.com/chanyeolyoo/')

lastquery = 0
dataset = []

while True:
    if lastquery == 0 or time.time() - lastquery >= 60*1:
        now = time.time()


        resp = requests.get(url = URL, params = PARAMS)
        content = resp.content
        
        # fid = open('response.txt', 'r')
        # content = fid.read()

        try:
            dataset = xmltodict.parse(content)['receptionReports']['receptionReport']
            dataset = list(filter(lambda data: now-float(data['@flowStartSeconds'])<60*15, dataset))
        except:
            print_dataset(dataset)
            print(content)
            lastquery = now
            continue

        print_dataset(dataset)
        lastquery = now

pass