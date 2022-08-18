
from .forms import UserCreation
from django.contrib.auth import login
from .models import Message, UserProfile
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
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


# ------------------------ Function to send a message ------------------------ #



# ---------------------------------------------------------------------------- #
#                               Class based Views                              #
# ---------------------------------------------------------------------------- #

# ----------------------- Inbox/messages/users list ----------------------- #
class messages_list(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'chat/messages_list.html'
    context_object_name = 'message'
    login_url = '/login/'

    # context data for latest message to display
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = UserProfile.objects.get(pk=self.request.user.pk)  # get your primary key
        mess = Message.get_message_list(user)

        other_users = []

        # getting the other person's name
        for i in range(len(mess)):
            if mess[i].sender != user:
                other_users.append(mess[i].sender)
            else:
                other_users.append(mess[i].reciever)

        # getting the latest message from the other person
        # print("length of other_user", len(other_users))
        # print(other_users)

        context['message'] = Message.get_message_list(user)
        context['other_users'] = other_users
        context['you'] = user
        return context


# --------------------------------- Chat view -------------------------------- #
class inbox(LoginRequiredMixin, DetailView):
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
        mess = Message.get_message_list(user) # get the message list  user

        other_users = []

        # getting the other person's name (for message_list)
        for i in range(len(mess)):
            if mess[i].sender != user:
                other_users.append(mess[i].sender)
            else:
                other_users.append(mess[i].reciever)

        sender = other_user  # the sender of the message will be the reciever of the most recent message after it's sent
        reciever = user

        context['messages'] = Message.get_all_messages(sender, reciever)  # get all the messages between the sender and the reciever
        context['message'] = Message.get_message_list(user) # for message_list
        context['other_person'] = other_user  # get the sender of the message (provide the sender's username to the send_message function)
        context['you'] = user  # get the reciever of the message (provide the reciever's username to the send_message function)
        context['other_users'] = other_users

        return context

    # send a message
    def post(self, request, *args, **kwargs):
        # print("sender: ", request.POST.get("you"))
        # print("receiver: ", request.POST.get('reciever'))
        sender = UserProfile.objects.get(pk=request.POST.get('you'))  # get the sender of the message(the person sending it)
        reciever = UserProfile.objects.get(pk=request.POST.get('reciever'))  # get the reciever of the message(You)
        message = request.POST.get('message')  # get the message from the form

        # if the sender is logged in, send the message
        if request.user.is_authenticated:
            if request.method == 'POST':
                if message:
                    Message.objects.create(sender=sender, reciever=reciever, message=message)
            return redirect('chat:inbox', username=reciever.username)  # redirect to the inbox of the reciever

        else:
            return render(request, 'auth/login.html')

# -------------------------------- Users list -------------------------------- #
class users_list(LoginRequiredMixin, ListView):
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