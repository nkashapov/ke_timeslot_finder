from datetime import datetime, timedelta
from urllib import request
import requests
import json
import time
import logging


def update_auth():
    burp0_url = "https://api.business.kazanexpress.ru:443/api/oauth/token"
    burp0_headers = {"Sec-Ch-Ua": "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"99\"", "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic a2F6YW5leHByZXNzOnNlY3JldEtleQ==", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": "https://business.kazanexpress.ru", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://business.kazanexpress.ru/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"}
    burp0_data = {"grant_type": "password", "username": login_ke, "password": password_ke}
    response = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
    print(response.text)
    auth_tokens = json.loads(response.text)
    print(auth_tokens)
    return auth_tokens["access_token"]


def set_timeslots(shopid, invoices, timeslot):
    post_data="""{"invoiceIds":invoices_change,"timeFrom": time_to_set }"""
    post_data = post_data.replace("invoices_change", str(invoices))
    post_data = post_data.replace("time_to_set",str(timeslot))
    url_toset= f"https://api.business.kazanexpress.ru/api/seller/shop/{shopid}/v2/invoice/time-slot/set"
    
    response = requests.post(url_toset,headers=auth_headers,data=post_data)
    print(response.request.body)
    print(response.text)

def find_timeslots(shopid, invoices):
    url = f"https://api.business.kazanexpress.ru/api/seller/shop/{shopid}/v2/invoice/time-slot/get"
    time_now = datetime.now() + timedelta(days=1, hours=1)
    milliseconds = int(round(time_now.timestamp() * 1000))
    #print(milliseconds)
    timeslots = []
    post_data = """{"invoiceIds":invoices_change,"timeFrom":"_timestamp_"}"""
    post_data = post_data.replace("invoices_change", str(invoices))
    post_data = post_data.replace("_timestamp_", str(milliseconds))
    try:
        response = requests.post(url,headers=auth_headers,data=post_data)
        response.raise_for_status()
        #print(response.text)
        timestamps_list = json.loads(response.text)
        try:
            timeslots = timestamps_list["payload"]["timeSlots"]
        except:
            timeslots = []
        print(timeslots)
    except requests.exceptions.HTTPError as e:
        print(" ERROR ".center(80, "-"))
        print(e)
        print(response.text)
        if response.status_code == 500 or response.status_code == 401:
            auth_headers["Authorization"] = "Bearer " + update_auth()
            time.sleep(1)
            return []
    except requests.exceptions.RequestException as e:
        print(e)

    return(timeslots)

def main():
    timeslots_1 = []
    timeslots_2 = []
    fo = open("logs2.txt", "w+")
    for i in range(1,10000):
        time.sleep(1)  # пауза в 1 секунду. можно убрать или закомментировать
        if not timeslots_1:
            timeslots_shop_2 = find_timeslots(shop_2,shop_2_invoices)
            if timeslots_shop_2!=[]:
                timeslots_2=timeslots_shop_2[0]["timeFrom"]
                set_timeslots(shop_2,shop_2_invoices, timeslots_2)
                fo.write("DONE 2")
                end_flag_2 = True
        if not timeslots_2:
            timeslots_shop_1 = find_timeslots(shop_1,shop_1_invoices)
            if timeslots_shop_1!=[]:
                timeslots_1=timeslots_shop_1[0]["timeFrom"]
                set_timeslots(shop_1,shop_1_invoices, timeslots_1)
                fo.write("DONE 1")
                end_flag_1 = True
        fo.write(str(timeslots_1) + str(timeslots_2) )
        fo.flush()
        if timeslots_1 and timeslots_2:
            break
    fo.close()


## definition of variables
shop_2 = 10776 # идентификатор второго магазина
shop_1 = 31119 # идентификатор первого магазина 
shop_2_invoices = [3104833,3104848,3128887,3128898] # номера инвойсов накладных (для второго магазина), обязательно через запятую в квадратных скобках
shop_1_invoices = [3083355, 3083357]  # номера инвойсов накладных (для второго магазина), обязательно через запятую в квадратных скобках
end_flag_2 = False # поставить True чтобы выключить поиск для второго магазина
end_flag_1 = False # поставить True чтобы выключить поиск для первого магазина
login_ke = "89179340209" # тут вписываем логин от кабинета КЕ
password_ke = "пароль тут" # тут пароль от кабинета КЕ
auth_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
"Accept": "application/json",
"Accept-Language": "en-US,en;q=0.5",
"Content-Type": "application/json",
"Authorization": "Bearer Ag4htw3MqGlYLgmAo8sR0RRXy_8",
"Content-Length": "3",
"Origin": "https://business.kazanexpress.ru",
"Connection": "keep-alive",
"Referer": "https://business.kazanexpress.ru/",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-site",
"Host": "api.business.kazanexpress.ru"}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()