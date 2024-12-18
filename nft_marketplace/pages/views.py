import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template.defaultfilters import slugify
import json
from pydantic import ValidationError
from .models import NFTModel, NFTItemsModel, ONE_NFT_Item_Model, TopNFTCollectionSchema, TopNFTItemsSchema, \
    NFTItemsSchema_Profile_Items
from django.conf import settings
from django.shortcuts import render

def home_page_view(request):
    response_collections = requests.get(
        f"http://{settings.SERVER_IP}/content/api/v1/top/collections/?page=1&page_size=10")  # GET-запрос для коллекции
    # Проверка успешности запроса
    if response_collections.status_code == 200:
        data_collections = response_collections.json()  # Получаем JSON
        print(data_collections)  # Логируем данные для отладки
        try:
            collection_data = TopNFTCollectionSchema(**data_collections)
        except ValidationError as e:
            return HttpResponse(f"Ошибка валидации данных: {e}", status=400)
    else:
        return HttpResponse("Ошибка при запросе данных.", status=500)
    # _________________________________________________________________________________________________________________
    response_collections = requests.get(
        f"http://{settings.SERVER_IP}/content/api/v1/top/nfts/?page=1&page_size=10")  # GET-запрос для коллекции
    # Проверка успешности запроса
    if response_collections.status_code == 200:
        data_items = response_collections.json()  # Получаем JSON
        print(data_items)  # Логируем данные для отладки
        try:
            nfts_data = TopNFTItemsSchema(**data_items)
        except ValidationError as e:
            return HttpResponse(f"Ошибка валидации данных: {e}", status=400)
    else:
        return HttpResponse("Ошибка при запросе данных.", status=500)

    # return render(request, "home/home.html", {'title': 'NFT Marketplace on TON'}) #ГОООООООООООООООООООООООООООООООООООООООООООООЛЛЛЛЛЛЛЛЛЛЛЛЛЛЛ
    return render(request, "home/home.html", {
        "top_collections": collection_data,
        "title": 'NFT Marketplace on TON',
        "top_nfts": nfts_data,
        # "user_address": address,
        # "mod_owner_address": mod_owner_address,
    })



def about_us(request):
    data = {
    }
    return render(request, "about_us/about_us.html", context=data)


# общая страница маркетплейса с подборками
def collections(request):
    return render(request, "collections/collections.html", {'title': 'Collections'})


# страница для конкретных коллекций
def collections_items(request, collection_address):
    response_collections = requests.get(
        f"http://{settings.SERVER_IP}/content/api/v1/nfts/collections/{collection_address}")  # GET-запрос для коллекции
    # Проверка успешности запроса
    if response_collections.status_code == 200:
        data = response_collections.json()  # Получаем JSON
        title = data.get("metadata", {}).get("name", "Default Title")
        print(data)
        try:
            nft_data = NFTModel(**data)  # Валидируем все через модель
        except ValidationError as e:
            return HttpResponse(f"Ошибка валидации данных: {e}", status=400)
    else:
        return HttpResponse("Ошибка при запросе данных.", status=500)

    # Создание GET-запроса для итемов коллекции
    response_items_collections = requests.get(
        f"http://{settings.SERVER_IP}/content/api/v1/nfts/collections/{collection_address}/items")
    if response_items_collections.status_code == 200:
        nfts_data = response_items_collections.json()
        try:
            nft_item_data = NFTItemsModel(**nfts_data)
            valid_nfts_data = json.loads(nft_item_data.json())
        except ValidationError as e:
            return HttpResponse(f"Ошибка валидации данных: {e}", status=400)
    else:
        return HttpResponse("Ошибка при запросе данных.", status=500)

    address = (request.COOKIES.get('address_wallet', 'Address not set')).replace("+", "-")
    mod_owner_address = data['owner_address'].replace("+", "-")

    return render(request, "collections/collection_items.html", {
        "data": nft_data,
        "title": title,
        "nfts": valid_nfts_data,
        "user_address": address,
        "mod_owner_address": mod_owner_address,
    })


# страница для одиночных NFT
def nft_item(request, nft_item_address, collection_address):  # принимаю нфтишки
    response = requests.get(f"http://{settings.SERVER_IP}/content/api/v1/nfts/{nft_item_address}")
    if response.status_code == 200:
        data_one = response.json()
        title = data_one.get("metadata", {}).get("name", "Default Title")
        try:
            nft_data_one = ONE_NFT_Item_Model(**data_one)
        except ValidationError as e:
            return HttpResponse(f"Ошибка валидации данных: {e}", status=400)
    else:
        return HttpResponse("Ошибка при запросе данных.", status=500)

    address = (request.COOKIES.get('address_wallet', 'Address not set')).replace("+", "-")
    mod_owner_address = data_one['owner_address'].replace("+", "-")
    return render(request, "NFT/nft_item.html",
                  {"data": data_one,
                   'title': title,
                   'nft_item_address': nft_item_address,
                   "user_address": address,
                   "mod_owner_address": mod_owner_address,
                   },
                  )


def feedback(request):
    return render(request, "feedback/feedback.html", {'title': 'Feedback'})


def profile(request, address):
    # получение итемов пол
    response = requests.get(f"http://{settings.SERVER_IP}/content/api/v1/accounts/{address}/items")
    if response.status_code == 200:
        data_one = response.json()
        title = data_one.get("metadata", {}).get("name", "Default Title")
    #     try:
    #         nft_data_one = UserActivity(**data_one)
    #         print(nft_data_one)
    #     except ValidationError as e:
    #         return HttpResponse(f"Ошибка валидации данных: {e}", status=400)
    # else:
    #     return HttpResponse("Ошибка при запросе данных.", status=500)

    # Извлечение значений из куки
    # address = request.COOKIES.get('address_wallet', 'Address not set')
    session_id = request.COOKIES.get('session_id', 'Session ID not set')

    response_collections = requests.get(
        f"http://{settings.SERVER_IP}/content/api/v1/accounts/{address}/items")  # GET-запрос для коллекции
    # Проверка успешности запроса
    if response_collections.status_code == 200:
        data_items = response_collections.json()  # Получаем JSON
        print(data_items)  # Логируем данные для отладки
        try:
            data_items_profile = NFTItemsSchema_Profile_Items(**data_items)
        except ValidationError as e:
            return HttpResponse(f"Ошибка валидации данных: {e}", status=400)
    else:
        return HttpResponse("Ошибка при запросе данных.", status=500)

    return render(request, 'profile/profile.html', {'address': address,
                                                    'session_id': session_id,
                                                    'title': 'Profile',
                                                    'data': data_items_profile})


def mint_collection(request):
    return render(request, "collections/mint_collections.html", {'title': 'Mint NFT collection'})


def mint_nft(request, collection_address):
    print(collection_address)
    return render(request, "NFT/mint_nft.html", {'title': 'Mint NFT',
                                                 'collection_address': collection_address})


def sell_nft(request, nft_item_address):
    return render(request, "NFT/sell_nft.html", {'title': 'Sell NFT',
                                                 'nft_item_address': nft_item_address})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
