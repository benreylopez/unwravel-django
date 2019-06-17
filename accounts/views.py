from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect

from accounts.serializers import AccountSerializer


class MyAccountView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user


class ConfirmEmailView():
    pass

def confirm_login(request):
	print(request.user.username)
	return redirect("http://localhost:3000/frontend/login/")

class ConfirmAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer
    print("I am USER")
    def get(self, *args, **kwargs):
    	print('USER:',self.request.user)
