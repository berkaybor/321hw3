from django.shortcuts import render
from .database import *


def home(request):
    return render(request, 'drugapp/home.html')


def listDrugs(request):
    drugs = return_drugs()
    drugs_dict = {"drugs_list": drugs}
    return render(request, 'drugapp/home.html', drugs_dict)


def showDrug(request, drugid):
    anan = return_drug_details(drugid)
    drug_dict = {"drug_details": anan}
    return render(request, 'drugapp/drug_detail.html', anan)
