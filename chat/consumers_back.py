from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import datetime
from . import models
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # self.accept()
        # self.send('{"type":"accept","status":"accepted"}')

        # print(self.scope.get("user"))
        # print(self.scope.get("session"))
        # print(self.scope.get("session").get("get_me_from_the_consumer"))

        # self.scope.get("session")["get_me_from_the_main_page"]="hi my name is mohammed"
        # print(self.scope.get("url_route").get("kwargs").get("name"))

        # print(self.channel_name)
        # print(self.channel_layer.channels)
        # print(self.channel_layer.groups)

        # async_to_sync(self.channel_layer.group_add)("momo_group", self.channel_name)
        # print(self.channel_layer.groups)

        # async_to_sync(self.channel_layer.group_add)("group_channels", self.channel_name)

        # data = {
        #     "type": "recevier.function",
        #     "message": "hi my name is mohammed",
        #     "my_last_name": "almalki"
        # }

        # async_to_sync(self.channel_layer.group_send)("group_channels", data)

        # async_to_sync(self.channel_layer.group_add)("test",self.channel_name)

        # print(self.scope.get("url_route").get("kwargs").get("id"))

        self.accept()

        # print(f"Full Scope: {self.scope}")

        print("username : " ,self.scope.get("user").username)
        print("pk : " ,self.scope.get("user").pk)
        print("user : " ,User.objects.get(username=self.scope.get("user").username))

        user = self.scope.get("user").username
        user_info = User.objects.get(username=user)

        try:
            # user_channel.user = models.UserChannel.objects.get(user=self.scope.get("user").username)
            user_channel = models.UserChannel.objects.get(user=user_info)
            user_channel.channel_name = self.channel_name
            user_channel.save()
        except:
            user_channel = models.UserChannel()
            # username= self.scope.get("user")
            # user_channel.user = User.objects.get(username=username)
            user_channel.user = User.objects.get(username=user_info)
            user_channel.channel_name = self.channel_name
            user_channel.save()

        self.person_id = self.scope.get("url_route").get("kwargs").get("id")
        self.scope['session']['person_id'] = self.person_id


    # def receive(self, text_data):
    #     # print(text_data)
    #     # self.send('{"type":"event_arrive","status":"arrived"}')
    #     text_data = json.loads(text_data)
    #     # print(text_data.get("type"))
    #     # print(text_data.get("message"))
    #     # print("person_id : ",self.scope['session']['person_id'])
    #     now = datetime.datetime.now()
    #     date = now.date()
    #     time = now.time()

    #     other_user = User.objects.get(id=self.person_id)

    #     print("from : ",self.scope.get("user"))
    #     print("to : ",other_user)

    #     new_message = models.Message()
    #     new_message.from_who = self.scope.get("user")
    #     new_message.to_who = other_user
    #     new_message.message = text_data.get("message")
    #     new_message.date = date
    #     new_message.time = time
    #     new_message.has_been_seen = False
    #     new_message.save()

    #     try:
    #         user_channel_name = models.UserChannel.objects.get(user=other_user)
    #         data = {
    #             "type": "recevier_function",
    #             "type_of_data": "new_message",
    #             "data": text_data.get("message")
    #         }

    #         async_to_sync(self.channel_layer.send)(user_channel_name.channel_name, data)
    #     except:
    #         pass

    def receive(self, text_data):
        text_data = json.loads(text_data)
        other_user = User.objects.get(id=self.person_id)
        print("other_user : ",other_user.username)



        if text_data.get("type") == "new_message":
            now = datetime.datetime.now()
            date = now.date()
            time = now.time()

            new_message = models.Message()
            new_message.from_who = self.scope.get("user")
            new_message.to_who = other_user
            new_message.message = text_data.get("message")
            new_message.date = date
            new_message.time = time
            new_message.has_been_seen = False
            new_message.save()

            try:
                user_channel_name = models.UserChannel.objects.get(user=other_user)
                print("user_channel_name.channel_name : ",user_channel_name.channel_name)
                data = {
                    "type": "recevier_function",
                    "type_of_data": "new_message",
                    "data": text_data.get("message"),
                }

                async_to_sync(self.channel_layer.send)(
                    user_channel_name.channel_name, data
                )
            except:
                pass

        elif text_data.get("type") == "i_have_seen_the_messages":
            try:
                user_channel_name = models.UserChannel.objects.get(user=other_user)

                data = {
                    "type": "recevier_function",
                    "type_of_data": "the_messages_have_been_seen_from_the_other",
                }

                async_to_sync(self.channel_layer.send)(
                    user_channel_name.channel_name, data
                )

                messages_have_not_been_seen = models.Message.objects.filter(
                    from_who=other_user, to_who=self.scope.get("user")
                )
                messages_have_not_been_seen.update(has_been_seen=True)
            except:
                pass



    def disconnect(self, code):
        print(code)
        print("hello, stoped")

    def recevier_function(self, the_data_that_will_come_from_the_layer):
        data = json.dumps(the_data_that_will_come_from_the_layer)
        print("data : ", data)
        self.send(data)