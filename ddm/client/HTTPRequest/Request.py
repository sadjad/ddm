import urllib2
import sys
import time
import socket
from constants import CHUNK_SIZE
from constants import DOWNLOAD_PATH
from constants import SPEED_MAX_CHUNK_NUMBER
from constants import IO_MAX_CHUNK_NUMBER
from constants import MAX_RETRIES


class Request:
    def __init__(self, request_URL=None, chunk_id=None, start_byte=None, end_byte=None, file_name=None):
        self.request_URL = request_URL
        self.chunk_id = chunk_id
        self.start_byte = start_byte
        self.end_byte= end_byte
        self.file_name = file_name
        self.download_speed = 0
        self.downloaded_size = 0
        self.exception_downloaded_size = 0
        self.number_of_retries = 0
        
        
    def set_request_URL(self, request_URL):
        self.request_URL = request_URL
    def set_range(self, start_byte, end_byte=None):
        self.start_byte = start_byte
        self.end_byte = end_byte
    def set_file_name(self, file_name):
        self.file_name = file_name
    def get_request_URL(self):
        return self.request_URL
    def get_range(self):
        return "%d" % self.start_byte + "-" + (("%d" % self.end_byte) if self.end_byte != None else "")
    def get_file_name(self):
        return self.file_name

    def execute_request(self, state_function):
        request_query = urllib2.Request(self.request_URL)
        range_HTTP_string = "bytes=" + "%d" % self.start_byte + "-" + (("%d" % self.end_byte) if self.end_byte != None else "")
        request_query.add_header('Range', range_HTTP_string)
        try:
            desired_chunk = urllib2.urlopen(request_query, timeout=5)
        except (urllib2.HTTPError, urllib2.URLError), msg:
            if self.number_of_retries < MAX_RETRIES:
                print "Cannot Connect to Host... Retry Attempt #" + "%d" % self.number_of_retries
                self.number_of_retries += 1
                self.execute_request(state_function)
            else:
                self.number_of_retries = 0
                state_function(1)
                return
        whole_file_size = desired_chunk.headers["Content-Length"] 
        whole_chunk_size = (self.end_byte - self.start_byte + 1) if self.end_byte != None else int(whole_file_size - self.start_byte)
        downloaded_chunk = ""
        speed_counter = 0
        io_counter = 0
        total_time = 0
        io_save_flag = 0
        try:
            for i in range(1,(whole_chunk_size/CHUNK_SIZE)+2):
                begin_time = time.time()
                downloaded_partial_chunk = desired_chunk.read(CHUNK_SIZE)
                end_time = time.time()
                io_save_flag = 0
                downloaded_chunk += downloaded_partial_chunk
                self.downloaded_size += len(downloaded_partial_chunk)
                self.exception_downloaded_size += len(downloaded_partial_chunk)
                if io_counter < IO_MAX_CHUNK_NUMBER-1:
                    io_counter += 1
                else:
                    io_save_flag = 1
                    io_counter = 0
                    self.save_downloaded_chunk(downloaded_chunk)
                    #print "%d" % (len(downloaded_chunk)/1024) + " Kbytes saved"
                    downloaded_chunk = ""
                
                if speed_counter < SPEED_MAX_CHUNK_NUMBER-1:
                    total_time += end_time-begin_time
                    speed_counter += 1
                else:
                    speed_counter = 0
                    self.download_speed = (CHUNK_SIZE*SPEED_MAX_CHUNK_NUMBER)/total_time
                    total_time = 0
                    #print "%d" % (self.downloaded_size) + " Bytes Downloaded. Speed: " + "%d" % (self.download_speed) + " B/s"
            #print "%d" % (self.downloaded_size) + " Bytes Downloaded. Speed: " + "%d" % (self.download_speed) + " B/s"
            self.save_downloaded_chunk(downloaded_chunk)
            #print "%d" % (len(downloaded_chunk)/1024) + " Kbytes saved"
            print "Finished"
        except socket.timeout, msg:
            print msg
            self.save_downloaded_chunk(downloaded_chunk)
            print "%d" % (len(downloaded_chunk)/1024) + " Kbytes saved"
            self.start_byte += self.exception_downloaded_size
            self.exception_downloaded_size = 0
            print "Download Restarted"
            self.execute_request(state_function)
        state_function(0)
    def save_downloaded_chunk(self, chunk_to_write):
        output_file = open(DOWNLOAD_PATH + self.file_name, "ab")
        output_file.write(chunk_to_write)
        output_file.close()