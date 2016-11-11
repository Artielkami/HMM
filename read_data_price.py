#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import os
from datetime import datetime
import time
import logging
import math

loger = logging.getLogger('{:^12s}'.format('Read_Data'))
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
                print(price_option['Price'])

        print('json')


# ----------------------------------------------------------------------------------------------------------------------
def create_session(day, org, des, *args, **kwargs):
    """ Return the session has been created """
    url = URL_LIVE_SKYCANNER_API
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    # real: hi198240969190851351185584361476
    # test: prtl6749387986743898559646983194
    form = {
        'apiKey': 'prtl6749387986743898559646983194',
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
    elif r.status_code == 429:
        result['status'] = 0
        result['message'] = 'Please try later, too many request in last minute. Skycanner rejected access !'
    elif r.status_code == 403:
        result['status'] = 0
        result['message'] = 'Input error, please check:' + r.reason
    else:
        result['status'] = 0
        result['message'] = 'Something wrong'
    return result


# ----------------------------------------------------------------------------------------------------------------------
def get_live_data(path, url, day, *args, **kwargs):
    # url = url
    # }     hi684525042063916181915830535816
    # real: hi198240969190851351185584361476
    # test: prtl6749387986743898559646983194

    form = {
        'apiKey': 'prtl6749387986743898559646983194',
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
        create_time = datetime.now().strftime('%Y%m%d')
        # create_time = '20161021'
        place = ''
        if args:
            place = args[0] + '_' + args[1] + '_'
        file_name = 'liveprice_' + place + create_time + '.json'
        data_file = folder + '/live_price/' + file_name

        # check if file exist or not
        if not os.path.exists(data_file):
            response = requests.get(url=url, params=form)
            # time.sleep(0.3)
            logging.debug('Sleep for wait result')
            if response.status_code != 200:
                return None
            # check status code of response
            # ensure that result will

            while response.json()['Status'] != 'UpdatesComplete':
                response = requests.get(url=url, params=form)
            #     logging.debug('sleep ...')
                time.sleep(0.7)
            with open(data_file, 'w') as _file:
                json.dump(response.json(), _file)
        # data_url = folder + '/live_price/' + 'liveprice_20161021.json'
        return data_file
    except TypeError:
        print('Writing file error')
    return True


# ----------------------------------------------------------------------------------------------------------------------
def auto_price(path, file, status, price_init, *args, **kwargs):
    """ Read data from a file then do something """
    # bool variable use for determine result will be written or not
    is_write = False
    # pricing result, which is store at dict type
    result = dict()
    # result content a list, named result_list
    result_list = list()
    logging.debug('Auto pricing start running')
    with open(file) as json_file:
        logging.debug('Access data file success.')
        # load file to json variable
        json_data = json.load(json_file)
        # count number of flight
        iter_count = len(json_data['Itineraries'])
        # ong gia em sun rang, nhai trau cao = 2 nuu rang
        # anh tim mang den em mot cap nhan co
        # last flight have lowest price
        last_iter_min_price = 0
        # loop through all list of Itineraries
        logging.debug('Starting processing every Itineraries')
        for index, initerary in enumerate(json_data['Itineraries']):
            print('- Iteratary %d is running' % index)
            lowest_price = initerary['PricingOptions'][0]['Price']
            if index == iter_count - 1 and status > 0:
                continue
                # cai cuoi cung thi khong tang gia nua
            next_iter_min_price = json_data['Itineraries'][index+1]['PricingOptions'][0]['Price']
            price_op_count = len(initerary['PricingOptions'])

            # if status > 0 and lowest_price == next_iter_min_price:
            #     last_iter_min_price = lowest_price
            #     continue
            # if status < 0 and lowest_price == last_iter_min_price:
            #     last_iter_min_price = lowest_price
            #     continue
            # -------------------------------------------------------------------------------------------------
            # if price_op_count == 1:
            #     if DENA_TRAVEL in initerary['PricingOptions'][0]['Agents']:
            #         # because only one price option, so it also the lowest price
            #         # and the next min price is the limit max price for adjust
            #
            #         # neu gia giam hoac khogn doi thif khong can chinh gia
            #         if status < 0:
            #             last_iter_min_price = lowest_price
            #             continue
            #
            #         dena_price = price_adjust(lowest_price, price_init, status,
            #                                   last_iter_min_price, next_iter_min_price)
            #         tmp = {
            #             'Iteratary': index,
            #             'OutboundLegId': initerary['OutboundLegId'],
            #             'Price': dena_price
            #         }
            #         result_list.append(tmp)
            #         is_write = True
            #     # move to next iter -> current will be last min price
            #     last_iter_min_price = lowest_price
            #     continue
            # --------------------------------------------------------------------------------------------------

            # if there are many price option
            # check each price option:
            # dena -> adjust price
            # other -> next
            limit_price = 0
            # neu khong phai lowest thi khong tang gia nua
            # go to next iter
            is_lowest = False
            if DENA_TRAVEL in initerary['PricingOptions'][0]['Agents']:
                is_lowest = True
            if status > 0 and not is_lowest:
                last_iter_min_price = lowest_price
                continue
            # neu la thap nhat thi khong can giam nua
            if status < 0 and is_lowest:
                last_iter_min_price = lowest_price
                continue
            # > 0 and lowest
            if status > 0 and lowest_price == next_iter_min_price:
                # if next price equals current price, but not belong to dena -> moving to next iter
                if not is_dena_next(json_data['Itineraries'][index + 1]):
                    last_iter_min_price = lowest_price
                    continue
                turn = index + 2
                # get the lowest price of the second one, if not have then return 0
                limit_price = get_min(price=limit_price,
                                      current=initerary,
                                      nex=json_data['Itineraries'][index + 1])
                # get next max price by loop through each next iter
                # check price and make sure the lowest is belong to deNa
                # if not -> max = min of those iter
                # if true -> next
                while turn < iter_count and is_dena_next(json_data['Itineraries'][turn]) \
                        and json_data['Itineraries'][turn]['PricingOptions'][0]['Price'] == lowest_price:
                    limit_price = get_min(price=limit_price,
                                          current=json_data['Itineraries'][turn],
                                          nex=None)
                    turn += 1
                limit_price = get_min(price=limit_price,
                                      current=json_data['Itineraries'][turn],
                                      nex=None,
                                      pos=0)

            for p_index, pricing_option in enumerate(initerary['PricingOptions']):
                # if dena not in, next price option
                if DENA_TRAVEL not in pricing_option['Agents']:
                    continue
                # if not set limit_price on above then set it in here
                # else do not thing
                if p_index == price_op_count - 1 and limit_price == 0:
                    limit_price = next_iter_min_price
                elif limit_price == 0:
                    limit_price = min(next_iter_min_price, initerary['PricingOptions'][p_index+1])

                dena_price = price_adjust(pricing_option['Price'], price_init, status,
                                          last_iter_min_price, limit_price)
                tmp = {
                    'Iteratary': index,
                    'OutboundLegId': initerary['OutboundLegId'],
                    'Price': math.floor(dena_price)
                }
                result_list.append(tmp)
                is_write = True
                if dena_price < lowest_price:
                    lowest_price = dena_price
                if p_index == price_op_count - 1:
                    last_iter_min_price = lowest_price
                    # print pricing_option['Agents']
                # after adjust price -> ignore other pricing option, move to next iti
                logging.debug('Itineraries %d done' % index)
                break

    # when done, write to file
    logging.debug('Start writing file')
    if is_write:
        result['Result'] = result_list
        create_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        place = ''
        if args:
            place = args[0] + '_' + args[1] + '_'
        file_name = 'result_' + place + create_time + '.json'
        data_file = path + '/result/' + file_name
        # time.sleep(1.2)
        with open(data_file, 'w') as fwrite:
            json.dump(result, fwrite)
    logging.debug('Write to file success')


def get_min(price=0, current=None, nex=None, pos=1):
    # get second price between 2 Iti
    count_cur = len(current['PricingOptions'])
    if price == 0 and nex:
        count_next = len(nex['PricingOptions'])
        if count_cur == 1 and count_next > 1:
            return nex['PricingOptions'][pos]['Price']
        if count_next == 1 and count_cur > 1:
            return current['PricingOptions'][pos]['Price']
        if count_cur > 1 and count_cur > 1:
            return min(nex['PricingOptions'][pos]['Price'], current['PricingOptions'][pos]['Price'])
        # if both are only have one member, then return None
        return 0
    if price == 0 and count_cur > 1:
        return current['PricingOptions'][1]['Price']
    if price != 0 and count_cur > 1:
        return min(price, current['PricingOptions'][pos]['Price'])
    if price != 0:
        return min(price, current['PricingOptions'][pos]['Price'])
    if price == 0 and pos == 0:
        return current['PricingOptions'][pos]['Price']
    return 0


def is_dena_next(iter):
    if DENA_TRAVEL in iter['PricingOptions'][0]['Agents']:
        return True
    return False


# ----------------------------------------------------------------------------------------------------------------------
def price_adjust(current, factor, status, min_price, max_price):
    price = current*(1+status*factor)
    # alpha = 0
    # if status > 0 and price == max_price:
    #     return price
    # if status < 0 and price == min_price:
    #     return price
    if min_price == 0:
        alpha = float((2*max_price))/(max_price*max_price)
    else:
        alpha = float((min_price + max_price))/(min_price*max_price)
    while price < min_price or price > max_price:
        if price <= min_price:
            price *= float(1+alpha)
        if price >= max_price:
            price *= float(1-alpha)
    return price


# ----------------------------------------------------------------------------------------------------------------------
def calculation_price(new_ds, old_ds, *args, **kwargs):
    # base = (abs(new_ds-old_ds)+1)*new_ds*old_ds
    delta = abs(new_ds - old_ds) + math.e  # make sure that ln(delta) > 1
    ln_new = math.log(new_ds)
    ln_delta = math.log(new_ds)
    base = delta*ln_new
    x = (float(new_ds) + 1) / (float(old_ds) + 1)
    h = math.log(x, base)*ln_delta/100
    loger.info('h value %f'%h)
    price_new = h*14390
    loger.info('Price from 14390 > %.2f'%price_new)
    return abs(h)


# ----------------------------------------------------------------------------------------------------------------------
def _get_option_price(itera):
    price = 0
    for p in itera['PricingOptions']:
        if price == 0 or price > p['Price']:
            price = p['Agents'][0]
