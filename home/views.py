import json
import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from TwitterAPI import TwitterAPI
from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = "home.html"

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(HomePageView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)        
        return context

    def post(self,request, *args, **kwargs):
        results = None
        negative = 0
        positve = 0
        neutral = 0
        item_count = 0
        tweet_list = []
        context = self.get_context_data(**kwargs)
        query = request.POST.get('search')
        api = TwitterAPI(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESSS_TOKEN_SECRET)
        r = api.request('search/tweets', {'q':query})
        for item in r:
            item_count+=1
            res = requests.post('http://sentimentanalyzer.appspot.com/api/classify?lang=en&content=%s&content-typ=json'%(item.get('text')))
            dict = res.__dict__
            results = json.loads(dict['_content'])
            item['score'] = results['score']
            if item['score']<0.5:
                negative += item['score']
            elif item['score']>0.5:
                positve+=item['score']
            elif item['score']==0.5:
                neutral+=item['score']            
            tweet_list.append(item)
        context['status'] = 'success'
        context['tweet_list'] = tweet_list
        context['html'] = render_to_string('ajax/tweet_content.html', {
                                           'tweet_list': tweet_list, })

        return HttpResponse(json.dumps({'context': context['html'],'status':context['status'],'positve':positve,'negative':negative,'neutral':neutral }), mimetype='application/json')
#       

