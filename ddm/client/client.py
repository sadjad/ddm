from Socket.Socket import mysocket
from HTTPRequest.Request import Request

def state_function(state):
    if state == 0:
        print "passed"
    elif state == 1:
        print "failed"
        

my_request = Request()
my_request.set_request_URL("http://sadjad.me/media/Yadegari/08%20Bi%20To%20(Remix).mp3")
my_request.set_range(5000000)
print my_request.get_range()
my_request.set_file_name("87.mp3")
my_request.execute_request(state_function)



'''url = "http://ce.sharif.edu/~fouladi/87.txt"

myNewsocket = mysocket()
myNewsocket.'''


'''myNewSocket = mysocket()
myNewSocket.connect('www.google.com',80)
myNewSocket.mysend('GET / HTTP/1.1\r\nHOST: www.google.com \r\n\r\n')
myNewSocket.myreceive()
'''