from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# ---------------------------------------------------------------------------- #
#                                  User Model                                  #
# ---------------------------------------------------------------------------- #

class UserProfile(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'chat_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


# ---------------------------------------------------------------------------- #
#                                 Message Model                                #
# ---------------------------------------------------------------------------- #
class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('-date',)

    # function gets all messages between 'the' two users (requires your pk and the other user pk)
    def get_all_messages(id_1, id_2):
        #     # here we'll treat you(that is log in and checking the messages) as the recipient
        messages = []
        # get messages between the two users, sort them by date(reverse) and add them to the list
        message1 = Message.objects.filter(sender_id=id_1, recipient_id=id_2).order_by('-date')
        for x in range(len(message1)):
            messages.append(message1[x])
        message2 = Message.objects.filter(sender_id=id_2, recipient_id=id_1).order_by('-date')
        for x in range(len(message2)):
            messages.append(message2[x])
        # print(messages)
        # because the function is called when viewing the chat, we'll return all messages as read
        for x in range(len(messages)):
            messages[x].is_read = True
        # sort the messages by date
        messages.sort(key=lambda x: x.date, reverse=False)
        # print(messages)
        return messages

    # function gets all messages between 'any' two users (requires your pk)
    def get_message_list(u):
        # get all the messages
        m = []  # stores all messages sorted by latest first
        j = []  # stores all usernames from the messages above after removing duplicates
        k = []  # stores the latest message from the sorted usernames above
        for message in Message.objects.all():
            for_you = message.recipient == u  # check if the message is for you
            from_you = message.sender == u  # check if the message is from you
            if for_you or from_you:  # if the message is for you or from you, add it to the queryset and sort it
                m.append(message)
                m.sort(key=lambda x: x.sender.username)  # sort the messages by senders
                m.sort(key=lambda x: x.date, reverse=True)  # sort the messages by date

        # remove duplicates usernames and get single message(latest message) per username(other user) (between you and other user)
        for i in m:
            if i.sender.username not in j or i.recipient.username not in j:
                j.append(i.sender.username)
                j.append(i.recipient.username)
                k.append(i)



        # print("messages m: ", m)
        # print("messages j: ", j)
        # print("messages k: ", k)
        # print("messages k length: ", len(k))

        return k
