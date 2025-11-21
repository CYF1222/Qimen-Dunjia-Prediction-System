import data
import sys
import io

# 设置标准输出编码为UTF-8，确保中文字符正常显示
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def leap_year(year):
    """判断是否为闰年"""
    if ((year % 4 == 0 and year % 100 != 0) or year % 400 == 0):
        return 1
    else:
        return 0

def Solar_terms(year, month, day):
    """计算节气信息"""
    month_const = data.TERM_CONST[month]
    
    # 根据年份范围选择对应的常数
    if (1900 <= year < 2000):
        year_const1 = month_const[0][0]
        year_const2 = month_const[1][0]
        term_date1 = int(year_const1 + 0.2422 * (year - 1900) - int((year - 1900) / 4))
        term_date2 = int(year_const2 + 0.2422 * (year - 1900) - int((year - 1900) / 4))
    elif (2000 <= year < 2100):
        year_const1 = month_const[0][1]
        year_const2 = month_const[1][1]
        term_date1 = int(year_const1 + 0.2422 * (year - 2000) - int((year - 2000) / 4))
        term_date2 = int(year_const2 + 0.2422 * (year - 2000) - int((year - 2000) / 4))
    elif (2100 <= year < 2200):
        year_const1 = month_const[0][2]
        year_const2 = month_const[1][2]
        term_date1 = int(year_const1 + 0.2422 * (year - 2100) - int((year - 2100) / 4))
        term_date2 = int(year_const2 + 0.2422 * (year - 2100) - int((year - 2100) / 4))
    
    # 判断当前日期属于哪个节气区间
    if (term_date1 <= day < term_date2):
        return month_const[0][-1], day - term_date1, [year, month, term_date1]
    elif (day >= term_date2):
        return month_const[1][-1], day - term_date2, [year, month, term_date2]
    else:
        # 如果当前日期不在本月节气区间，需要查找前一个月的节气
        if (month == 1):
            month_p = 12
            month_const = data.TERM_CONST[month_p]
            year_p = year - 1
            if (1900 <= year_p < 2000):
                year_const2 = month_const[1][0]
                term_date2 = int(year_const2 + 0.2422 * (year_p - 1900) - int((year_p - 1900) / 4))
            elif (2000 <= year_p < 2100):
                year_const2 = month_const[1][1]
                term_date2 = int(year_const2 + 0.2422 * (year_p - 2000) - int((year_p - 2000) / 4))
            elif (2100 <= year_p < 2200):
                year_const2 = month_const[1][2]
                term_date2 = int(year_const2 + 0.2422 * (year_p - 2100) - int((year_p - 2100) / 4))
            return month_const[1][-1], day + data.MONTH_DAYS[month_p] - term_date2, [year - 1, month_p, term_date2]
        elif (month == 3):
            month_p = 2
            month_const = data.TERM_CONST[month_p]
            if (1900 <= year < 2000):
                year_const2 = month_const[1][0]
                term_date2 = int(year_const2 + 0.2422 * (year - 1900) - int((year - 1900) / 4))
            elif (2000 <= year < 2100):
                year_const2 = month_const[1][1]
                term_date2 = int(year_const2 + 0.2422 * (year - 2000) - int((year - 2000) / 4))
            elif (2100 <= year < 2200):
                year_const2 = month_const[1][2]
                term_date2 = int(year_const2 + 0.2422 * (year - 2100) - int((year - 2100) / 4))
            
            if (leap_year(year) == 1):
                return month_const[1][-1], day + data.MONTH_DAYS[month_p] + 1 - term_date2, [year, month_p, term_date2]
            else:
                return month_const[1][-1], day + data.MONTH_DAYS[month_p] - term_date2, [year, month_p, term_date2]
        else:
            month_p = month - 1
            month_const = data.TERM_CONST[month_p]
            if (1900 <= year < 2000):
                year_const2 = month_const[1][0]
                term_date2 = int(year_const2 + 0.2422 * (year - 1900) - int((year - 1900) / 4))
            elif (2000 <= year < 2100):
                year_const2 = month_const[1][1]
                term_date2 = int(year_const2 + 0.2422 * (year - 2000) - int((year - 2000) / 4))
            elif (2100 <= year < 2200):
                year_const2 = month_const[1][2]
                term_date2 = int(year_const2 + 0.2422 * (year - 2100) - int((year - 2100) / 4))
                
            return month_const[1][-1], day + data.MONTH_DAYS[month_p] - term_date2, [year, month_p, term_date2]

def day_year(year, month, day):
    """计算指定日期是该年的第几天"""
    days = day
    for i in range(1, month):
        days = days + data.MONTH_DAYS[i]
    if (month > 2 and leap_year(year)):
        days = days + 1
    return days

def day_between_year(year):
    """计算从1900年到指定年份前一年的总天数"""
    days = 0
    for i in range(1900, year):
        if (leap_year(i)):
            days = days + 366
        else:
            days = days + 365
    return days

def get_jiazi(year, month, day):
    """计算日柱干支"""
    days = day_year(year, month, day) + day_between_year(year)
    index = (days + 10) % 60
    if index == 0:
        index = 60
    return data.jiazi_list[index - 1]

def day_p(year, month, day):
    """获取前一天的日期"""
    if (day > 1):
        return [year, month, day - 1]
    else:
        if (month > 3 or month == 2):
            return [year, month - 1, data.MONTH_DAYS[month - 1]]
        elif (month == 3):
            if (leap_year(year) == 1):
                return [year, 2, data.MONTH_DAYS[2] + 1]
            else:
                return [year, 2, data.MONTH_DAYS[2]]
        else:
            return [year - 1, 12, 31]

def find_futou(year, month, day):
    """查找符头日期和干支"""
    current_ganzhi = get_jiazi(year, month, day)
    if current_ganzhi[0] in ['甲', '己']:
        return [year, month, day], current_ganzhi
    futou_date = [year, month, day]
    while True:
        futou_date = day_p(futou_date[0], futou_date[1], futou_date[2])
        futou_ganzhi = get_jiazi(futou_date[0], futou_date[1], futou_date[2])
        if futou_ganzhi[0] in ['甲', '己']:
            return futou_date, futou_ganzhi

def get_sanyuan(futou_ganzhi):
    """根据符头干支确定三元"""
    dizhi = futou_ganzhi[1]
    if (dizhi in ['子', '午', '卯', '酉']):
        return "上元"
    elif (dizhi in ['寅', '申', '巳', '亥']):
        return "中元"
    else:
        return "下元"

def days_between_dates(year1, month1, day1, year2, month2, day2):
    """计算两个日期之间的天数差"""
    if (year1, month1, day1) > (year2, month2, day2):
        year1, month1, day1, year2, month2, day2 = year2, month2, day2, year1, month1, day1
    total_days = 0
    if year1 == year2 and month1 == month2:
        return day2 - day1
    if year1 == year2:
        if month1 == 2 and leap_year(year1):
            total_days += data.MONTH_DAYS[month1] + 1 - day1
        else:
            total_days += data.MONTH_DAYS[month1] - day1
        for month in range(month1 + 1, month2):
            if month == 2 and leap_year(year1):
                total_days += data.MONTH_DAYS[month] + 1
            else:
                total_days += data.MONTH_DAYS[month]
        total_days += day2
        return total_days
    if month1 == 2 and leap_year(year1):
        total_days += data.MONTH_DAYS[month1] + 1 - day1
    else:
        total_days += data.MONTH_DAYS[month1] - day1
    for month in range(month1 + 1, 13):
        if month == 2 and leap_year(year1):
            total_days += data.MONTH_DAYS[month] + 1
        else:
            total_days += data.MONTH_DAYS[month]
    for year in range(year1 + 1, year2):
        if leap_year(year):
            total_days += 366
        else:
            total_days += 365
    for month in range(1, month2):
        if month == 2 and leap_year(year2):
            total_days += data.MONTH_DAYS[month] + 1
        else:
            total_days += data.MONTH_DAYS[month]
    
    total_days += day2
    return total_days

def get_previous_solar_term(current_solar_term):
    """获取前一个节气"""
    current_index = data.solar_terms.index(current_solar_term)
    prev_index = (current_index - 1) % len(data.solar_terms)
    return data.solar_terms[prev_index]

def check_chaoshen_jieqi(solar_term_date, futou_date, solar_term, jushu):
    """检查超神接气，调整局数"""
    days_diff = days_between_dates(
        futou_date[0], futou_date[1], futou_date[2],
        solar_term_date[0], solar_term_date[1], solar_term_date[2]
    )
    
    if days_diff > 0:
        if days_diff > 9 and solar_term in ["芒种", "大雪"]:
            prev_term = get_previous_solar_term(solar_term)
            prev_jushu = data.ju_table_base.get(prev_term, 1)
            return prev_jushu
        else:
            return jushu
    elif days_diff < 0:
        return jushu
    else:
        return jushu

def get_jushu(year, month, day):
    """获取奇门遁甲的局数"""
    solar_term_name, days_after, solar_term_date = Solar_terms(year, month, day)
    if solar_term_name in data.yang_dun:
        yinyang = '阳'
        ju_table = data.yang_ju
    else:
        ju_table = data.yin_ju
        yinyang = '阴'
    futou_date, futou_ganzhi = find_futou(year, month, day)
    sanyuan = get_sanyuan(futou_ganzhi)
    base_jushu = ju_table.get(solar_term_name, {}).get(sanyuan, 1)
    final_jushu = check_chaoshen_jieqi(solar_term_date, futou_date, solar_term_name, base_jushu)
    return yinyang, final_jushu

def get_hour_ganzhi(day_ganzhi, hour):
    """计算时柱干支"""
    day_gan = day_ganzhi[0]
    hour_branch = data.hour_to_branch[hour]
    branch_index = data.di_zhi.index(hour_branch)
    zi_gan = data.wushudun[day_gan]
    zi_gan_index = data.tian_gan.index(zi_gan)
    hour_gan_index = (zi_gan_index + branch_index) % 10
    hour_gan = data.tian_gan[hour_gan_index]
    return hour_gan + hour_branch

def get_xunshou(hour_ganzhi):
    """获取旬首"""
    current_index = data.jiazi_list.index(hour_ganzhi)
    for i in range(current_index, -1, -1):
        if data.jiazi_list[i] in data.xunshou_list:
            return data.jiazi_list[i]
    for i in range(len(data.jiazi_list) - 1, current_index, -1):
        if data.jiazi_list[i] in data.xunshou_list:
            return data.jiazi_list[i]
    return '甲子'

def get_xunxu(xunshou):
    """根据旬首获取旬序数"""
    return data.xunshou_to_xunxu[xunshou]

def get_zhifu_zhishi_index(ju_number, xunxu, yinyang):
    """计算值符和值使的序数"""
    if yinyang == "阳":
        index = ju_number + xunxu - 1
    else:
        index = 1 + ju_number - xunxu
    
    if index > 9:
        index -= 9
    elif index < 1:
        index += 9
    
    return index

def get_zhifu_zhishi_by_index(index):
    """根据序数确定值符和值使"""
    return data.index_to_zhifu_zhishi[index]

def determine_zhifu_and_zhishi(xunshou, ju_number, yinyang):
    """根据旬首、局数和阴阳遁确定值符和值使"""
    xunxu = get_xunxu(xunshou)
    index = get_zhifu_zhishi_index(ju_number, xunxu, yinyang)
    zhifu, zhishi = get_zhifu_zhishi_by_index(index)
    return zhifu, zhishi

def arrange_earth_plate(ju_number, yinyang):
    """排地盘"""
    earth_plate_dict = {}
    start_index = ju_number - 1
    
    if yinyang == "阳":
        for i, gong in enumerate(data.jiugong):
            star_index = (start_index + i) % 9
            earth_plate_dict[gong] = data.qiyi[star_index]
    else:
        for i, gong in enumerate(data.jiugong):
            star_index = (start_index - i) % 9
            earth_plate_dict[gong] = data.qiyi[star_index]
    
    return earth_plate_dict

def arrange_human_plate(xunshou, hour_zhi, yinyang):
    """排人盘"""
    zhishi_gate = data.xunshou_to_zhishi[xunshou]
    target_position = data.zhi_to_jiugong.get(hour_zhi, "中")
    start_position = data.initial_gate_positions.get(zhishi_gate, "坎")
    
    start_index = data.jiugong.index(start_position)
    target_index = data.jiugong.index(target_position)
    
    if yinyang == "阳":
        offset = (target_index - start_index) % 9
    else:
        offset = (start_index - target_index) % 9
    
    human_plate = {}
    
    for i, pos in enumerate(data.jiugong):
        if pos == "中":
            human_plate[pos] = None
            continue
            
        zhishi_index = data.gates.index(zhishi_gate)
        
        if yinyang == "阳":
            gate_index = (zhishi_index + i + offset) % 8
        else:
            gate_index = (zhishi_index - i - offset) % 8
            
        human_plate[pos] = data.gates[gate_index % 8]
    
    return human_plate

def arrange_heaven_plate(earth_plate, zhifu, hour_gan, yinyang):
    """排天盘"""
    start_position = None
    for pos, star in earth_plate.items():
        if star == zhifu:
            start_position = pos
            break
    
    if start_position is None:
        start_position = "坎"
    
    target_position = data.gan_to_jiugong.get(hour_gan, "中")
    
    start_index = data.jiugong.index(start_position)
    target_index = data.jiugong.index(target_position)
    
    if yinyang == "阳":
        offset = (target_index - start_index) % 9
    else:
        offset = (start_index - target_index) % 9
    
    heaven_plate = {}
    zhifu_index = data.stars.index(zhifu)
    
    for i, pos in enumerate(data.jiugong):
        if pos == "中":
            heaven_plate[pos] = None
            continue
            
        if yinyang == "阳":
            star_index = (zhifu_index + offset + i) % 9
        else:
            star_index = (zhifu_index - offset - i) % 9
            
        heaven_plate[pos] = data.stars[star_index % 9]
    
    return heaven_plate

def arrange_god_plate(zhifu_position, yinyang):
    """排神盘"""
    if yinyang == "阳":
        gods = data.gods_yang
        direction = 1
    else:
        gods = data.gods_yin  
        direction = -1
    
    god_plate = {}
    start_index = data.jiugong.index(zhifu_position)
    
    for i, pos in enumerate(data.jiugong):
        if pos == "中":
            god_plate[pos] = None
            continue
            
        god_index = (start_index + direction * i) % 8
        god_plate[pos] = gods[god_index]
    
    return god_plate

def get_month_ganzhi(year_gan_zhi, month):
    """计算月柱干支"""
    year_gan, year_zhi = year_gan_zhi
    gan_index = data.tian_gan.index(year_gan)
    zhi_index = data.di_zhi.index(year_zhi)
    month_gan = data.tian_gan[(gan_index * 12 + (month - 1)) % 10]
    month_zhi = data.di_zhi[(zhi_index * 12 + (month - 1)) % 12]
    return month_gan, month_zhi

def get_year_ganzhi(year):
    """计算年柱干支"""
    gan_index = (year - 1) % 10
    zhi_index = (year - 1) % 12
    return data.tian_gan[gan_index], data.di_zhi[zhi_index]

def create_qimen_pan(year, month, day, hour):
    """创建奇门遁甲盘"""
    solar_term, _, solar_term_date = Solar_terms(year, month, day)
    yinyang, ju_number = get_jushu(year, month, day)
    day_ganzhi = get_jiazi(year, month, day)
    hour_ganzhi = get_hour_ganzhi(day_ganzhi, hour)
    xunshou = get_xunshou(hour_ganzhi)
    
    earth_plate = arrange_earth_plate(ju_number, yinyang)
    
    zhifu, zhishi = determine_zhifu_and_zhishi(xunshou, ju_number, yinyang)
    
    zhifu_position = None
    for pos, star in data.jiugong_to_star.items():
        if star == zhifu:
            zhifu_position = pos
            break
    
    heaven_plate = arrange_heaven_plate(earth_plate, zhifu, hour_ganzhi[0], yinyang)
    human_plate = arrange_human_plate(xunshou, hour_ganzhi[1], yinyang)
    god_plate = arrange_god_plate(zhifu_position, yinyang)
    
    return {
        '基本信息': {
            '时间': f"{year}年{month}月{day}日{hour}时",
            '节气': solar_term,
            '阴阳遁': yinyang,
            '局数': ju_number,
            '四柱': {
                '年': get_year_ganzhi(year)[0] + get_year_ganzhi(year)[1] + '年', 
                '月': get_month_ganzhi(get_year_ganzhi(year), month),
                '日': day_ganzhi,
                '时': hour_ganzhi
            }
        },
        '地盘': earth_plate,
        '天盘': heaven_plate,
        '人盘': human_plate,
        '神盘': god_plate,
        '值符': zhifu,
        '值使': zhishi
    }
