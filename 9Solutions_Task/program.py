"""
This is a simple program that reads user input from localhols web page and compares it to config files list.
If it finds a mathc, programm will send an email.
There is tempalates file witch has page.html -file.
There is also config.ini file.
For email sendig is used yagmail library
"""

from flask import Flask, render_template,request
from configparser import ConfigParser
import webbrowser
import yagmail

#Reading config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

#get lists from config file to objects
taulukko = config_object.get("Vulnerable_characters", "input")
emails = config_object.get("Email_Adresses", "mona")

def sending():
    #email configurations and sending email to address from config file
    try:
        receiver = emails
        body = "From your localhost page was detected some vulnerable feed! Check security settings."
        yag = yagmail.SMTP("joiku.vain@gmail.com")
        yag.send(
            to = receiver,
            subject = "Alert from vulnerable feed",
            contents = body
        )
    except:
        pass

#open web browser ready to use
webbrowser.open('http://localhost:8000')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('page.html')

@app.route('/', methods=['POST'])
def process():
    # Retrieve the HTTP POST request parameter value
    inputText = request.form['inputText']
    print(inputText)
    #print(taulukko)

    #get first and last characters from user input
    firstChar= inputText.startswith(tuple(taulukko))
    lastChar = inputText.endswith(tuple(taulukko))

    #compare input word to config file chars and if there is a match, email will be send (and cmd output)
    if firstChar or lastChar:
        print("Vulnerable character detected! Email sent!")
        sending()
    else:
        print("All good!")

    return render_template('page.html')

if __name__=='__main__':
    app.run(debug=True, host='localhost', port=8000)


