a = ['192.168.1.10', '192.168.1.2']
print(list(map(lambda address: {"address": address, "id": ""}, list(a))))