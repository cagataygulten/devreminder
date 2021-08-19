from flask import Flask, request, abort
from flask_restful import Api, Resource, reqparse
import requests
import time

app = Flask(__name__)
api = Api (app)

message_put_args = reqparse.RequestParser()
message_put_args.add_argument("info",type=str, help="Enter Process Info ")
message_put_args.add_argument("chatid",type=int, help="Chat Id")
message_put_args.add_argument("time",type=float, help="Total elapsed time")
message_put_args.add_argument("ec",type=int, help="Execution count")

spam_dict={}

def sec_to_hours(seconds):
    day= str(seconds//86400)
    hour=str((seconds%86400//3600))
    minute = str((seconds%3600)//60)
    second=str((seconds%3600)%60)
    total_txt="{}{}{}{}".format("" if day == "0" else (day+" day " if day == "1" else day+' days '),
                                 "" if hour == "0" else (hour+" hour " if hour == "1" else hour+' hours '),
                                 "" if minute == "0" else (minute+" minute " if minute == "1" else minute+' minutes '),
                                 "" if second == "0" else (second+" second" if second == "1" else second+' seconds'))
    return total_txt

class MessageInfo(Resource):

    def __init__(self):
        self.token = "token"

    def send_msg(self,chat_id,text):
        url_req = "https://api.telegram.org/bot" + self.token + "/sendMessage" + "?chat_id=" + str(chat_id) + "&text=" + text
        results = requests.get(url_req)

    def put(self):
        args = message_put_args.parse_args()
        sender_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        title=args["info"]
        chat_id=args["chatid"]
        ec=args["ec"]
        total_time= args["time"]
        total_time_txt= sec_to_hours(round(total_time))
        if total_time_txt=="":
            total_time_txt = "Less than one second"

        info_emoji = u'\U00002139'
        number_emoji = u'\U0001F522'
        clock_emoji = u'\U000023F1'

        if title != None:

            total_txt = "Your process has finished. \n\nExecution \n" + number_emoji + " Count: "+ str(ec) + "\n" +  info_emoji +" Name: " + title + "\n"+clock_emoji+" Time: "+ total_time_txt
            self.send_msg(chat_id,
                total_txt)
        else:
            total_txt = "Your process has finished. \n\nExecution \n" + number_emoji + " Count: " + str(
                ec) + "\n" + clock_emoji + " Time: " + total_time_txt
            self.send_msg(chat_id,total_txt)


        try:
            if spam_dict[sender_ip][0] == 10:
                    self.send_msg(chat_id,
                                  "You have requested 10 times in a minute which is the limit count. Your next requests will be ignored for "
                                  +str((60-round(time.time()-spam_dict[sender_ip][1])))+' seconds.')
        except:pass


        return args,201

    @app.before_request
    def block_method():

        sender_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)


        if sender_ip in spam_dict.keys():
            spam_dict[sender_ip][0] += 1
            if time.time()-spam_dict[sender_ip][1]>60:
                del spam_dict[sender_ip]
            else:
                if spam_dict[sender_ip][0]>10:
                    abort(403)
                else:pass
        else:
            spam_dict[sender_ip] = [1,time.time()]
        print(spam_dict)

class Welcome(Resource):
    def get(self):
        return "Welcome to Devrimender! Project's github repository : https://github.com/cagataygulten/devreminder "


api.add_resource(MessageInfo,"/messageinfo")
api.add_resource(Welcome,"/welcome")

if __name__ == "__main__":

    app.run(debug=True)