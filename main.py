from fastapi import FastAPI, status, Body, Form
import uuid
from fastapi.responses import JSONResponse, FileResponse
from ipaddress import IPv4Address


import ipaddress
# # для IP4-адреса
# ipAddr = ipaddress.IPv4Address(address)


# Класс device дает общую характеристику реализующих его объектов machine
class Device:
    def __init__(self, name, ip):
        self.name = name
        self.ip = str(ipaddress.IPv4Address(ip))  #str(IPv4Address)

# условная база данных - набор объектов класса Device
machine = [Device("CCP1", "192.168.1.102"), Device("CCP2", "192.168.1.103"),
           Device("CCP3", "192.168.1.104"),
           Device("CP1A", "192.168.1.105"), Device("CP2A", "192.168.1.106"),
           Device("CP1B", "192.168.1.107"), Device("CP2B", "192.168.1.108"),
           Device("CP1C", "192.168.1.109"), Device("CP2C", "192.168.1.110"),
           Device("DUCD", "192.168.1.111"), Device("DUIL", "192.168.1.112"),
           Device("DUIR", "192.168.1.113"), Device("DUOL", "192.168.1.114"),
           Device("DUOR", "192.168.1.115"), Device("FDMU", "192.168.1.116"),
           Device("FWL1", "192.168.1.117"), Device("FWL2", "192.168.1.118"),
           Device("SDBLA", "192.168.1.119"), Device("SDBLB", "192.168.1.120"),
           Device("SDBRA", "192.168.1.121"), Device("SDBRB", "192.168.1.122"),
           Device("FTI1", "192.168.1.123")]

# для поиска устройства в списке machine
def find_device(ip):
    for device in machine:
        if device.ip == ip:
            return device
    return None



app = FastAPI()

# При обращении к корню веб-приложения, то есть по пути "/",
# оно будет отправлять в ответ файл index.html, то есть веб-страницу,
# посредством которой пользователь сможет взаимодействовать с сервером:
@app.get("/")
def root():
    return FileResponse("public/index.html")

# # Для обработки полученных в POST-запросе данных по адресу "/hello" определена функция hello().
# # Эта функция имеет один параметр - data, который получает содержимое тела запроса:
# @app.post("/hello")
# def hello(data = Body()):
#     name = data["name"]
#     age = data["age"]
#     return {"message": f"{name}, ваш возраст - {age}"}
# # То есть здесь data будет представлять весь объект, который отправляется с веб-страницы и который
# # имеет свойства "name" и "age". Этот объект в python будет представлять словарь. Соответственно, чтобы получить
# # значения свойства "name", обращаемся по одноименному ключу: name = data["name"]


# В функции add_vl, которая обрабатывает запрос по одноименному пути, через параметры получаем
# отправленные данные. Причем параметры называются также, как и атрибуты name у полей формы.
# А самим параметрам присваивается объект Form.
@app.post("/add_vl", status_code=status.HTTP_201_CREATED)
def add_vl(vl_name=Form(), vl_ip=Form()):
    return {"vl_name": vl_name, "vl_ip": vl_ip}

# status_code является атрибутом метода-декоратора (get, post и т.д.),
# а не функции-обработчика пути в отличие от всех остальных параметров и тела запроса.


# кнопка удаления последней строки таблицы - Delete VL
@app.post("/delete_vl", status_code=status.HTTP_200_OK)
def delete_last_vl(ip):
    # получаем IP адрес виртуального канала по id
    device = find_device(ip)

    # если не найдено, отправляем статусный код и сообщение об ошибке
    if device == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Упс, устройство не найдено"}
        )

    # если устройство найдено, удаляем его
    machine.remove(device)
    return device



# Извлечь переменные пути из маршрута, определим их при объявлении маршрута, а затем передадим их в функцию маршрута.
@app.get("/all_list/{ip_vl}")
async def ip_ping(ip_vl: str):
    return {"ip_vl":ip_vl}



@app.get("/device/{ip}")
def get_device(ip):
    # получаем устройство по ip
    device = find_device(ip)
    print(device)
    # если устройство не найдено, отправляем статусный код и сообщение об ошибке
    if device == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Упс, устройство не найдено"}
        )
    # если устройство найдено, отправляем его
    return device