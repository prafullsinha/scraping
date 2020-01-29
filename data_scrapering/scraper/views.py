import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.generic import TemplateView
from .forms import IdForm
from .models import ObjectModel
from django.shortcuts import redirect, render

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
        temp = {
            'review_title': i.review_title,
            'review_rating': i.review_rating,
            'review_content': i.review_content,
        }
        list1.append(temp)
    return JsonResponse(list1, safe=False)


def scrape(product_id):
    session = requests.Session()
    session.headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 "
                      "Safari/537.36"}
    url = 'https://www.mouthshut.com/product-reviews/' + product_id
    content = session.get(url, verify=False).content
    soup = BeautifulSoup(content, 'html.parser')

    reviews = soup.find_all('div', {'class': 'review-article'})

    for i in reviews:
        title = i.find('a').text
        print("new title: {}".format(title))

        rating = i.find_all('i', {'class': 'icon-rating rated-star'})
        message = i.find_all('div', {'class': 'reviewdata'})
        print("Printing  message")
        msg = [x.text for x in message][0].rsplit("...", 1)[0].strip()

        ObjectModel.objects.create(product_id=product_id,
                                   review_title=title,
                                   review_rating=len(rating),
                                   review_content=msg)
    return 0
