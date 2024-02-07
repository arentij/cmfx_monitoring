import datetime
import time
import urllib
import urllib.request
from PIL import Image
from email.mime.text import MIMEText
import smtplib
import loggers
from gmail_info import GmailInfo

class Smoke(GmailInfo):
    def __init__(self):
        super().__init__()
        self.level = 0
        self.team = dict(artur='8304994663@tmomail.net',
                         ruben='3015479282@tmomail.net',
                         heidi='2024152874@tmomail.net',
                         dan='3016466601@txt.att.net',
                         bryan='3017853928@vtext.com')

        self.todaysdate = datetime.date.today().strftime('%m%d%y')
        self.outfile = '/data/3m/' + self.todaysdate + '/smokelevels.log'
        self.url = 'http://192.168.1.114/img/snapshot.cgi?size=3&quality=1'

        self.sentflag1 = 1
        self.sentflag2 = 1
        self.sentflag3 = 0
        self.sentflag0 = 0
        self.lastsenttime1 = 0
        self.lastsenttime2 = 0
        self.connected = False
        self.last_time_read = None
        self.time_to_leave = False

        today = str(datetime.date.today())
        today = today[5:7] + today[8:10] + today[2:4]
        smoke_logger_name = '/data/3m/' + str(today) + '/smokelevels.log'
        self.logger = loggers.setup_logger('smoke_log', smoke_logger_name)

    def connect(self):
        try:
            urllib.request.urlopen(self.url)
            self.connected = True
        except urllib.error.URLError as e:
            print(e)

    def read(self):
        # print('reading smoke')

        with urllib.request.urlopen(self.url) as url:
            u = url.read()
        # u = urllib.urlopen('http://192.168.1.114/img/snapshot.cgi?size=3&quality=1')
        localFile = open('temp/smoke.jpg', 'wb')
        localFile.write(u)
        localFile.close()

        # This opens the image, crops it
        im0 = Image.open('temp/smoke.jpg')
        # box = (292, 54, 297, 215) #original santiago calibration crop box
        # box = (292, 62, 297, 223) #axl testing
        # box = (292, 54, 297, 215) #doug testing
        box = (287, 50, 292, 215)  # Artur testing
        im1 = im0.crop(box)
        im2 = im1.load()
        im1.save('temp/test.jpg')

        # figures out which led is lit
        # j iterates vetically starting from top
        # i iterates horizontally, five pixels across
        # s is the sum of all rgb components for all five pixels for a given j
        # if a led is lit
        j, s = 0, 0
        while (s < 2800 and j < 161):
            s = 0
            for i in range(5):
                s += sum(im2[i, j])
            # print 'j=',j,'s=',s
            j += 1
        # print j

        smoklev = int(round(20.0 * (161.0 - j) / 161.0))

        self.level = smoklev

        if self.level >= 2 and self.sentflag0 == 0 and False:
            message = 'TEST: High Bay smoke testing system alarm test system'
            subject = 'High Bay smoke test'
            self.send_email(['artur', 'ruben'], message, subject)
            self.sentflag0 = 1

        if self.level >= 3 and self.sentflag1 == 0:
            message = 'High Bay smoke level reached 3/20'
            subject = 'High Bay smoke alarm'
            self.send_email(['artur', 'ruben'], message, subject)
            self.sentflag1 = 1

        if self.level >= 5 and self.sentflag2 == 0:
            message = 'High Bay smoke level reached 5/20'
            subject = 'High Bay smoke alarm'
            self.send_email(['artur', 'ruben'], message, subject)
            self.sentflag2 = 1

        if self.level >= 8 and self.sentflag3 == 0:
            message = 'High Bay smoke level reached 8/20'
            subject = 'High Bay smoke alarm'
            self.send_email(['artur', 'ruben', 'dan', 'heidi', 'bryan'], message, subject)
            self.sentflag3 = 1

        now = datetime.datetime.now()
        ssm = str((now - now.replace(hour=0, minute=0, second=0)).total_seconds())
        self.logger.info(ssm + '\t' + str(self.level))

    def send_email(self, destination=['artur'], message='', subject=''):
        team = []
        for member in destination:
            try:
                team.append(self.team[member])
            except KeyError:
                print('Unknown destination ' + str(member))

        # team = [self.team[member] for member in destination]
        me = 'threemeter@sodium.umd.edu'
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = ', '.join(team)
        # s = smtplib.SMTP('localhost')
        # s.sendmail(me, team, msg.as_string())
        # print('Email sent')
        # s.close()

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(self.gmail_user, self.gmail_password)
        # server.login(gmail_user, gmail_password)
        server.sendmail(me, team, msg.as_string())
        server.close()
        print('Email sent')

if __name__ == "__main__":
    smoke = Smoke()

    while True:
        # print('smoke level=' + str(smoke.level))
        time.sleep(5)
        smoke.read()
