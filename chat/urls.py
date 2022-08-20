from django.urls import path
from .views import InboxView, UserListsView, MessagesListView, signup
from django.contrib.auth import views as auth_views

app_name = 'chat'


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', MessagesListView.as_view(), name='message_list'),
    path('meet/', UserListsView.as_view(), name='users_list'),
    path('inbox/<str:username>/', InboxView.as_view(), name='inbox'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='chat:message_list'), name='logout'),
]