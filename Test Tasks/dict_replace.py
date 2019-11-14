def repplace_keys_values(dic):
    new_dic={}
    for key, value in dic.items():
        try:
            new_dic[value] = key
        except TypeError:
            print("Imposible")
            return ''
    return new_dic


dic={
    1:'one',
    2:'two',
    3:'three'
}
print(repplace_keys_values(dic))
dic={
    1:'one',
    2:'two',
    3:['three']
}
print(repplace_keys_values(dic))