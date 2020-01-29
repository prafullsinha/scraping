import requests
from bs4 import BeautifulSoup
import json
from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from .forms import IdForm
from .models import ObjectModel
from django.shortcuts import redirect, render, HttpResponse
from django.core import serializers
requests.packages.urllib3.disable_warnings()


class ScrapeView(TemplateView):
    template_name = 'scraper/home.html'

    def get(self, request, *args, **kwargs):
        form = IdForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = IdForm(request.POST)
        if form.is_valid():
            abc = form.save(commit=False)
            scrape('{}'.format(abc.product_id))
            return redirect('deatil', product_id=abc.product_id)
        else:
            form = IdForm()
        return render(request, self.template_name, {'form': form})


def DetailView(request, product_id, *args, **kwargs):
    dict1 = ObjectModel.objects.filter(product_id=product_id)
    list1 = []
    for i in dict1:
        listtemp = json.dumps({
            'review_title': i.review_title,
            'review_rating': i.review_rating,
            'review_content': i.review_content,
        })
        list1.append(listtemp) #######object listtemp is not appending in list1
    template = 'scraper/deatil.html'
    context = {
        'list1': list1
    }
    return render(request, template, context)


def scrape(product_id):
    session = requests.Session()
    session.headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 "
                      "Safari/537.36"}
    url = 'https://www.mouthshut.com/product-reviews/' + product_id
    content = session.get(url, verify=False).content
    soup = BeautifulSoup(content, 'html.parser')

    reviews = soup.find_all('div', {'class': 'row review-article'})
    l, m = 0, 0
    for i in reviews:
        if m < 10:
            title = i.find_all('a', {
                'id': 'ctl00_ctl00_ContentPlaceHolderFooter_ContentPlaceHolderBody_rptreviews_ctl{}{}_lnkTitle'.format(
                    l, m)})
        else:
            title = i.find_all('a', {
                'id': 'ctl00_ctl00_ContentPlaceHolderFooter_ContentPlaceHolderBody_rptreviews_ctl{}_lnkTitle'.format(
                    m)})
        m += 1
        rating = i.find_all('i', {'class': 'icon-rating rated-star'})
        message = i.find_all('div', {'class': 'more reviewdata'})
        x, y = 0, 0
        message = str(message)
        # for j in range(len(message)):
        #     if message[j] == '>':
        #         x = j
        #     if message[j] == '<':
        #         y = j
        #         break
        # message = message[x+1:y-1]

        title = str(title)
        for j in range(len(title)):
            if title[j] == '>':
                x = j
            if title[j] == '<' and title[j + 1] == '/':
                y = j
                break
        title = title[x + 1:y]
        print(title,len(rating),message)
        ObjectModel.objects.create(product_id=product_id,
                                   review_title=title,
                                   review_rating=len(rating),
                                         review_content=message)
    return 0


