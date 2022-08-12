from datetime import date
def get_y(dob):
    _y = dob[:4]
    _m = dob[5:7]
    _d = dob[8:]

    cur = str(date.today())
    c_y = cur[:4]
    c_m = cur[5:7]
    c_d = cur[8:]
    
    dif_y = int(c_y) - int(_y)
    dif_m = int(c_m) - int(_m)
    dif_d = int(c_d) - int(_d)

    if dif_m < 0:
        dif_y -= 1
    elif dif_m == 0 and dif_d < 0:
        dif_y -=1
         
    print(dif_y)

get_y("2020-08-02")