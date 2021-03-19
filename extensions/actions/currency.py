import requests


def get_rate():
    """Получения актуального курса по Кронам, Евро и Рублям в отношении к одному доллару"""

    try:
        response = requests.get('https://api.exchangeratesapi.io/latest?symbols=EUR,RUB,CZK&base=USD').json()
    except Exception as e:
        raise e
    else:
        rates = response['rates']
        return "Текущий курс к одному доллару составляет:\nRUB: {rub}\nCZK: {czk}\nEUR: {eur}".format(
                eur=round(rates['EUR'], 2), rub=round(rates['RUB'], 2), czk=round(rates['CZK'], 2)
            )
