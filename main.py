import json

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
        self.ip = str(ipaddress.IPv4Address(ip))  # str(IPv4Address)

    def toString(self):
        return "name " + self.name + ", ip " + self.ip


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


@app.get("/")
def root():
    return FileResponse("public/index.html")


@app.put("/update_device", status_code=status.HTTP_201_CREATED)
def update_device(data=Body()):
    # получаем IP адрес виртуального канала по id
    device = find_device(data["vl_ip"])

    # если не найдено, отправляем статусный код и сообщение об ошибке
    if device == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Упс, устройство не найдено"}
        )

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


@app.get("/device/{ip}")
def get_device(ip):
    # получаем устройство по ip
    device = find_device(ip)
    # если устройство не найдено, отправляем статусный код и сообщение об ошибке
    if device == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Упс, устройство не найдено"}
        )
    # если устройство найдено, отправляем его
    return device

@app.get("/alldevices")
def get_alldevices():
    return machine