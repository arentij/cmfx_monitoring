import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import netifaces as ni


def sendmail(destination=['artur_email']):

    team_list = dict(artur='8304994663@tmomail.net',
                artur_email='arentij@gmail.com',
                carlos='9257848145@msg.fi.google.com',
                carlos_email='romero@umbc.edu',
                )

    team = []
    for member in destination:
        try:
            team.append(team_list[member])
        except KeyError:
            print('Unknown destination ' + str(member))

    with open("/home/pereval/PycharmProjects/pythonProject/cmfx_monitoring/static/camphoto.jpg", 'rb') as f:
        img_data = f.read()

    with open("/home/pereval/PycharmProjects/pythonProject/cmfx_monitoring/static/camphoto2.jpg", 'rb') as f:
        img_data2 = f.read()

    msg = MIMEMultipart()
    msg['Subject'] = 'CMFX Pressure'
    msg['From'] = 'CMFX.monitor@gmail.com'
    msg['To'] = ', '.join(team)

    ip = ni.ifaddresses('wlo1')[ni.AF_INET][0]['addr']

    text = MIMEText(ip)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(
        "/home/pereval/PycharmProjects/pythonProject/cmfx_monitoring/static/camphoto.jpg"))
    msg.attach(image)

    image2 = MIMEImage(img_data2, name=os.path.basename(
        "/home/pereval/PycharmProjects/pythonProject/cmfx_monitoring/static/camphoto2.jpg"))
    msg.attach(image2)

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    # s.starttls()
    # s.ehlo()
    s.login("CMFX.monitor@gmail.com", "rsjncajkwmsiodln")
    s.sendmail('CMFX Monitoring', team, msg.as_string())
    s.close()


if __name__ == "__main__":
    destination = ['artur_email', 'artur']
    sendmail(destination)
