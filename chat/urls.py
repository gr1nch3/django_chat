from django.urls import path
from .views import inbox, messages_list, signup, users_list
from django.contrib.auth import views as auth_views

app_name = 'chat'


urlpatterns = [
    path('', messages_list.as_view(), name='message_list'),
    path('meet/', users_list.as_view(), name='users_list'),
    path('signup/', signup, name='signup'),
    path('inbox/<str:username>/', inbox.as_view(), name='inbox'),
    # path('send_message/', send_message, name='send_message'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='chat:message_list'), name='logout'),
]