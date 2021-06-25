from datetime import datetime

def check_conflict(data, fecha_ini, h1, cliente, terapeuta ):
    for element in data:
        date = element[3].strftime('%Y-%m-%d')
        if date == fecha_ini:
            hour_one = element[3].hour
            hour_two = element[5].hour
            if element[1] == int(cliente) or element[2] == int(terapeuta):
                if h1 >= 19 or h1 <= 7:
                    return True
                elif h1 >= hour_one and h1 <= hour_two:
                    return True
                else:
                    return False
