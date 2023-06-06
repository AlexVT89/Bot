import requests
import config
API_TOKEN = config.API_TOKEN

#Поиск в два пути
def api_response_2way(origin,destination,departure,return_):
    def response_iata(airo_city):
        iata=requests.get(f"https://autocomplete.travelpayouts.com/places2?locale=ru&types[]=airport&types[]=city&term={airo_city}").json()
        return (iata[0]['code'],iata[0]['name'])
    list_ticket=[]
    try:
        response = requests.get(f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={response_iata(origin)[0]}&"
                                f"destination={response_iata(destination)[0]}&currency=rub&departure_at={departure}&return_at={return_}&"
                                f"sorting=price&limit=15&token={API_TOKEN}",headers={"Accept-Encoding": "gzip"})
        for i in response.json()["data"]:
            list_ticket.append([f"Вылет из аэропорта: {response_iata(i['origin_airport'])[1]}\nДата вылета: {i['departure_at'][:10]}\nВремя вылета: {i['departure_at'][11:19]}\nВремя полета: {i['duration_to']}мин.\n"
                            f"Прилет в аэропорт: {response_iata(i['destination_airport'])[1]}\nДата обратного вылета: {i['return_at'][:10]}\nВремя обратного вылета: {i['return_at'][11:19]}\nВремя полета: {i['duration_back']}мин.\n"
                            f"Цена: {i['price']}руб.",i['link']])
        return list_ticket
    except:
        return list_ticket
    
#Поиск в один путь
def api_response_1way(origin,destination,departure):
    def response_iata(airo_city):
        iata=requests.get(f"https://autocomplete.travelpayouts.com/places2?locale=ru&types[]=airport&types[]=city&term={airo_city}").json()
        return (iata[0]['code'],iata[0]['name'])
    list_ticket=[]
    try:
        response = requests.get(f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={response_iata(origin)[0]}&"
                                f"destination={response_iata(destination)[0]}&currency=rub&departure_at={departure}&one_way=false&return_at=&sorting=price&"
                                f"limit=15&token={API_TOKEN}",headers={"Accept-Encoding": "gzip"})
        for i in response.json()["data"]:
            list_ticket.append([f"Вылет из аэропорта: {response_iata(i['origin_airport'])[1]}\nДата вылета: {i['departure_at'][:10]}\nВремя вылета: {i['departure_at'][11:19]}\nВремя полета: {i['duration_to']}мин.\n"
                            f"Прилет в аэропорт: {response_iata(i['destination_airport'])[1]}\n"
                            f"Цена: {i['price']}руб.",i['link']])
        return list_ticket
    except:
        return list_ticket