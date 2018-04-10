'''Written to conduct analyses on network log files 
Answers provided are based on these assumptions on my part:
 a) www.domain.com is different than domain.com
 b) All items being requested in these logs are image files (had my reasons)
 c) Only bytes for status 200 GET items are considered in my "successfully transferred bytes" numbers
 d) Saw some negative bytes in file (unclear what that means).  If they get added to a total, adding as is
 
Written by Stacy Howerton
    Using Windows 10 machine.  
    Last updated 11/10/2017'''

#INPUT: 'LogFiles.txt' == file containing list of apache log files with relative path
#OUTPUT: results to three files: "Client_image_transfer_data.csv", "Client_unique_visitors.csv", amd "Busiest_times.csv" 

#!/usr/bin/python
import os.path
import fileinput
import re
from urllib.parse import urlparse
import datetime

log_parts = [
    r'(?P<ip>\S+)',
    r'\S+',
    r'(?P<remote_user>\S+)',
    r'(?P<req_datetime>.+)\]',
    r'(?P<full_req>"\D+\s\S+\s\S+")',
    r'(?P<status>[0-9]+)',
    r'(?P<transf_bytes>\S+)',
    r'(?P<referer>"http\D+")',
    r'(?P<user_agent>"([^"])*")'
    ]

log_pattern = re.compile(r'\s+'.join(log_parts)+r'\s*')

def main():
    getImageTransferDataForClients()
    getUniqueVisitors()
    getBusiestTimeIntervals()

def getBusiestTimeIntervals():
    '''Bins all hits into time intervals and get number of hits in those intervals, provides as output.'''
    hits_interval_dict = createIntervalHitsDict(readLogListFile())
    getBusiestTimes(hits_interval_dict)
    createOutput(hits_interval_dict, "Busiest_times.csv", "Time interval beginning,Time interval end,Number of Hits, Total Bytes successfully transferred")

def getBusiestTimes(a_dict):
    '''INPUT = Dictionary with time intervals and hits, with bytes.
    OUTPUT = print to screen the busiest time, by hits and bytes.'''
    high_hits, high_bytes = 0, 0
    high_hits_time_min, high_hits_time_max = datetime.time(0,0,0), datetime.time(0,0,0)
    high_bytes_time_min, high_bytes_time_max = datetime.time(0,0,0), datetime.time(0,0,0)
    for key in a_dict.keys():
        hits, num_bytes = int(a_dict[key][1]), float(a_dict[key][2])
        if hits > high_hits:
            high_hits = hits
            high_hits_time_min, high_hits_time_max = key, a_dict[key][0]
        else: continue
        if num_bytes > high_bytes:
            high_bytes = num_bytes
            high_bytes_time_min, high_bytes_time_max = key, a_dict[key][0]
        else: continue
    print("The most hits, %s, occured between %s and %s.\n"% (high_hits , high_hits_time_min, high_hits_time_max))
    print("The most successfully transferred bytes, %s,  occured between %s and %s.\n"% (high_bytes, high_bytes_time_min,high_bytes_time_max))
    
def getUniqueVisitors():
    '''Gets unique hits for each client, regardless of status, provides as output.'''
    client_hits_dict = createClientHitDict(readLogListFile())
    createOutput(client_hits_dict, "Client_unique_visitors.csv", "Client,Number of unique hits, Unique IPs")

def getImageTransferDataForClients():
    '''Gets hits and successfully transferred total bytes data for each client'''
    client_data_dict = createClientTransferDataDict(readLogListFile())
    createOutput(client_data_dict, "Client_image_transfer_data.csv", "Client,Total Successful Transfer Hits,Total Successful Transfer Bytes")

def createIntervalHitsDict(file_list):
    '''INPUT = textfile listing each apache logfile.  For all data from each logfile, dictionary created where k = beginning of
    time interval, v = (end of time interval, number of hits in interval).
    OUTPUT = dictionary returned: hits per time interval of 5 minutes.'''
    hits_interval_dict = createTimeBinDict()
    for key in hits_interval_dict.keys():
        counter = 0
        min_time = key
        max_time = hits_interval_dict[key][0]
        total_bytes = hits_interval_dict[key][2]
        for log_file in file_list:
            fileDir = os.path.dirname(os.path.realpath('__file__'))
            file = os.path.join(fileDir, log_file)
            try: f = open(file)
            except IOError: print("%s not a valid file\n" % file)
            for line in f:
                m = log_pattern.match(line)
                num_bytes, status, request = float(m['transf_bytes'].strip()), m['status'].strip(), m['full_req'].split()[0][1:]
                datetime_items = m['req_datetime'].strip().split(":")
                hours, minutes, seconds = int(datetime_items[1]), int(datetime_items[2]), int(datetime_items[3][:2])
                log_time = datetime.time(hour=hours,minute=minutes,second=seconds)
                if log_time >= min_time and log_time < max_time:
                    counter+=1
                    if status < '300' and request == "GET": total_bytes = total_bytes + num_bytes
                    hits_interval_dict[key] = (max_time, counter, total_bytes)
                else: continue
        f.close()
    return hits_interval_dict   

def createTimeBinDict():
    '''Divides up 24 hours into bins where k = start time, v = (end time, number of hits, total bytes successfully transferred).
    OUTPUT = Returns dictionary of bins with hits = 0 for all.'''
    time_bin_dict = {}
    time = datetime.time(0,0,0)
    incr_time = datetime.time(0,5,0)
    max_time = datetime.time(23,55,00)
    while True:
        hours = time.hour + incr_time.hour
        mins = time.minute + incr_time.minute
        secs = time.second + incr_time.second
        last_time = time
        time = datetime.time(hour=hours,minute=mins,second=secs)
        time_bin_dict[last_time]  = (time, 0, 0)
        if time.minute == 55:
            time = datetime.time(hour=time.hour,minute=time.minute,second=time.second)
            new_time = hourFlip(time)
            time_bin_dict[time]  = (new_time, 0, 0)
            if time == max_time:
                time_bin_dict[time] = (datetime.time(0,0,0),0, 0)
                break
            else:
                time = hourFlip(time)
    return time_bin_dict

def hourFlip(time):
    '''INPUT = Datetime time object that needs to move to the next hour.
    OUTPUT = Returns datetime time object with incremented hour'''
    if time.hour == 23:
        new_time = datetime.time(0,0,0)
    else:
        hour_flip = time.hour + datetime.time(1,0,0).hour
        new_time = datetime.time(hour=hour_flip,minute=0)
    return new_time

def createClientHitDict(file_list):
    '''INPUT = textfile listing each apache logfile.  For all data from each logfile, dictionary created where k = client, v = (hits by unique ip's, unique ips).
    OUTPUT = dictionary returned: Number of unique visitors for each client, as well as those unique ip's.'''
    client_hits_dict = {}
    for log_file in file_list:
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        file = os.path.join(fileDir, log_file)
        try: f = open(file)
        except IOError: print("%s not a valid file\n" % file)
        for line in f:
            m = log_pattern.match(line)
            ip = m['ip'].strip()
            client_url = urlparse(m['referer'].strip()[1:])
            client = client_url.netloc
            if client in client_hits_dict:
                ips = client_hits_dict[client][1]
                ip_list = ips.split(' ')
                if ip not in ip_list:
                    ips = ips + ' ' + ip
                else: continue
                client_hits_dict[client] = (len(ips.split(' ')), ips)
            else:
                ips = ip
                num_ips = len(ips.split(' '))
                client_hits_dict[client] = (num_ips, ips)
        f.close()
    return client_hits_dict
    
def createClientTransferDataDict(file_list):
    '''INPUT = textfile listing each apache logfile.  For all data from each logfile, dictionary created where k = client, v = (hits, bytes).
    OUTPUT = dictionary returned: Number of hits and total bytes successfully transferred for each client.'''
    client_data_dict = {}
    for log_file in file_list:
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        file = os.path.join(fileDir, log_file)
        try: f = open(file)
        except IOError: print("%s not a valid file\n" % file)
        for line in f:
            m = log_pattern.match(line)
            status, request = m['status'].strip(), m['full_req'].split()[0][1:]
            client_url = urlparse(m['referer'].strip()[1:])
            client = client_url.netloc
            num_bytes = float(m['transf_bytes'].strip())
            if status < '300' and request == "GET":
                if client in client_data_dict:
                    data_tuple = client_data_dict[client]
                    hits, total_bytes = data_tuple[0], data_tuple[1]
                    hits = hits + 1
                    total_bytes = total_bytes + num_bytes
                    data_tuple = (hits,total_bytes)
                    client_data_dict[client] = data_tuple
                else:
                    client_data_dict[client] = (1,num_bytes)
            else:
                continue
        f.close()
    return client_data_dict

def createOutput(a_dict, csv_filename, header):
    '''INPUT: dictionary of data
    OUTPUT: outputfile of results in dictionary'''
    output = open(csv_filename, "w")
    output.write(header + "\n")
    for key in a_dict.keys():
        output.write(str(key))
        for item in a_dict[key]:
            output.write("," + str(item))
        output.write("\n")
    print("Your outputfile %s has been written\n" % csv_filename)
    output.close()
    
def readLogListFile():
    '''INPUT = Reads name of each log file to act on, in LogFiles.txt file.
    OUTPUT = Returns list of filenames.'''
    log_filenames = []
    with fileinput.input('LogFiles.txt') as log_files:
        for filename in log_files:
            filename = filename.rstrip()
            log_filenames.append(filename)
    fileinput.close()
    return log_filenames

                   
if __name__ == "__main__": main()
