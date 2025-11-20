import data
import sys
import io

'''
def leap_year(year)
def Solar_terms(year,month,day)
def day_year(year,month,day)
def day_between_year(year)
def get_jiazi(year, month, day)
def day_p(year,month,day)
def find_futou(year,month,day)
def get_sanyuan(futou_ganzhi)
def get_jushu(solar_term, current_date)
def days_between_dates(year1, month1, day1, year2, month2, day2)
def get_previous_solar_term(current_solar_term)
def check_chaoshen_jieqi(solar_term_date, futou_date, solar_term, jushu)
def get_jushu(year, month, day)
'''

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def leap_year(year):
    if((year%4==0 and year%100!=0) or year%400==0):
        return 1
    else:
        return 0

def Solar_terms(year,month,day):
    month_const=data.TERM_CONST[month]
    
    if(1900<=year<2000):
        year_const1=month_const[0][0]
        year_const2=month_const[1][0]
        term_date1=int(year_const1 + 0.2422 * (year - 1900) - int((year - 1900)/4))
        term_date2=int(year_const2 + 0.2422 * (year - 1900) - int((year - 1900)/4))
    elif(2000<=year<2100):
        year_const1=month_const[0][1]
        year_const2=month_const[1][1]
        term_date1=int(year_const1 + 0.2422 * (year - 2000) - int((year - 2000)/4))
        term_date2=int(year_const2 + 0.2422 * (year - 2000) - int((year - 2000)/4))
    elif(2100<=2200):
        year_const1=month_const[0][2]
        year_const2=month_const[1][2]
        term_date1=int(year_const1 + 0.2422 * (year - 2100) - int((year - 2100)/4))
        term_date2=int(year_const2 + 0.2422 * (year - 2100) - int((year - 2100)/4))
    
    if(term_date1<=day<term_date2):
        return month_const[0][-1],day-term_date1,[year,month,term_date1]
    elif(day>=term_date2):
        return month_const[1][-1],day-term_date2,[year,month,term_date2]
    else:
        if(month==1):
            month_p=12
            month_const=data.TERM_CONST[month_p]
            year_p=year-1
            if(1900<=year_p<2000):
                year_const2=month_const[1][0]
                term_date2=int(year_const2 + 0.2422 * (year_p - 1900) - int((year_p - 1900)/4))
            elif(2000<=year_p<2100):
                year_const2=month_const[1][1]
                term_date2=int(year_const2 + 0.2422 * (year_p - 2000) - int((year_p - 2000)/4))
            elif(2100<=year_p<2200):
                year_const2=month_const[1][2]
                term_date2=int(year_const2 + 0.2422 * (year_p - 2100) - int((year_p - 2100)/4))
            return month_const[1][-1],day+data.MONTH_DAYS[month_p]-term_date2,[year-1,month_p,term_date2]
        elif(month==3):
            month_p=2
            month_const=data.TERM_CONST[month_p]
            if(1900<=year<2000):
                year_const2=month_const[1][0]
                term_date2=int(year_const2 + 0.2422 * (year - 1900) - int((year - 1900)/4))
            elif(2000<=year<2100):
                year_const2=month_const[1][1]
                term_date2=int(year_const2 + 0.2422 * (year - 2000) - int((year - 2000)/4))
            elif(2100<=2200):
                year_const2=month_const[1][2]
                term_date2=int(year_const2 + 0.2422 * (year - 2100) - int((year - 2100)/4))
            
            if(leap_year(year)==1):
                return month_const[1][-1],day+data.MONTH_DAYS[month_p]+1-term_date2,[year,month_p,term_date2]
            else:
                return month_const[1][-1],day+data.MONTH_DAYS[month_p]-term_date2,[year,month_p,term_date2]
        else:
            month_p=month-1
            month_const=data.TERM_CONST[month_p]
            if(1900<=year<2000):
                year_const2=month_const[1][0]
                term_date2=int(year_const2 + 0.2422 * (year - 1900) - int((year - 1900)/4))
            elif(2000<=year<2100):
                year_const2=month_const[1][1]
                term_date2=int(year_const2 + 0.2422 * (year - 2000) - int((year - 2000)/4))
            elif(2100<=2200):
                year_const2=month_const[1][2]
                term_date2=int(year_const2 + 0.2422 * (year - 2100) - int((year - 2100)/4))
                
            return month_const[1][-1],day+data.MONTH_DAYS[month_p]-term_date2,[year,month_p,term_date2]
        
def day_year(year,month,day):
    days=day
    for i in range(1,month):
        days=days+data.MONTH_DAYS[i]
    if(month>2 and leap_year(year)):
        days=days+1
    return days

def day_between_year(year):
    days=0
    for i in range(1900,year):
        if(leap_year(i)):
            days=days+366
        else:
            days=days+365
    return days

def get_jiazi(year, month, day):
    days = day_year(year, month, day) + day_between_year(year)
    index = (days+10) % 60
    if index == 0:
        index = 60
    return data.jiazi_list[index-1]

def day_p(year,month,day):
    if(day>1):
        return [year,month,day-1]
    else:
        if(month>3 or month==2):
            return [year,month-1,data.MONTH_DAYS[month-1]]
        elif(month==3):
            if(leap_year(year)==1):
                return [year,2,data.MONTH_DAYS[2]+1]
            else:
                return [year,2,data.MONTH_DAYS[2]]
        else:
            return[year-1,12,31]

def find_futou(year,month,day):
    current_ganzhi = get_jiazi(year,month,day)
    if current_ganzhi[0] in ['甲', '己']:
        return [year,month,day], current_ganzhi
    futou_date = [year,month,day]
    while True:
        futou_date = day_p(futou_date[0],futou_date[1],futou_date[2])
        futou_ganzhi = get_jiazi(futou_date[0],futou_date[1],futou_date[2])
        if futou_ganzhi[0] in ['甲', '己']:
            return futou_date, futou_ganzhi

def get_sanyuan(futou_ganzhi):
    dizhi = futou_ganzhi[1]
    if (dizhi in ['子', '午', '卯', '酉']):
        return "上元"
    elif (dizhi in ['寅', '申', '巳', '亥']):
        return "中元"
    else:
        return "下元"

def days_between_dates(year1, month1, day1, year2, month2, day2):
    if (year1, month1, day1) > (year2, month2, day2):
        year1, month1, day1, year2, month2, day2 = year2, month2, day2, year1, month1, day1
    total_days = 0
    if year1 == year2 and month1 == month2:
        return day2 - day1
    if year1 == year2:
        if month1 == 2 and leap_year(year1):
            total_days += data.MONTH_DAYS[month1]+1 - day1
        else:
            total_days += data.MONTH_DAYS[month1] - day1
        for month in range(month1 + 1, month2):
            if month == 2 and leap_year(year1):
                total_days += data.MONTH_DAYS[month]+1
            else:
                total_days += data.MONTH_DAYS[month]
        total_days += day2
        return total_days
    if month1 == 2 and leap_year(year1):
        total_days += data.MONTH_DAYS[month]+1 - day1
    else:
        total_days += data.MONTH_DAYS[month1] - day1
    for month in range(month1 + 1, 13):
        if month == 2 and leap_year(year1):
            total_days += data.MONTH_DAYS[month]+1
        else:
            total_days += data.MONTH_DAYS[month]
    for year in range(year1 + 1, year2):
        if leap_year(year):
            total_days += 366
        else:
            total_days += 365
    for month in range(1, month2):
        if month == 2 and leap_year(year2):
            total_days += data.MONTH_DAYS[month]+1
        else:
            total_days += data.MONTH_DAYS[month]
    
    total_days += day2
    return total_days

def get_previous_solar_term(current_solar_term):
    current_index = data.solar_terms.index(current_solar_term)
    prev_index = (current_index - 1) % len(data.solar_terms)
    return data.solar_terms[prev_index]

def check_chaoshen_jieqi(solar_term_date, futou_date, solar_term, jushu):
    days_diff = days_between_dates(
        futou_date[0], futou_date[1], futou_date[2],
        solar_term_date[0], solar_term_date[1], solar_term_date[2]
    )
    
    if days_diff > 0:
        # 超神超过9天需要置润
        if days_diff > 9 and solar_term in ["芒种", "大雪"]:
            # 置润时使用上一个节气的局数
            prev_term = get_previous_solar_term(solar_term)
            prev_jushu = data.ju_table_base.get(prev_term, 1)  # 获取上一个节气的局数
            return prev_jushu
        else:
            return jushu
    elif days_diff < 0:
        return jushu
    else:
        return jushu
    
def get_jushu(year, month, day):
    solar_term_name, days_after, solar_term_date = Solar_terms(year, month, day)
    if solar_term_name in data.yang_dun:
        yinyang='阳'
        ju_table = data.yang_ju
    else:
        ju_table = data.yin_ju
        yinyang='阴'
    futou_date, futou_ganzhi = find_futou(year, month, day)
    sanyuan = get_sanyuan(futou_ganzhi)
    base_jushu = ju_table.get(solar_term_name, {}).get(sanyuan, 1)
    final_jushu = check_chaoshen_jieqi(solar_term_date, futou_date, solar_term_name, base_jushu)
    return yinyang,final_jushu

def get_hour_ganzhi(day_ganzhi, hour):
    day_gan = day_ganzhi[0]
    hour_branch = data.hour_to_branch[hour]
    branch_index = data.di_zhi.index(hour_branch)
    zi_gan = data.wushudun[day_gan]
    zi_gan_index = data.tian_gan.index(zi_gan)
    hour_gan_index = (zi_gan_index + branch_index) % 10
    hour_gan = data.tian_gan[hour_gan_index]
    return hour_gan + hour_branch

def get_xunshou(hour_ganzhi):
    current_index = data.jiazi_list.index(hour_ganzhi)
    for i in range(current_index, -1, -1):
        if data.jiazi_list[i] in data.xunshou_list:
            return data.jiazi_list[i]
    for i in range(len(data.jiazi_list)-1, current_index, -1):
        if data.jiazi_list[i] in data.xunshou_list:
            return data.jiazi_list[i]
    return '甲子'

def determine_zhifu(xunshou, earth_plate):
    liuyi = data.xunshou_to_liuyi[xunshou]
    position = None
    
    for pos, value in earth_plate.items():
        if value == liuyi:
            position = pos
            break
    return data.jiugong_to_star[position]

def arrange_earth_plate(ju_number, yinyang):
    earth_plate_dict = {}
    start_index = ju_number - 1
    if yinyang == "阳":
        for i, gong in enumerate(data.jiugong[:-1]):
            star_index = (start_index + i) % 8
            earth_plate_dict[gong] = data.qiyi[star_index]
    else:
        for i, gong in enumerate(data.jiugong[:-1]):
            star_index = (start_index - i) % 8
            earth_plate_dict[gong] = data.qiyi[star_index]
    earth_plate_dict[data.jiugong[8]] = data.qiyi[ju_number - 1]
    
    return earth_plate_dict

def arrange_heaven_plate(earth_plate, shifu, hour_gan):
    shifu_position = None
    for pos, star in earth_plate.items():
        if star == shifu:
            shifu_position = pos
            break
    target_position = data.gan_to_jiugong.get(hour_gan)
    start_index = data.jiugong.index(shifu_position)
    target_index = data.jiugong.index(target_position)
    offset = (target_index - start_index) % 9
    heaven_plate = {}
    for i, pos in enumerate(data.jiugong):
        new_star_index = (i - offset) % 9
        heaven_plate[pos] = data.stars[new_star_index]
    return heaven_plate

def arrange_human_plate(xunshou, hour_zhi):
    zhishi_gate = data.xunshou_to_zhishi.get(xunshou)
    zhishi_index = data.gates.index(zhishi_gate)
    target_position = data.zhi_to_jiugong.get(hour_zhi)
    target_index = data.jiugong.index(target_position)
    offset = (target_index - zhishi_index) % 9
    human_plate = {}
    for i, pos in enumerate(data.jiugong):
        new_gate_index = (i - offset) % 9
        human_plate[pos] = data.gates[new_gate_index]
    return human_plate

def arrange_god_plate(yinyang, zhifu_position):
    start_index = data.jiugong.index(zhifu_position)
    if yinyang == "阳":
        gods = data.gods_yang
        direction = 1
    else:
        gods = data.gods_yin
        direction = 1
    god_plate = {}
    for i, pos in enumerate(data.jiugong):
        god_index = (start_index + i * direction) % 9
        god_plate[pos] = gods[god_index]
    return god_plate

