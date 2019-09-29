import json


def main():
    name=[]
    while len(name) != 2:  #не успокоимся, пока не введутся 2 и только 2 слова разделенные пробелом
        input_name = input("First and second name: ")
        input_name = ' '.join(input_name.split()) #отбрасываем все лишнее
        name = input_name.split(" ")  #пилим на слова
       


    try:
        with open("dic.txt", "r") as file:
            names=json.load(file)  #читаем словарь 
    except FileNotFoundError:
        print("File Dic is not found, sorry!")
        names=[]
    except:
        print("Some other error occurred!")

    
    f_name = name[0].title()
    s_name = name[1].title()
    for i in names:
        if f_name == i: #если имя нашлось меняем его на полное из словаря
            f_name = names[i]
   

    print("Hello, {} {}!".format(f_name,s_name))




if __name__ == "__main__":
    main()









