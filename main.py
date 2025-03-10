import time
import schedule
import requests
from settings import settings
from database import create_table, find_item, add_item

TOKEN = settings.TOKEN
URL = settings.lolz_url
LOLZAPITOKEN = settings.LOLZAPITOKEN
HEADERS = settings.headers_
CHAT_IDS = settings.chat_ids


def unix_to_date(unix_seconds):
    time_struct = time.localtime(unix_seconds)
    formatted_date = time.strftime("%d %B, %Y", time_struct)
    return formatted_date


def get_items_and_filter_them():
    create_table()
    lst = []
    response = requests.get(URL, headers=HEADERS)
    
    for item in response.json()['items']:
        if str(item['category_id']) == '11':
            item_id = str(item['item_id'])
            existing_item = find_item(item_id)
            
            if existing_item is None:
                lst.append({
                    "price": item['rub_price'],
                    "link": f"https://lzt.market/{item_id}",
                    "account_balance": item['battlenet_balance'],
                    "last_activity": unix_to_date(item['battlenet_last_activity'])
                })
                add_item(
                    item_id, 
                    item['rub_price'],
                    f"https://lzt.market/{item_id}", 
                    item['battlenet_balance'], 
                    unix_to_date(item['battlenet_last_activity'])
                )
    
    if not lst:
        return None
    
    return lst


def send_message_to_telegram(chat_ids: dict) -> None:
    items = get_items_and_filter_them()
    if not items:
        return

    for chat_id in chat_ids:
        for item in items:
            message = ""
            message += "<b>Новый аккаунт!</b>\n\n"
            message += f'Аккаунт: {item["link"]}\n'
            message += f'Цена: {item["price"]} руб.\n'
            message += f'Баланс: {item["account_balance"]} руб.\n'
            message += f'Последнее активное действие: {item["last_activity"]}\n'
        
            response = requests.post(
                f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                data={
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'HTML',
                    'disable_webpage_preview': True
                }
            )
        
            if response.status_code != 200:
                print(f'Error sending message to chat {chat_id}: {response.json()}')


schedule.every(3).seconds.do(send_message_to_telegram, CHAT_IDS)

while True:
    schedule.run_pending()
    time.sleep(1)