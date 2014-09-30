from flask import Flask, request, redirect
import twilio.twiml
import re

app = Flask(__name__)



@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    smsbody = request.values.get('Body', None)
    smsbody = smsbody.lower()
    #if a user texts links they will recived a message with our facebook and bathstudent links
    if smsbody == "links":
        message = "Facebook: bit.do/bathcs  Bath Student: bathstudent.com/bcss"
    elif smsbody == "about":
        message = "A society for people interested in tech. We host a beginner programming course; tech talks; nights out and many other events!"
    elif smsbody == "course":
        message = "The programming course takes place tomorrow in 3E 3.1 at 6:15pm. See you there!"
    elif smsbody == "pizza":
        message = "The pizza and video games night takes place this Thursday in 8W 2.1 at 6:15pm. See you there!"
    elif smsbody == "phone":
        message = "This will add your number to our phone notification system. If this is ok reply: confirm"
    elif smsbody == "confirm":
        file = open("numbers.txt", "a")
        file.write(request.values.get('From', None)+"\n")
        file.close()
        message = "Thank you your number was added to our notification system. If this was done in error and you wish to be removed reply: STOP"
    elif smsbody == "stop":
        file = open("numbers.txt", "a")
        file.write(request.values.get('From', None)+"remove \n")
        file.close()
    #if user send email, write it to the file
    elif re.match("[^@]+@[^@]+\.[^@]+", smsbody):
        file = open("emails.txt", "a")
        file.write(smsbody+"\n")
        file.close()
        message = "Thank you, your email has been added to our mailing list. Don't forget to like us on Facebook and buy your membership!"
    else:
        message = "Hi this is BCSS. To join our mailing list reply with your email. Otherwise commands available are: about, links, phone, course, pizza"
    resp = twilio.twiml.Response()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)