#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import os

# agents code of DeNA travel
DENA_TRAVEL = 1945844
URL_LIVE_SKYCANNER_API = 'http://partners.api.skyscanner.net/apiservices/pricing/v1.0'
API_KEY = 'hi198240969190851351185584361476'


def read_price(path, day, *args, **kwargs):
    """ Read live data """

    data_url = path + day.replace('-', '') + 'live_price'
    with open(data_url) as json_file:
        json_data = json.load(json_file)
        for initerary in json['Itineraries']:
            for price_option in initerary['PricingOptions']:
                print price_option['Price']

        print('json')


def create_session(day, org, des, *args, **kwargs):
    url = URL_LIVE_SKYCANNER_API
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    # real: hi198240969190851351185584361476
    # test: prtl6749387986743898559646983194
    form = {
        'apiKey': 'hi198240969190851351185584361476',
        'currency': 'JPY',
        'locale': 'jp-JP',
        'country': 'JP',
        'originplace': org,
        'destinationplace': des,
        'outbounddate': day
    }
    r = requests.post(url=url, data=form, headers=header)
    result = {
        'status': 1,  # 1=True, 0=False
        'message': 'Request live data success'
    }
    if r.status_code == 201:
        result['session'] = r.headers['Location']
    elif r.status_code == 409:
        result['status'] = 0
        result['message'] = 'Please try later, too many request in last minute. Skycanner rejected access !'
    elif r.status_code == 403:
        result['status'] = 0
        result['message'] = 'Input error, please check:' + r.reason
    else:
        result['status'] = 0
        result['message'] = 'Something wrong'
    return result


def get_live_data(path, url, day, org, des, *args, **kwargs):
    url = url
    # header = {
    #     'Content-Type': 'application/x-www-form-urlencoded',
    #     'Accept': 'application/json'
    # }
    # real: hi198240969190851351185584361476
    # test: prtl6749387986743898559646983194

    form = {
        'apiKey': 'hi198240969190851351185584361476',
    }
    try:
        response = requests.get(url=url, data=form)

    except:
        print 'Sum Ting Won'
    return True