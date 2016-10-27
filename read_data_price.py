#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import os
from datetime import datetime
import logging
import math

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


def get_live_data(path, url, day, *args, **kwargs):
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
        folder = path + '/' + day.replace('-', '')

        if not os.path.exists(folder):
            # make folder then also make 'live_price', 'log_search' and 'result'
            os.makedirs(folder)
            data_folder = folder + '/live_price'
            os.makedirs(data_folder)
            data_folder = folder + '/log_search'
            os.makedirs(data_folder)
            data_folder = folder + '/result'
            os.makedirs(data_folder)


        # iters = response['Itineraries']
        # create_time = datetime.now().strftime('%Y%m%d_%H%M%S')

        # get current day
        # create_time = datetime.now().strftime('%Y%m%d')
        create_time = '20161021'
        file_name = 'liveprice_' + create_time + '.json'
        data_file = folder + '/live_price/' + file_name

        # check if file exist or not
        if not os.path.exists(data_file):
            response = requests.get(url=url, data=form)
            with open(data_file, 'w') as _file:
                json.dump(response, _file)

        # data_url = folder + '/live_price/' + 'liveprice_20161021.json'
        return data_file
    except:
        print 'Sum Ting Won'
    return True


def auto_price(path, file, status, *args, **kwargs):
    with open(file) as json_file:
        json_data = json.load(json_file)
        iter_count = len(json_data['Itineraries'])
        last_iter_min_price = 0
        for index, initerary in enumerate(json_data['Itineraries']):
            lowest_price = initerary['PricingOptions'][0]['Price']
            price_op_count = len(initerary['PricingOptions'])
            for pricing_option in initerary['PricingOptions']:
                # if dena not in
                if DENA_TRAVEL not in pricing_option['Agents']:
                    continue

                print pricing_option['Agents']


def calculation_price(new_ds, old_ds, *args, **kwargs):
    base = new_ds + 1
    x = float((new_ds + 1) / (old_ds + 1))
    h = math.log(x, base)
    return h


def _get_option_price(itera):
    price = 0
    for p in itera['PricingOptions']:
        if price == 0 or price > p['Price']:
            price = p['Agents'][0]
