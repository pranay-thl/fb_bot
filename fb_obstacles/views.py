import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
class ObstaclesView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '17071995':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])     
        return HttpResponse()

def post_facebook_message(fbid, recevied_message):         
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAARHaxQCWFIBABm8FWuo0dKHFZCwCZA9ZCfQPxOZCgSsTu5Rp0LLB8L2CqM0or05nys0A1xRr40wLOHfE6STqyu19XfrktZCwLrGPckOleJ7Yyh44ftADALCtLUwINKTWQJBWZBm5CGmp4DBaKp9dgxocrPDiTDZC0sZBsijeUHjrAZDZD'
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'EAARHaxQCWFIBABm8FWuo0dKHFZCwCZA9ZCfQPxOZCgSsTu5Rp0LLB8L2CqM0or05nys0A1xRr40wLOHfE6STqyu19XfrktZCwLrGPckOleJ7Yyh44ftADALCtLUwINKTWQJBWZBm5CGmp4DBaKp9dgxocrPDiTDZC0sZBsijeUHjrAZDZD'}
    user_details = requests.get(user_details_url, user_details_params).json()
    o_text = 'Yo '+user_details['first_name']+'..!' + '\n' + recevied_message
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":o_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

