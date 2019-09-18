

import json;

names = {
    "Alex":"Alexey",
    "Vadik":"Vadim",
    "Вадик":"Вадим",
    "Nadya":"Nadezhda",
    "Vika":"Viktoriya",
    "Vasya":"Vasiliy",
    "Petya":"Petr",
    "Sasha":"Alexandr",
    "Nastya":"Anastasiya"
    }
with open("dic.txt", "w") as file:
    json.dump(names, file)
print ("file has been created")


