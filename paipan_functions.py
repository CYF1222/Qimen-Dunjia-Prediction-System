import data
from datetime import datetime as dt

def leap_year(year):
    """判断是否为闰年"""
    return 1 if ((year % 4 == 0 and year % 100 != 0) or year % 400 == 0) else 0

def Solar_terms(year, month, day):
    """计算节气信息"""
    month_const = data.TERM_CONST[month]
    # 根据年份范围选择对应的常数
    if 1900 <= year < 2000:
        const_idx, base_year = 0, 1900
    elif 2000 <= year < 2100:
        const_idx, base_year = 1, 2000
    elif 2100 <= year < 2200:
        const_idx, base_year = 2, 2100
    else:
        return "立春", 0, [year, 1, 1]
    
    year_const1, year_const2 = month_const[0][const_idx], month_const[1][const_idx]
    term_date1 = int(year_const1 + 0.2422 * (year - base_year) - (year - base_year) // 4)
    term_date2 = int(year_const2 + 0.2422 * (year - base_year) - (year - base_year) // 4)
    
    # 判断当前日期属于哪个节气区间
    if term_date1 <= day < term_date2:
        return month_const[0][-1], day - term_date1, [year, month, term_date1]
    elif day >= term_date2:
        return month_const[1][-1], day - term_date2, [year, month, term_date2]
    
    # 如果当前日期不在本月节气区间，需要查找前一个月的节气
    prev_month = 12 if month == 1 else month - 1
    prev_year = year - 1 if month == 1 else year
    
    month_const = data.TERM_CONST[prev_month]
    if 1900 <= prev_year < 2000:
        year_const2 = month_const[1][0]
        term_date2 = int(year_const2 + 0.2422 * (prev_year - 1900) - (prev_year - 1900) // 4)
    elif 2000 <= prev_year < 2100:
        year_const2 = month_const[1][1]
        term_date2 = int(year_const2 + 0.2422 * (prev_year - 2000) - (prev_year - 2000) // 4)
    elif 2100 <= prev_year < 2200:
        year_const2 = month_const[1][2]
        term_date2 = int(year_const2 + 0.2422 * (prev_year - 2100) - (prev_year - 2100) // 4)
    
    prev_month_days = data.MONTH_DAYS[prev_month] + (1 if prev_month == 2 and leap_year(prev_year) else 0)
    return month_const[1][-1], day + prev_month_days - term_date2, [prev_year, prev_month, term_date2]

def day_year(year, month, day):
    """计算指定日期是该年的第几天"""
    days = day
    for i in range(1, month):
        days += data.MONTH_DAYS[i]
    return days + 1 if (month > 2 and leap_year(year)) else days

def day_between_year(year):
    """计算从1900年到指定年份前一年的总天数"""
    return sum(366 if leap_year(i) else 365 for i in range(1900, year))

def get_jiazi(year, month, day):
    """计算日柱干支"""
    days = day_year(year, month, day) + day_between_year(year)
    index = (days + 10) % 60
    return data.jiazi_list[index - 1 if index else 59]

def day_p(year, month, day):
    """获取前一天的日期"""
    if day > 1:
        return [year, month, day - 1]
    
    if month > 3 or month == 2:
        return [year, month - 1, data.MONTH_DAYS[month - 1]]
    elif month == 3:
        return [year, 2, data.MONTH_DAYS[2] + (1 if leap_year(year) else 0)]
    else:
        return [year - 1, 12, 31]

def find_futou(year, month, day):
    """查找符头日期和干支"""
    current_date = [year, month, day]
    while True:
        current_ganzhi = get_jiazi(*current_date)
        if current_ganzhi[0] in ['甲', '己']:
            return current_date, current_ganzhi
        current_date = day_p(*current_date)

def get_sanyuan(futou_ganzhi):
    """根据符头干支确定三元"""
    dizhi = futou_ganzhi[1]
    return "上元" if dizhi in ['子', '午', '卯', '酉'] else "中元" if dizhi in ['寅', '申', '巳', '亥'] else "下元"

def days_between_dates(year1, month1, day1, year2, month2, day2):
    """计算两个日期之间的天数差（使用datetime优化）"""
    date1 = dt(year1, month1, day1)
    date2 = dt(year2, month2, day2)
    return abs((date2 - date1).days)

def get_previous_solar_term(current_solar_term):
    """获取前一个节气"""
    current_index = data.solar_terms.index(current_solar_term)
    return data.solar_terms[current_index - 1]

def check_chaoshen_jieqi(solar_term_date, futou_date, solar_term, jushu):
    """检查超神接气，调整局数"""
    days_diff = days_between_dates(futou_date[0], futou_date[1], futou_date[2],
                                   solar_term_date[0], solar_term_date[1], solar_term_date[2])
    
    if days_diff > 0 and days_diff > 9 and solar_term in ["芒种", "大雪"]:
        return data.ju_table_base.get(get_previous_solar_term(solar_term), 1)
    return jushu

def get_jushu(year, month, day):
    """获取奇门遁甲的局数"""
    solar_term_name, days_after, solar_term_date = Solar_terms(year, month, day)
    is_yang = solar_term_name in data.yang_dun
    ju_table = data.yang_ju if is_yang else data.yin_ju
    yinyang = '阳' if is_yang else '阴'
    
    futou_date, futou_ganzhi = find_futou(year, month, day)
    sanyuan = get_sanyuan(futou_ganzhi)
    base_jushu = ju_table.get(solar_term_name, {}).get(sanyuan, 1)
    
    return yinyang, check_chaoshen_jieqi(solar_term_date, futou_date, solar_term_name, base_jushu)

def get_hour_ganzhi(day_ganzhi, hour):
    """计算时柱干支"""
    day_gan = day_ganzhi[0]
    hour_branch = data.hour_to_branch[hour]
    branch_index = data.di_zhi.index(hour_branch)
    zi_gan_index = data.tian_gan.index(data.wushudun[day_gan])
    hour_gan = data.tian_gan[(zi_gan_index + branch_index) % 10]
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
    index = ju_number + xunxu - 1 if yinyang == "阳" else 1 + ju_number - xunxu
    return index - 9 if index > 9 else index + 9 if index < 1 else index

def get_zhifu_zhishi_by_index(index):
    """根据序数确定值符和值使"""
    return data.index_to_zhifu_zhishi[index]

def determine_zhifu_and_zhishi(xunshou, ju_number, yinyang):
    """根据旬首、局数和阴阳遁确定值符和值使"""
    return get_zhifu_zhishi_by_index(get_zhifu_zhishi_index(ju_number, get_xunxu(xunshou), yinyang))

def arrange_earth_plate(ju_number, yinyang):
    """排地盘"""
    earth_plate_dict, start_index = {}, ju_number - 1
    is_yang = yinyang == "阳"
    
    for i, gong in enumerate(data.jiugong):
        star_index = (start_index + i) % 9 if is_yang else (start_index - i) % 9
        earth_plate_dict[gong] = data.qiyi[star_index]
    return earth_plate_dict

def arrange_human_plate(xunshou, hour_zhi, yinyang):
    """排人盘"""
    zhishi_gate = data.xunshou_to_zhishi[xunshou]
    target_position = data.zhi_to_jiugong.get(hour_zhi, "中")
    start_index = data.jiugong.index(data.initial_gate_positions.get(zhishi_gate, "坎"))
    target_index = data.jiugong.index(target_position)
    
    offset = (target_index - start_index) % 9 if yinyang == "阳" else (start_index - target_index) % 9
    zhishi_index = data.gates.index(zhishi_gate)
    
    human_plate = {}
    for i, pos in enumerate(data.jiugong):
        if pos == "中":
            human_plate[pos] = None
            continue
        gate_index = (zhishi_index + i + offset) % 8 if yinyang == "阳" else (zhishi_index - i - offset) % 8
        human_plate[pos] = data.gates[gate_index % 8]
    return human_plate

def arrange_heaven_plate(earth_plate, zhifu, hour_gan, yinyang):
    """排天盘"""
    start_position = next((pos for pos, star in earth_plate.items() if star == zhifu), "坎")
    target_position = data.gan_to_jiugong.get(hour_gan, "中")
    start_index, target_index = data.jiugong.index(start_position), data.jiugong.index(target_position)
    
    offset = (target_index - start_index) % 9 if yinyang == "阳" else (start_index - target_index) % 9
    zhifu_index = data.stars.index(zhifu)
    
    heaven_plate = {}
    for i, pos in enumerate(data.jiugong):
        star_index = (zhifu_index + offset + i) % 9 if yinyang == "阳" else (zhifu_index - offset - i) % 9
        heaven_plate[pos] = data.stars[star_index % 9]
    return heaven_plate

def arrange_god_plate(zhifu_position, yinyang):
    """排神盘"""
    gods, direction = (data.gods_yang, 1) if yinyang == "阳" else (data.gods_yin, -1)
    god_plate, start_index = {}, data.jiugong.index(zhifu_position)
    
    for i, pos in enumerate(data.jiugong):
        god_plate[pos] = None if pos == "中" else gods[(start_index + direction * i) % 8]
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
    return data.tian_gan[(year - 1) % 10], data.di_zhi[(year - 1) % 12]

def create_qimen_pan(year, month, day, hour):
    """创建奇门遁甲盘"""
    solar_term, _, solar_term_date = Solar_terms(year, month, day)
    yinyang, ju_number = get_jushu(year, month, day)
    day_ganzhi = get_jiazi(year, month, day)
    hour_ganzhi = get_hour_ganzhi(day_ganzhi, hour)
    xunshou = get_xunshou(hour_ganzhi)
    
    earth_plate = arrange_earth_plate(ju_number, yinyang)
    zhifu, zhishi = determine_zhifu_and_zhishi(xunshou, ju_number, yinyang)
    
    zhifu_position = next((pos for pos, star in data.jiugong_to_star.items() if star == zhifu), "坎")
    heaven_plate = arrange_heaven_plate(earth_plate, zhifu, hour_ganzhi[0], yinyang)
    human_plate = arrange_human_plate(xunshou, hour_ganzhi[1], yinyang)
    god_plate = arrange_god_plate(zhifu_position, yinyang)
    
    year_gan, year_zhi = get_year_ganzhi(year)
    month_ganzhi = get_month_ganzhi((year_gan, year_zhi), month)
    
    return {
        '基本信息': {
            '时间': f"{year}年{month}月{day}日{hour}时",
            '节气': solar_term,
            '阴阳遁': yinyang,
            '局数': ju_number,
            '四柱': {
                '年': f"{year_gan}{year_zhi}年",
                '月': month_ganzhi,
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