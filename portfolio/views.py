import pandas as pd
import numpy as np
from io import StringIO

from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from accounts.models import Account
from django.conf import settings
# from apps.portfolio.models import Portfolio
# from apps.portfolio.serializers import (CreatePortfolioSerializer,
#                                         PortfolioDetailSerializer,
#                                         PortfolioSerializer)

from accounts.models import Account
from accounts.serializers import AccountSerializer
import json


class PortfolioListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get(self, *args, **kwargs):
        print("user: ", self.request.user)
        account = Account.objects.get(email=self.request.user)
        path = settings.BASE_DIR + '/portfolio/static/data/victoria_secret.json'
        json_data = open(path)
        temp_portfolios = json.load(json_data)
        json_portfolios = json.dumps(temp_portfolios)
        result = []
        

        return Response(
            data=json_portfolios,
            status=status.HTTP_200_OK,
            )

class PortfolioListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)


def portfolioList(request):
	user = request.user
	try:
		print("account", user.email)
	except:
		pass

	return HttpResponse("OK")
		