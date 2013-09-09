import socket
import urllib
from bs4 import BeautifulSoup
from random import randint
from time import sleep
from time import clock

nick = 'Saundy'
network = 'chat.freenode.net'
port = 8000
chan = '#r/kansascity'
#chan = '#bottesting'
subreddit = 'askreddit'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

irc.connect((network,port))

irc.recv (4096)
irc.send('NICK ' + nick + '\r\n')
irc.send('USER ' + nick + ' 8 * :' + nick + '\r\n')
irc.send('JOIN ' + chan + '\r\n')

nexttime = clock() + randint(600,3600)

while True:
    data = irc.recv (4096)
    print data
    if data.find('PING') != -1:
        irc.send('PONG ' + data.split()[1] + '\r\n')
        if clock() > nexttime:
            try:
                f = urllib.urlopen('http://www.reddit.com/r/' + subreddit)

                s = f.read()
                f.close()

                soup = BeautifulSoup(s)

                test = soup.find_all("a", class_="title")
                
                message = test[randint(0,len(test)-1)].contents[0]
                
                irc.send('PRIVMSG ' + chan + ' :' + message + '\r\n')
            except:
                print 'exception caught'
                
            nexttime = clock() + randint(600,3600)
        
    if data.find('PRIVMSG ' + nick + ' :bye bot') != -1:
        irc.send('QUIT :Food\r\n')
    
    if data.find('PRIVMSG ' + nick + ' :now') != -1:
        try:
            f = urllib.urlopen('http://www.reddit.com/r/' + subreddit)

            s = f.read()
            f.close()

            soup = BeautifulSoup(s)

            test = soup.find_all("a", class_="title")
            
            message = test[randint(0,len(test)-1)].contents[0]
            
            irc.send('PRIVMSG ' + chan + ' :' + message + '\r\n')
        except:
            print 'exception caught'
            
        nexttime = clock() + randint(600,3600)
    
    if data.find('PRIVMSG ' + nick + ' :subreddit') != -1:
        print 'Setting subreddit: ' + data.split()[4]
        
        subreddit = data.split()[4]
    
    if len(data) == 0:
        break;
    