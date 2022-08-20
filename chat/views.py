from .forms import UserCreation
from django.http import JsonResponse
from django.contrib.auth import login
from .models import Message, UserProfile
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.

# ---------------------------------------------------------------------------- #
#                             Function Based Views                             #
# ---------------------------------------------------------------------------- #

# --------------------------- Creating User Profile -------------------------- #
def signup(request):
    userform = UserCreation()
    if request.method == 'POST':
        userform = UserCreation(request.POST)
        if userform.is_valid():
            uf = userform.save(commit=False)
            uf.save()

            # Login the user and redirect to the home page
            if uf is not None:
                if uf.is_active:
                    login(request, uf)  # login the user
                    return redirect('chat:message_list')  # redirect to the home page

        else:
            # used dictionary to know the field and the error
            errors = {}
            # loop through the form fields and add the errors to the dictionary
            for field in userform:
                for error in field.errors:
                    errors[
                        field.name] = error  # add the error to the dictionary as the value and the field name as the key
            return JsonResponse({"status": False, "errors": errors})

    else:
        userform = UserCreation()
    return render(request, 'auth/signup.html', {'form': userform})

# ---------------------------------------------------------------------------- #
#                               Class based Views                              #
# ---------------------------------------------------------------------------- #

# ----------------------- Inbox/messages/users list ----------------------- #
class MessagesListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'chat/messages_list.html'
    login_url = '/login/'

    # context data for latest message to display
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = UserProfile.objects.get(pk=self.request.user.pk)  # get your primary key
        messages = Message.get_message_list(user) # get all messages between you and the other user

        other_users = [] # list of other users

        # getting the other person's name fromthe message list and adding them to a list
        for i in range(len(messages)):
            if messages[i].sender != user:
                other_users.append(messages[i].sender)
            else:
                other_users.append(messages[i].recipient)


        context['messages_list'] = messages
        context['other_users'] = other_users
        context['you'] = user
        return context


# --------------------------------- Chat view -------------------------------- #
class InboxView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'chat/inbox.html'
    login_url = '/login/'
    queryset = UserProfile.objects.all()


    # to send a message (pass the username instead of the primary key to the post function)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    # overide detailview default request pk or slug to get username instead
    def get_object(self):
        UserName= self.kwargs.get("username")
        return get_object_or_404(UserProfile, username=UserName)



    # context data for the chat view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = UserProfile.objects.get(pk=self.request.user.pk)  # get your primary key
        other_user = UserProfile.objects.get(username=self.kwargs.get("username"))  # get the other user's primary key
        messages = Message.get_message_list(user) # get all messages between you and the other user

        other_users = [] # list of other users

        # getting the other person's name fromthe message list and adding them to a list
        for i in range(len(messages)):
            if messages[i].sender != user:
                other_users.append(messages[i].sender)
            else:
                other_users.append(messages[i].recipient)

        sender = other_user  # the sender of the message will be the recipient of the most recent message after it's sent
        recipient = user # the recipient of the message will be the sender of the most recent message after it's sent

        context['messages'] = Message.get_all_messages(sender, recipient)  # get all the messages between the sender(you) and the recipient (the other user)
        context['messages_list'] = messages # for MessagesListView template
        context['other_person'] = other_user  # get the other person you are chatting with from the username provided
        context['you'] = user  # send your primary key to the post
        context['other_users'] = other_users

        return context

    # send a message
    def post(self, request, *args, **kwargs):
        # print("sender: ", request.POST.get("you"))
        # print("recipient: ", request.POST.get('recipient'))
        sender = UserProfile.objects.get(pk=request.POST.get('you'))  # get the sender of the message(the person sending it)
        recipient = UserProfile.objects.get(pk=request.POST.get('recipient'))  # get the recipient of the message(You)
        message = request.POST.get('message')  # get the message from the form

        # if the sender is logged in, send the message
        if request.user.is_authenticated:
            if request.method == 'POST':
                if message:
                    Message.objects.create(sender=sender, recipient=recipient, message=message)
            return redirect('chat:inbox', username=recipient.username)  # redirect to the inbox of the recipient

        else:
            return render(request, 'auth/login.html')

# -------------------------------- Users list -------------------------------- #
class UserListsView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'chat/users_list.html'
    context_object_name = 'users'
    login_url = '/login/'

    # context data for the users list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = UserProfile.objects.get(pk=self.request.user.pk)  # get your primary key
        context['users'] = UserProfile.objects.exclude(pk=user.pk)  # get all the users except you
        return context