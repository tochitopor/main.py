import json

from fastapi import FastAPI, status, Body, Form
import uuid
from fastapi.responses import JSONResponse, FileResponse
from ipaddress import IPv4Address

import ipaddress
import uvicorn


# # для IP4-адреса
# ipAddr = ipaddress.IPv4Address(address)

# переменные self.name, self.ip являются переменными экземпляра.
# они определяются внутри метода init.
# В Python этот специальный метод выполняется автоматически каждый раз, когда создается новый объект из своего класса.
# Поэтому нужно вложить все, что свойственно объекту, который создается.

# В конструкторе класса device дается общая характеристика реализующих его объектов machine
class Device:
    def __init__(self, name, ip):
        self.name = name
        self.ip = str(ipaddress.IPv4Address(ip))  # str(IPv4Address)

    # def toString(self):
    #     return "name " + self.name + ", ip " + self.ip

# условная база данных - набор объектов класса Device
machine = [Device("CCP1", "192.168.1.102"), Device("CCP2", "192.168.1.103"),
           Device("CCP3", "192.168.1.104"),
           Device("CP1A", "192.168.1.105"), Device("CP2A", "192.168.1.106"),
           Device("CP1B", "192.168.1.107"), Device("CP2B", "192.168.1.108")]


# функция для поиска устройства в списке machine
def find_device(ip):
    for device in machine:
        if device.ip == ip:
            return device
    return None


# функция для вывода повторяющегося сообщения "устройство не найдено"
def NoneDevice(device):
    # если не найдено, отправляем статусный код и сообщение об ошибке
    if device == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Упс, устройство не найдено"}
        )


app = FastAPI()


@app.get("/")
def root():
    return FileResponse("public/index.html")


# Иногда возникает необходимость вручную сгенерировать то или иное исключение. Для этого применяется оператор raise.
# Оператору raise передается объект BaseException - в данном случае объект Exception.
# В конструктор этого типа можно ему передать сообщение, которое затем можно вывести пользователю.
# В итоге, если устройство не найдено по ip/названию, то сработает оператор raise, который сгенерирует исключение.
# Управление программой перейдет к блоку except, который обрабатывает исключения типа Exception:

@app.put("/update_device", status_code=status.HTTP_201_CREATED)
def update_device(data=Body()):
    # получаем IP адрес виртуального канала по id
    try:
        device = find_device(data["vl_ip"])
        if device == None:
            raise Exception("ошибка")
    except Exception:
        device = NoneDevice(device)

    # # если не найдено, отправляем статусный код и сообщение об ошибке
    # if device == None:
    #     return JSONResponse(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         content={"message": "Упс, устройство не найдено"}
    #     )

    # если устройство найдено, удаляем его добавляем новое
    machine.remove(device)
    updateDevice = Device(data["vl_name"], data["vl_ip"])
    machine.append(updateDevice)
    return updateDevice


@app.post("/add_device", status_code=status.HTTP_201_CREATED)
def add_device(data=Body()):
    postDevice = Device(data["vl_name"], data["vl_ip"])
    machine.append(postDevice)
    return postDevice


# кнопка удаления по ip
@app.delete("/delete_device/{ip}", status_code=status.HTTP_200_OK)
def delete_device(ip):
    # получаем IP адрес виртуального канала по id
    try:
        device = find_device(ip)
        if device == None:
            raise Exception()
    except Exception:
        device = NoneDevice(device)

    # # если не найдено, отправляем статусный код и сообщение об ошибке
    # if device == None:
    #     return JSONResponse(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         content={"message": "Упс, устройство не найдено"}
    #     )

    # если устройство найдено, удаляем его
    machine.remove(device)
    return device


@app.get("/device/{ip}")
def get_device(ip):
    # получаем устройство по ip
    try:
        device = find_device(ip)
        if device == None:
            raise Exception()
    except Exception:
        device = NoneDevice(device)

    # # если устройство не найдено, отправляем статусный код и сообщение об ошибке
    # if device == None:
    #     return JSONResponse(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         content={"message": "Упс, устройство не найдено"}
    #     )
    # если устройство найдено, отправляем его
    return device

@app.get("/alldevices")
def get_alldevices():
    return machine


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)