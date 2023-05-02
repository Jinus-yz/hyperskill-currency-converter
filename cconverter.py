import requests
import json


def get_cache():
    try:
        with open("rates.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_cache(next_cache):
    with open("rates.json", "w") as file:
        json.dump(next_cache, file)


rates = None


def get_rates(currency):
    global rates

    if rates is None:
        rates = requests.get(f"http://www.floatrates.com/daily/{currency.lower()}.json").json()

    return rates


currency_from = input()
cache = get_cache()

if cache.get(currency_from) is None:
    data = get_rates(currency_from)
    cache[currency_from] = {
        'USD': data.get("usd", {"rate": 0})["rate"],
        'EUR': data.get("eur", {"rate": 0})["rate"],
    }

    save_cache(cache)

while True:
    currency_to = input().upper()

    if currency_to == "":
        break

    amount = float(input())

    print("Checking the cache...")
    rate = cache[currency_from].get(currency_to)

    if rate is None:
        print("Sorry, but it is not in the cache!")

        data = get_rates(currency_from)
        rate = cache[currency_from][currency_to] = data.get(currency_to.lower(), {"rate": 0})["rate"]
        save_cache(cache)
    else:
        print("Oh! It is in the cache!")

    print(f"You received {round(amount * rate, 2)} {currency_to}.")
