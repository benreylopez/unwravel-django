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
        json_data = open('/home/superdev/Documents/myproject/unwravel/portfolio/static/data/victoria_secret.json')
        json_portfolios = json.load(json_data)
        topsize = account.topsize
        bottomsize = account.bottomsize
        brasize = account.brasize
        pantysize = account.pantysize
        json_result = []
        for portfolio in json_portfolios:
            product_category = portfolio['product_category']
            available_size = portfolio['available_size']
            print(product_category)
            if product_category == "Panties":
                if pantysize in available_size:
                    json_result.append(portfolio)
            if product_category == "Lingerie":
                # if pantysize in available_size:
                json_result.append(portfolio)
            if product_category == "Bras":
                if brasize in available_size:
                    json_result.append(portfolio)
            # if product_category == "Panties":
            #     if pantysize in available_size:
            #         json_result.append(portfolio)

        return Response(
            data=json_result,
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
		