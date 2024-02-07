import datetime
import time
import urllib
import urllib.request
from PIL import Image
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import smtplib


class Mailing:
    def __init__(self):
        super().__init__()
        self.level = 0
        self.team = dict(artur='8304994663@tmomail.net',
                         artur_email='pereval@umbc.edu',
                         carlos='9257848145@msg.fi.google.com',
                         )

        self.todaysdate = datetime.date.today().strftime('%m%d%y')
        # self.outfile = '/data/3m/' + self.todaysdate + '/smokelevels.log'
        # self.url = 'http://192.168.1.114/img/snapshot.cgi?size=3&quality=1'

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
        # smoke_logger_name = '/data/3m/' + str(today) + '/smokelevels.log'
        # self.logger = loggers.setup_logger('smoke_log', smoke_logger_name)

    def send_email(self, destination=['artur_email'], message=MIMEMultipart('alternative'), subject=''):
        team = []
        for member in destination:
            try:
                team.append(self.team[member])
            except KeyError:
                print('Unknown destination ' + str(member))

        # team = [self.team[member] for member in destination]
        me = 'CMFX monitor system'
        msg = message
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = ', '.join(team)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login("CMFX.monitor@gmail.com", "rsjncajkwmsiodln")
        server.sendmail(me, team, msg.as_string())
        server.close()
        print('Email sent')


if __name__ == "__main__":
    mailing = Mailing()

    msg = MIMEMultipart('alternative')
    img1 = MIMEImage(open("/home/pereval/PycharmProjects/pythonProject/cmfx_monitoring/static/camphoto.jpg", 'rb').read())
    img1.add_header('Content-ID', '<image1>')
    msg.attach(img1)
    text = MIMEText('<img src="cid:image1">', 'html')
    text2 = MIMEText('Hello world!')
    msg.attach(text)
    msg.attach(text2)

    # img2 = MIMEImage(open("/home/pereval/PycharmProjects/pythonProject/cmfx_monitoring/static/camphoto2.jpg", 'rb').read())
    # img2.add_header('Content-ID', '<image2>')
    # msg.attach(img2)
    # text2 = MIMEText('<img src="cid:image2">', 'html')
    # msg.attach(text2)

    mailing.send_email(['artur'], msg, 'CMFX Pressure')
    #
    # while True:
    #     # print('smoke level=' + str(smoke.level))
    #     time.sleep(5)
    #     smoke.read()

