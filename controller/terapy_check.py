import datetime

def check_conflict(client, doctor, current_date, data):
    print(f"cliente: {client}")
    print(f"terapeuta: {doctor}")
    for element in data:
        if element[1] == client or element[2] == doctor:
            print("client or doctor found")
            if element[3].year == current_date.year:
                if element[3].month == current_date.month:
                    if element[3].day == current_date.day:
                        if current_date.hour >= element[3].hour and current_date.hour <= element[5].hour:
                            print("True")
                            return True
        else:
            print("False")
            return False
                

