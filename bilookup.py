def __create_random_ip_list(list_length=10000, for_creating_tries=True):
    # creating set of ips for creating/searching tries.
    import random

    if for_creating_tries:
        with open('db.txt', 'w') as f:
            for i in range(1, list_length):
                ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0, 255), 4))
                mask = str(random.choice([8, 12, 16, 24, 28]))
                f.write(ip + "\\" + mask + "," + getMaskBin(ip)[:int(mask)] + "\n")
    else:  # else it means that it is for searching
        with open('to_search.txt', 'w') as f:
            for i in range(1, list_length):
                ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0, 255), 4))
                mask = str(random.choice([8, 12, 16, 24, 28]))
                f.write(ip + "\\" + mask + "," + getMaskBin(ip)[:mask] + "\n")