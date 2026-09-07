import requests
import re
import time
import json
from datetime import datetime
import subprocess
import os
import sys

class PersonSearch:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def parse_fullname(self, fullname):
        parts = fullname.strip().split()
        if len(parts) >= 3:
            surname, name, patronymic = parts[0], parts[1], parts[2]
        elif len(parts) == 2:
            surname, name = parts[0], parts[1]
            patronymic = ""
        else:
            return {"surname": "", "name": "", "patronymic": "", "gender": ""}
            
        gender = self.detect_gender(name)
        return {
            "surname": surname,
            "name": name,
            "patronymic": patronymic,
            "gender": gender
        }
    
    def detect_gender(self, name):
        female_endings = ['а', 'я', 'ия']
        
        if not name:
            return "неизвестно"
            
        last_char = name[-1]
        if last_char in female_endings:
            return "женский"
        else:
            return "мужской"
    
    def search_vk(self, surname, name):
        results = []
        try:
            search_url = f"https://vk.com/people/{surname}_{name}"
            response = self.session.get(search_url)
            if response.status_code == 200:
                results.append({
                    'platform': 'VK',
                    'url': search_url
                })
        except:
            pass
        return results
    
    def search_ok(self, surname, name):
        results = []
        try:
            search_url = f"https://ok.ru/search?st.query={surname}+{name}"
            response = self.session.get(search_url)
            if response.status_code == 200:
                results.append({
                    'platform': 'OK',
                    'url': search_url
                })
        except:
            pass
        return results
    
    def search_cases(self, surname, name, patronymic, birth_date=""):
        try:
            import requests
            url = "https://cases.x-cr.ru/verify.html"
            data = {
                'surname': surname,
                'name': name,
                'patronymic': patronymic,
                'birthdate': birth_date
            }
            response = requests.post(url, data=data)
            if "судимость" in response.text.lower():
                return {"has_criminal_record": True, "details": "Найдена судимость"}
            else:
                return {"has_criminal_record": False, "details": "Судимость не найдена"}
        except Exception as e:
            return {"has_criminal_record": None, "details": f"Ошибка: {str(e)}"}

class PhoneSearch:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.city_db = self.load_cities()
        
    def load_cities(self):
        cities = {
            '495': 'Москва',
            '496': 'Московская область',
            '498': 'Московская область',
            '499': 'Москва',
            '812': 'Санкт-Петербург',
            '813': 'Ленинградская область',
            '846': 'Самара',
            '343': 'Екатеринбург',
            '383': 'Новосибирск',
            '861': 'Краснодар',
            '843': 'Казань',
            '381': 'Омск',
            '351': 'Челябинск',
            '863': 'Ростов-на-Дону',
            '844': 'Волгоград',
            '841': 'Пенза',
            '831': 'Нижний Новгород',
            '833': 'Киров',
            '835': 'Чебоксары',
            '836': 'Йошкар-Ола',
            '845': 'Саратов',
            '847': 'Ульяновск',
            '851': 'Астрахань',
            '855': 'Набережные Челны',
            '862': 'Сочи',
            '865': 'Ставрополь',
            '866': 'Нальчик',
            '867': 'Владикавказ',
            '871': 'Грозный',
            '872': 'Махачкала',
            '873': 'Черкесск',
            '877': 'Майкоп',
            '879': 'Пятигорск',
            '901': 'Москва',
            '902': 'Московская область',
            '903': 'Москва',
            '904': 'Московская область',
            '905': 'Москва',
            '906': 'Московская область',
            '909': 'Москва',
            '910': 'Московская область',
            '911': 'Санкт-Петербург',
            '912': 'Санкт-Петербург',
            '913': 'Санкт-Петербург',
            '914': 'Санкт-Петербург',
            '915': 'Санкт-Петербург',
            '916': 'Москва',
            '917': 'Москва',
            '918': 'Краснодар',
            '919': 'Москва',
            '920': 'Воронеж',
            '921': 'Санкт-Петербург',
            '922': 'Екатеринбург',
            '923': 'Красноярск',
            '924': 'Хабаровск',
            '925': 'Москва',
            '926': 'Москва',
            '927': 'Самара',
            '928': 'Краснодар',
            '929': 'Москва',
            '930': 'Москва',
            '931': 'Москва',
            '932': 'Московская область',
            '933': 'Москва',
            '934': 'Московская область',
            '936': 'Москва',
            '937': 'Московская область',
            '938': 'Краснодар',
            '939': 'Москва',
            '950': 'Санкт-Петербург',
            '951': 'Санкт-Петербург',
            '952': 'Санкт-Петербург',
            '953': 'Санкт-Петербург',
            '954': 'Санкт-Петербург',
            '955': 'Санкт-Петербург',
            '956': 'Санкт-Петербург',
            '958': 'Санкт-Петербург',
            '960': 'Краснодар',
            '961': 'Краснодар',
            '962': 'Краснодар',
            '963': 'Краснодар',
            '964': 'Краснодар',
            '965': 'Москва',
            '966': 'Москва',
            '967': 'Московская область',
            '968': 'Москва',
            '969': 'Москва',
            '980': 'Москва',
            '981': 'Санкт-Петербург',
            '982': 'Санкт-Петербург',
            '983': 'Санкт-Петербург',
            '984': 'Санкт-Петербург',
            '985': 'Москва',
            '986': 'Москва',
            '987': 'Казань',
            '988': 'Краснодар',
            '989': 'Москва',
            '977': 'Москва',
            '978': 'Крым',
            '979': 'Москва',
            '990': 'Москва',
            '991': 'Санкт-Петербург',
            '992': 'Екатеринбург',
            '993': 'Новосибирск',
            '994': 'Краснодар',
            '995': 'Москва',
            '996': 'Москва',
            '997': 'Москва',
            '998': 'Москва',
            '999': 'Москва'
        }
        return cities
        
    def parse_phone(self, phone_number):
        try:
            import phonenumbers
            from phonenumbers import carrier, geocoder, timezone
            
            parsed = phonenumbers.parse(phone_number, "RU")
            if not phonenumbers.is_valid_number(parsed):
                return None
                
            country = geocoder.country_name_for_number(parsed, "ru")
            operator = carrier.name_for_number(parsed, "ru")
            time_zones = timezone.time_zones_for_number(parsed)
            
            national_number = str(parsed.national_number)
            city = "Неизвестно"
            
            if len(national_number) >= 3:
                def_code = national_number[:3]
                if def_code in self.city_db:
                    city = self.city_db[def_code]
                else:
                    def_code_2 = national_number[:2]
                    if def_code_2 in self.city_db:
                        city = self.city_db[def_code_2]
            
            return {
                "valid": True,
                "country": country,
                "city": city,
                "operator": operator if operator else "Неизвестно",
                "timezone": list(time_zones)[0] if time_zones else "Неизвестно",
                "national_format": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                "international_format": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def check_whatsapp(self, phone_number):
        try:
            clean_number = re.sub(r'[^0-9+]', '', phone_number)
            if not clean_number.startswith('+'):
                clean_number = '+' + clean_number
            
            wa_link = f"https://wa.me/{clean_number}"
            
            url = f"https://api.whatsapp.com/phone/{clean_number}"
            response = self.session.get(url, allow_redirects=True, timeout=5)
            
            if "whatsapp" in response.url.lower() or response.status_code == 200:
                return {"exists": True, "url": wa_link}
            return {"exists": False, "url": wa_link}
        except:
            return {"exists": False, "url": None}
    
    def check_telegram(self, phone_number):
        try:
            clean_number = re.sub(r'[^0-9]', '', phone_number)
            
            tg_link = f"https://t.me/+{clean_number}"
            
            url = f"https://t.me/+{clean_number}"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                return {"exists": True, "url": tg_link}
            return {"exists": False, "url": tg_link}
        except:
            return {"exists": False, "url": None}
    
    def check_viber(self, phone_number):
        try:
            clean_number = re.sub(r'[^0-9]', '', phone_number)
            
            viber_link = f"viber://chat?number={clean_number}"
            
            url = f"https://chats.viber.com/{clean_number}"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                return {"exists": True, "url": viber_link}
            return {"exists": False, "url": viber_link}
        except:
            return {"exists": False, "url": None}

class TelegramSearch:
    def __init__(self):
        pass
        
    def search_by_username(self, username):
        results = {}
        try:
            url = f"https://t.me/{username}"
            response = requests.get(url)
            if response.status_code == 200:
                results['username'] = username
                results['url'] = url
                if "tgme_page" in response.text:
                    results['exists'] = True
                    if "tgme_page_title" in response.text:
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(response.text, 'html.parser')
                        title = soup.find('div', class_='tgme_page_title')
                        if title:
                            results['name'] = title.text.strip()
            else:
                results['exists'] = False
        except:
            results['exists'] = False
            results['error'] = "Ошибка проверки"
        return results
    
    def search_by_id(self, user_id):
        results = {}
        try:
            url = f"https://t.me/user/{user_id}"
            response = requests.get(url)
            if response.status_code == 200:
                results['id'] = user_id
                results['exists'] = True
            else:
                results['exists'] = False
        except:
            results['exists'] = False
            results['error'] = "Ошибка проверки"
        return results

def print_banner():
    banner = """
    \033[91m
      ___           ___           ___           ___     
     /  /\         /  /\         /  /\         /  /\    
    /  /::\       /  /::\       /  /::|       /  /:/_   
   /  /:/\:\     /  /:/\:\     /  /:/:|      /  /:/ /\  
  /  /:/~/:/    /  /:/~/::\   /  /:/|:|__   /  /:/ /:/_ 
 /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ |:| /\ /__/:/ /:/ /\\
 \  \:\/:::::/ \  \:\/:/__\/ \__\/  |:|/:/ \  \:\/:/ /:/
  \  \::/~~~~   \  \::/          |  |:/:/   \  \::/ /:/ 
   \  \:\        \  \:\          |  |::/     \  \:\/:/  
    \  \:\        \  \:\         |  |:/       \  \::/   
     \__\/         \__\/         |__|/         \__\/    
    \033[0m
    """
    print(banner)

def print_menu():
    print("\033[91m" + "="*50 + "\033[0m")
    print("\033[91m" + "          ПОИСКОВАЯ СИСТЕМА v2.0" + "\033[0m")
    print("\033[91m" + "="*50 + "\033[0m")
    print("\033[93m1.\033[0m Поиск по ФИО")
    print("\033[93m2.\033[0m Поиск по номеру телефона")
    print("\033[93m3.\033[0m Поиск в Telegram")
    print("\033[93m4.\033[0m Выход")
    print("\033[91m" + "="*50 + "\033[0m")

def print_result_header(title):
    print("\n\033[92m" + "="*50 + "\033[0m")
    print("\033[92m" + f"  {title}" + "\033[0m")
    print("\033[92m" + "="*50 + "\033[0m")

def print_result_item(label, value, color="93"):
    print(f"\033[{color}m{label}:\033[0m {value}")

def print_success(text):
    print(f"\033[92m[+] {text}\033[0m")

def print_error(text):
    print(f"\033[91m[-] {text}\033[0m")

def print_info(text):
    print(f"\033[94m[i] {text}\033[0m")

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def main_menu():
    clear_screen()
    print_banner()
    print_menu()
    
    choice = input("\n\033[93mВыберите опцию (1-4): \033[0m")
    
    if choice == "1":
        clear_screen()
        print_banner()
        print_result_header("ПОИСК ПО ФИО")
        
        fullname = input("\033[93mВведите полное ФИО (Фамилия Имя Отчество): \033[0m")
        birth_date = input("\033[93mВведите дату рождения (ДД.ММ.ГГГГ) или Enter для пропуска: \033[0m")
        
        searcher = PersonSearch()
        parsed = searcher.parse_fullname(fullname)
        
        print_result_header("РЕЗУЛЬТАТЫ РАЗБОРА")
        print_result_item("Фамилия", parsed['surname'])
        print_result_item("Имя", parsed['name'])
        print_result_item("Отчество", parsed['patronymic'])
        print_result_item("Пол", parsed['gender'])
        
        print_result_header("ПОИСК В СОЦИАЛЬНЫХ СЕТЯХ")
        
        vk_results = searcher.search_vk(parsed['surname'], parsed['name'])
        if vk_results:
            for res in vk_results:
                print_success(f"VK: {res['url']}")
        else:
            print_error("VK: Не найден")
        
        ok_results = searcher.search_ok(parsed['surname'], parsed['name'])
        if ok_results:
            for res in ok_results:
                print_success(f"Одноклассники: {res['url']}")
        else:
            print_error("Одноклассники: Не найден")
        
        if birth_date:
            print_result_header("ПРОВЕРКА СУДИМОСТИ")
            result = searcher.search_cases(
                parsed['surname'], 
                parsed['name'], 
                parsed['patronymic'], 
                birth_date
            )
            if result['has_criminal_record']:
                print_error(f"Судимость: {result['details']}")
            else:
                print_success(f"Судимость: {result['details']}")
        
        input("\n\033[93mНажмите Enter для продолжения...\033[0m")
        
    elif choice == "2":
        clear_screen()
        print_banner()
        print_result_header("ПОИСК ПО НОМЕРУ ТЕЛЕФОНА")
        
        phone = input("\033[93mВведите номер телефона (например, +79123456789): \033[0m")
        searcher = PhoneSearch()
        
        info = searcher.parse_phone(phone)
        if info and info.get('valid'):
            print_result_header("ИНФОРМАЦИЯ О НОМЕРЕ")
            print_result_item("Страна", info.get('country', 'Неизвестно'))
            print_result_item("Город", info.get('city', 'Неизвестно'))
            print_result_item("Оператор", info.get('operator', 'Неизвестно'))
            print_result_item("Часовой пояс", info.get('timezone', 'Неизвестно'))
            
            print_result_header("ПРОВЕРКА МЕССЕНДЖЕРОВ")
            
            wa = searcher.check_whatsapp(phone)
            if wa.get('exists'):
                print_success(f"WhatsApp: Найден - {wa.get('url')}")
            else:
                print_error("WhatsApp: Не найден")
            
            tg = searcher.check_telegram(phone)
            if tg.get('exists'):
                print_success(f"Telegram: Найден - {tg.get('url')}")
            else:
                print_error("Telegram: Не найден")
            
            vb = searcher.check_viber(phone)
            if vb.get('exists'):
                print_success(f"Viber: Найден - {vb.get('url')}")
            else:
                print_error("Viber: Не найден")
        else:
            print_error("Неверный номер телефона")
        
        input("\n\033[93mНажмите Enter для продолжения...\033[0m")
        
    elif choice == "3":
        clear_screen()
        print_banner()
        print_result_header("ПОИСК В TELEGRAM")
        
        print("\033[93m1.\033[0m Поиск по username")
        print("\033[93m2.\033[0m Поиск по ID")
        sub_choice = input("\033[93mВыберите опцию (1-2): \033[0m")
        
        searcher = TelegramSearch()
        
        if sub_choice == "1":
            username = input("\033[93mВведите username (без @): \033[0m")
            result = searcher.search_by_username(username)
            print_result_header("ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ")
            for key, value in result.items():
                if key == 'exists':
                    if value:
                        print_success(f"Существует: Да")
                    else:
                        print_error(f"Существует: Нет")
                else:
                    print_result_item(key, value)
                    
        elif sub_choice == "2":
            user_id = input("\033[93mВведите ID пользователя: \033[0m")
            result = searcher.search_by_id(user_id)
            print_result_header("ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ")
            for key, value in result.items():
                if key == 'exists':
                    if value:
                        print_success(f"Существует: Да")
                    else:
                        print_error(f"Существует: Нет")
                else:
                    print_result_item(key, value)
        
        input("\n\033[93mНажмите Enter для продолжения...\033[0m")
        
    elif choice == "4":
        clear_screen()
        print_banner()
        print("\033[91m" + "="*50 + "\033[0m")
        print("\033[91m" + "          ДО СВИДАНИЯ!" + "\033[0m")
        print("\033[91m" + "="*50 + "\033[0m")
        return False
    
    return True

if __name__ == "__main__":
    try:
        import requests
        import phonenumbers
    except ImportError:
        print("\033[93mУстанавливаю необходимые библиотеки...\033[0m")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "phonenumbers", "beautifulsoup4"])
        print("\033[92mУстановка завершена!\033[0m")
        
    while True:
        try:
            if not main_menu():
                break
        except KeyboardInterrupt:
            print("\n\033[91mВыход...\033[0m")
            break
        except Exception as e:
            print(f"\033[91mОшибка: {e}\033[0m")
            input("\033[93mНажмите Enter для продолжения...\033[0m")
