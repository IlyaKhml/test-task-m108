import requests

def fetch_data_from_api(url: str) -> dict:
    """
    Send a GET request to a given URL and return the response as a dictionary.

    Parameters
    ----------
    url : str
        The URL to send the GET request to.

    Returns
    -------
    dict or None
        If the request was successful, the response as a dictionary. Otherwise None.
    """
    try:
        # Отправка GET-запроса
        response = requests.get(url)

        # Проверка статуса ответа
        response.raise_for_status()

        # Преобразование ответа в JSON (словарь)
        data = response.json()
        return data

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None


def get_final_dict(data: list) -> dict:
    """
    Process a list of data dictionaries to extract and return a final dictionary
    containing specific metadata and achievements.

    Parameters
    ----------
    data : list of dict
        A list of data dictionaries, each having keys that map to individual
        dictionaries containing 'metadata' and 'achievements'.

    Returns
    -------
    dict
        A dictionary where each key corresponds to a key in the input data
        dictionaries and the value is a dictionary including 'metadata' and 
        'achievements'. The 'achievements' include only those present in the 
        second data dictionary but not in the first.
    """
    final_dict = dict()

    for data_key in data[0].keys():
        data_dict_1 = data[0][data_key]
        data_dict_2 = data[1][data_key]

        temp_dict = dict()

        # Добавляем метаданные
        temp_dict['metadata'] = data_dict_1['metadata']

        # Находим множества достижений
        achivements_set_1 = set(data_dict_1['achievements'].keys())
        achivements_set_2 = set(data_dict_2['achievements'].keys())

        # Получаем только те достижения, которые появились в ответе второго запроса, но отсутствовали в первом.
        final_achivements = achivements_set_2 - achivements_set_1
        final_achivements.discard(achivements_set_2 & achivements_set_1)

        # Добавляем во временный словарь только нужные пары ключ-значение
        temp_dict['achievements'] = {key:val for key, val in data_dict_2['achievements'].items() if key in final_achivements}

        final_dict[data_key] = temp_dict
    
    return final_dict

if __name__ == "__main__":
    url = "https://base.media108.ru/training/sample/"

    # Список для хранения данных с сайта
    data = []

    for i in range(2):
        data.append(fetch_data_from_api(url))

    final_dict = get_final_dict(data)

    print(final_dict)
