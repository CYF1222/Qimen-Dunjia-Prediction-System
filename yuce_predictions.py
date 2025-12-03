"""
预测分析模块
包含各类问题的详细预测分析功能
"""

from data import *
from yuce_utils import *
from yuce_yongshen import get_current_season

def get_love_prediction(pan, door, star, god):
    """获取感情预测建议"""
    advice_list = []
    # 查找六合位置
    for pos in jiugong:
        if pan.get('神盘', {}).get(pos) == '六合':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"✅ 六合在{pos}宫({direction})，这个方位利于感情发展")
            break
    
    if door in love_advice['door']:
        advice_list.append(love_advice['door'][door])
    if star in love_advice['star']:
        advice_list.append(love_advice['star'][star])
    if god in love_advice['god']:
        advice_list.append(love_advice['god'][god])
    
    return advice_list

def get_career_prediction(pan, door, star, god):
    """获取事业预测建议"""
    advice_list = []
    # 查找开门位置
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '开门':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"✅ 开门在{pos}宫({direction})，事业发展机会在这个方向")
            break
    
    if door in career_advice['door']:
        advice_list.append(career_advice['door'][door])
    if star in career_advice['star']:
        advice_list.append(career_advice['star'][star])
    if god in career_advice['god']:
        advice_list.append(career_advice['god'][god])
    
    return advice_list

def get_wealth_prediction(pan, door):
    """获取财运预测建议"""
    advice_list = []
    # 查找生门和开门位置
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '生门':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"✅ 生门在{pos}宫({direction})，求财往这个方向有利")
        if pan.get('人盘', {}).get(pos) == '开门':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"✅ 开门在{pos}宫({direction})，合作或新项目可考虑这个方向")
    
    if door in wealth_advice['door']:
        advice_list.append(wealth_advice['door'][door])
    # 查找戊土位置（钱财）
    for pos in jiugong:
        if pan.get('地盘', {}).get(pos) == '戊':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"💰 戊土在{pos}宫({direction})，钱财与这个方位相关")
            break
    
    return advice_list

def get_study_prediction(pan, door, star, god):
    """获取学习预测建议"""
    advice_list = []
    # 查找天辅星位置（文曲星）
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天辅':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"✅ 文昌星天辅在{pos}宫({direction})，在这个方位学习效果更好")
            break
    
    if star in study_advice['star']:
        advice_list.append(study_advice['star'][star])
    if door in study_advice['door']:
        advice_list.append(study_advice['door'][door])
    if god in study_advice['god']:
        advice_list.append(study_advice['god'][god])
    
    return advice_list

def get_health_prediction(pan, gong, door, star):
    """获取健康预测建议"""
    advice_list = []
    # 查找天芮星位置（病星）和天心星位置（医星）
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天芮':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"⚠️ 病星天芮在{pos}宫({direction})，注意相关脏腑健康")
        if pan.get('天盘', {}).get(pos) == '天心':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"✅ 医星天心在{pos}宫({direction})，治疗可往这个方向寻找")
    
    if door in health_advice['door']:
        advice_list.append(health_advice['door'][door])
    if star == '天芮':
        advice_list.append("⚠️ 当前有天芮星照，需特别注意健康问题")
    elif star == '天心':
        advice_list.append("✅ 天心星现，医疗效果较好，康复顺利")
    # 根据宫位对应的脏腑
    if gong in gong_to_organ:
        advice_list.append(f"📍 当前宫位对应：{gong_to_organ[gong]}")
    
    return advice_list

def get_lawsuit_prediction(pan, door, star, god):
    """获取官司诉讼预测建议"""
    advice_list = []
    # 查找值符位置
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == pan.get('值符', ''):
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"✅ 值符在{pos}宫({direction})，这个方位寻求司法帮助更有效")
            break
    
    if door in lawsuit_advice['door']:
        advice_list.append(lawsuit_advice['door'][door])
    if star in lawsuit_advice['star']:
        advice_list.append(lawsuit_advice['star'][star])
    if god in lawsuit_advice['god']:
        advice_list.append(lawsuit_advice['god'][god])
    
    return advice_list

def get_travel_prediction(pan, door, god):
    """获取出行安全预测建议"""
    advice_list = []
    # 查找天冲星和伤门位置
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天冲':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"✅ 天冲星在{pos}宫({direction})，这个方向出行较顺利")
        if pan.get('人盘', {}).get(pos) == '伤门':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"⚠️ 伤门在{pos}宫({direction})，这个方位需注意安全")
    
    if door in travel_advice['door']:
        advice_list.append(travel_advice['door'][door])
    if god in travel_advice['god']:
        advice_list.append(travel_advice['god'][god])
    
    return advice_list

def get_general_prediction(door, star, god):
    """获取通用预测建议"""
    advice_list = []
    
    if door in ji_gates:
        advice_list.append("✅ 当前吉门当值，可以积极行动")
    elif door in xiong_gates:
        advice_list.append("⚠️ 当前凶门当值，需谨慎行事")
    
    if god in ji_gods:
        advice_list.append("✅ 吉神护佑，有贵人相助")
    elif god in xiong_gods:
        advice_list.append("⚠️ 凶神临位，需小心应对")
    # 根据星的基本判断
    if star in ['天辅', '天心', '天任']:
        advice_list.append("✅ 当前吉星当值，运势较为顺利")
    elif star in ['天芮', '天蓬']:
        advice_list.append("⚠️ 当前需要注意，可能有挑战")
    
    return advice_list

def add_general_suggestions(advice_list, yinyang, solar_term):
    """添加通用建议"""
    season = get_current_season(solar_term)
    if season in general_suggestions['season']:
        advice_list.append(general_suggestions['season'][season])
    
    if yinyang in general_suggestions['yinyang']:
        advice_list.append(general_suggestions['yinyang'][yinyang])
    
    return advice_list

def get_detailed_love_prediction(pan, yongshen_info):
    """详细的感情预测分析"""
    analysis = "💖 详细感情预测：\n\n"
    # 查找六合位置
    liuhe_pos = next((pos for pos in jiugong if pan.get('神盘', {}).get(pos) == '六合'), None)
    
    if liuhe_pos:
        direction = convert_gong_to_direction(liuhe_pos)
        time_desc = gong_to_time.get(liuhe_pos, '相关时间')
        analysis += f"✅ 六合（婚姻缘分）在{liuhe_pos}宫({direction})，说明：\n"
        analysis += f"   • 你的正缘可能出现在{direction}\n   • 在{time_desc}更容易遇到合适的人\n"
    # 查找天芮星位置
    tianrui_pos = next((pos for pos in jiugong if pan.get('天盘', {}).get(pos) == '天芮'), None)
    
    if tianrui_pos:
        direction = convert_gong_to_direction(tianrui_pos)
        analysis += f"⚠️ 天芮星（问题）在{tianrui_pos}宫({direction})，提示：\n"
        analysis += f"   • 感情中可能存在{direction}相关的问题\n   • 需要更多的沟通和理解\n"
    # 什么时候表白合适
    analysis += "\n📅 最佳表白时机：\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = gong_to_time.get(gong, '')
        if time_desc:
            analysis += f"   • 在{time_desc}表白效果更佳\n"
    # 根据季节判断
    solar_term = pan.get('基本信息', {}).get('节气', '')
    season = get_current_season(solar_term)
    if season in love_timing:
        analysis += f"   • {love_timing[season]}\n"
    # 根据门判断
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = convert_gong_to_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        
        if door in love_confession:
            analysis += f"\n{love_confession[door].format(direction=direction)}"
    
    return analysis

def get_detailed_career_prediction(pan, yongshen_info):
    """详细的事业预测分析"""
    analysis = "💼 详细事业预测：\n\n"
    # 查找开门和生门位置
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '开门':
            direction = convert_gong_to_direction(pos)
            time_desc = gong_to_time.get(pos, '相关时间')
            analysis += f"✅ 开门（事业机会）在{pos}宫({direction})，说明：\n"
            analysis += f"   • 事业发展机会在{direction}\n   • 在{time_desc}更容易成功\n"
            break
    
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '生门':
            direction = convert_gong_to_direction(pos)
            analysis += f"💰 生门（财运）在{pos}宫({direction})，说明：\n   • 财运机会在{direction}\n   • 适合投资或创业\n"
            break
    # 最佳工作变动时机
    analysis += "\n📅 最佳工作变动时机：\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = gong_to_time.get(gong, '')
        if time_desc:
            analysis += f"   • 在{time_desc}考虑变动更有利\n"
    # 根据阴阳遁判断
    yinyang = pan.get('基本信息', {}).get('阴阳遁', '')
    if yinyang == '阳遁':
        analysis += "   • 当前阳遁，适合主动寻求机会\n   • 可以大胆尝试新领域\n"
    else:
        analysis += "   • 当前阴遁，适合等待合适时机\n   • 保守行事，稳固现有基础\n"
    # 根据值符值使判断
    zhifu, zhishi = pan.get('值符', ''), pan.get('值使', '')
    analysis += f"\n👔 贵人提示：\n   • 值符（{zhifu}）代表领导贵人\n   • 值使（{zhishi}）代表执行贵人\n   • 多与相关人士沟通合作\n"
    
    return analysis

def get_detailed_wealth_prediction(pan, yongshen_info):
    """详细的财运预测分析"""
    analysis = "💰 详细财运预测：\n\n"
    # 查找生门、开门和戊土位置
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '生门':
            direction = convert_gong_to_direction(pos)
            time_desc = gong_to_time.get(pos, '相关时间')
            analysis += f"✅ 生门（财运）在{pos}宫({direction})，说明：\n   • 求财最佳方向是{direction}\n   • 在{time_desc}财运最旺\n"
            break
    
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '开门':
            direction = convert_gong_to_direction(pos)
            analysis += f"🚪 开门（机会）在{pos}宫({direction})，说明：\n   • 合作机会在{direction}\n   • 适合开展新业务或合作\n"
            break
    
    for pos in jiugong:
        if pan.get('地盘', {}).get(pos) == '戊':
            direction = convert_gong_to_direction(pos)
            analysis += f"💵 戊土（钱财）在{pos}宫({direction})，说明：\n   • 钱财与{direction}相关\n   • 注意财务管理和投资方向\n"
            break
    # 投资建议
    analysis += "\n📈 投资建议：\n"
    # 根据季节判断
    solar_term = pan.get('基本信息', {}).get('节气', '')
    season = get_current_season(solar_term)
    if season in investment_advice:
        analysis += f"   • {investment_advice[season]}\n"
    # 根据门判断
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = convert_gong_to_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        
        if door in wealth_timing:
            analysis += wealth_timing[door].format(direction=direction)
    
    return analysis

def get_detailed_study_prediction(pan, yongshen_info):
    """详细的学习预测分析"""
    analysis = "📚 详细学习预测：\n\n"
    # 查找天辅星位置
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天辅':
            direction = convert_gong_to_direction(pos)
            time_desc = gong_to_time.get(pos, '相关时间')
            analysis += f"✅ 天辅星（文曲星）在{pos}宫({direction})，说明：\n   • 学习最佳方位是{direction}\n   • 在{time_desc}学习效果最好\n"
            break
    # 考试时间建议
    analysis += "\n📅 最佳考试时间：\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = gong_to_time.get(gong, '')
        if time_desc:
            analysis += f"   • 在{time_desc}考试状态更佳\n"
    # 根据季节判断
    solar_term = pan.get('基本信息', {}).get('节气', '')
    season = get_current_season(solar_term)
    if season in study_season:
        analysis += f"   • {study_season[season]}\n"
    # 根据门判断
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = convert_gong_to_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        
        if door in study_suggestions:
            analysis += study_suggestions[door].format(direction=direction)
    # 学习方法建议
    analysis += "\n💡 学习方法建议：\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = convert_gong_to_direction(gong)
        
        if gong in study_methods:
            analysis += study_methods[gong].format(direction=direction)
    
    return analysis

def get_detailed_health_prediction(pan, yongshen_info):
    """详细的健康预测分析"""
    analysis = "💊 详细健康预测：\n\n"
    # 查找天芮星和天心星位置
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天芮':
            direction = convert_gong_to_direction(pos)
            time_desc = gong_to_time.get(pos, '相关时间')
            analysis += f"⚠️ 病星天芮在{pos}宫({direction})，说明：\n   • 健康问题与{direction}相关\n   • 在{time_desc}症状可能加重\n"
        if pan.get('天盘', {}).get(pos) == '天心':
            direction = convert_gong_to_direction(pos)
            analysis += f"✅ 医星天心在{pos}宫({direction})，说明：\n   • 医疗资源在{direction}更有效\n   • 治疗效果较好，康复顺利\n"
    # 最佳治疗时机
    analysis += "\n📅 最佳治疗时机：\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = gong_to_time.get(gong, '')
        if time_desc:
            analysis += f"   • 在{time_desc}治疗效果更佳\n"
    # 根据季节判断
    solar_term = pan.get('基本信息', {}).get('节气', '')
    season = get_current_season(solar_term)
    if season in health_season:
        analysis += f"   • {health_season[season]}\n"
    # 根据门判断
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = convert_gong_to_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        
        if door in rest_advice:
            analysis += rest_advice[door].format(direction=direction)
    # 养生方法
    analysis += "\n🌿 养生方法建议：\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        
        if gong in gong_to_organ:
            analysis += f"   • 重点调理：{gong_to_organ[gong]}\n"
        
        if gong in health_methods:
            analysis += health_methods[gong]
    
    return analysis

def get_detailed_lawsuit_prediction(pan, yongshen_info):
    """详细的官司诉讼预测分析"""
    analysis = "⚖️ 详细官司诉讼预测：\n\n"
    # 查找值符位置和天柱星位置
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == pan.get('值符', ''):
            direction = convert_gong_to_direction(pos)
            analysis += f"⭐ 值符（法官/裁决者）在{pos}宫({direction})，说明：\n   • 司法资源或法官态度在{direction}有利\n   • 寻求官方渠道解决更有效\n"
        if pan.get('天盘', {}).get(pos) == '天柱':
            direction = convert_gong_to_direction(pos)
            analysis += f"⚠️ 天柱星（口舌）在{pos}宫({direction})，提示：\n   • 争议焦点与{direction}相关\n   • 注意法律文书的准确性\n   • 避免口头承诺，以书面为准\n"
    # 最佳解决时机
    analysis += "\n📅 最佳解决时机：\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = gong_to_time.get(gong, '')
        if time_desc:
            analysis += f"   • 在{time_desc}处理法律事务更有利\n"
    # 根据门判断
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = convert_gong_to_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        
        if door in lawsuit_strategy:
            analysis += lawsuit_strategy[door].format(direction=direction)
    # 和解建议
    analysis += "\n🤝 和解建议：\n"
    # 查找六合位置
    liuhe_pos = next((pos for pos in jiugong if pan.get('神盘', {}).get(pos) == '六合'), None)
    
    if liuhe_pos:
        direction = convert_gong_to_direction(liuhe_pos)
        analysis += f"   • 六合在{liuhe_pos}宫({direction})，和解机会存在\n   • 通过{direction}的中间人调解\n   • 考虑妥协方案，避免两败俱伤\n"
    else:
        analysis += "   • 当前和解机会较小，需做好诉讼准备\n"
    
    return analysis

def get_detailed_travel_prediction(pan, yongshen_info):
    """详细的出行安全预测分析"""
    analysis = "✈️ 详细出行安全预测：\n\n"
    # 查找天冲星和伤门位置
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天冲':
            direction = convert_gong_to_direction(pos)
            time_desc = gong_to_time.get(pos, '相关时间')
            analysis += f"🚗 天冲星（出行）在{pos}宫({direction})，说明：\n   • 出行方向以{direction}较佳\n   • 在{time_desc}出行更顺利\n"
        if pan.get('人盘', {}).get(pos) == '伤门':
            direction = convert_gong_to_direction(pos)
            analysis += f"⚠️ 伤门（伤害）在{pos}宫({direction})，提示：\n   • {direction}需注意安全\n   • 避免高风险活动\n   • 注意交通安全\n"
    # 最佳出行时间
    analysis += "\n📅 最佳出行时间：\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = gong_to_time.get(gong, '')
        if time_desc:
            analysis += f"   • 在{time_desc}出行更安全顺利\n"
    # 根据门判断
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = convert_gong_to_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        
        if door in travel_suggestions:
            analysis += travel_suggestions[door].format(direction=direction)
    # 交通工具选择和安全注意事项
    analysis += "\n🚗 交通工具选择：\n"
    analysis += "\n🔒 安全注意事项：\n"
    # 查找白虎和太阴位置
    for pos in jiugong:
        if pan.get('神盘', {}).get(pos) == '白虎':
            direction = convert_gong_to_direction(pos)
            analysis += f"   • 白虎在{pos}宫({direction})，该方位可能有风险\n   • 避免夜间单独出行\n   • 保管好贵重物品\n"
        if pan.get('神盘', {}).get(pos) == '太阴':
            direction = convert_gong_to_direction(pos)
            analysis += f"   • 太阴在{pos}宫({direction})，适合隐秘出行\n   • 低调行事，避免张扬\n"
    
    return analysis

def predict_timing(pan, yongshen_info, question_type):
    """预测应期祸福"""
    timing_analysis = f"【详细分析】\n\n"    
    # 获取基本信息
    ju_shu = pan.get('基本信息', {}).get('局数', '')
    yinyang = pan.get('基本信息', {}).get('阴阳遁', '')
    # 一、时间判断
    timing_analysis += "一、时间判断（什么时候会有什么变化？）\n"
    timing_analysis += "-"*40 + "\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        yongshen_gong = yongshen_info['宫位']
        # 从数据文件中获取宫位与时间对应关系
        time_desc = gong_to_time.get(yongshen_gong, '近期内')
        timing_analysis += f"1. 关键时间点：{time_desc}\n"
        # 根据局数判断时间长短
        if 1 <= ju_shu <= 3:
            timing_analysis += "2. 时间快慢：较快，可能在几天到一周内有结果\n"
        elif 4 <= ju_shu <= 6:
            timing_analysis += "2. 时间快慢：中等，大概需要一到两周\n"
        else:
            timing_analysis += "2. 时间快慢：较慢，可能需要一个月左右\n"
    else:
        timing_analysis += "1. 请先确定用神位置，才能准确判断时间\n"
    # 二、现状分析
    timing_analysis += "\n二、当前情况分析\n"
    timing_analysis += "-"*40 + "\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        door = pan.get('人盘', {}).get(gong, '')
        star = pan.get('天盘', {}).get(gong, '')
        god = pan.get('神盘', {}).get(gong, '')
        
        timing_analysis += f"1. 你的状态：用神在{gong}宫({convert_gong_to_direction(gong)})\n"
        # 门的状态描述
        timing_analysis += f"2. 当前机会：{door_desc.get(door, '需要结合具体分析')}\n"
        # 星的状态描述
        timing_analysis += f"3. 个人状态：{star_desc.get(star, '状态平稳')}\n"
        # 神的状态描述
        timing_analysis += f"4. 外部环境：{god_desc.get(god, '环境一般')}\n"
    else:
        timing_analysis += "无法分析现状，请先确定用神位置\n"
    # 三、行动建议
    timing_analysis += "\n三、行动建议\n"
    timing_analysis += "-"*40 + "\n"
    
    advice_list = []
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        door = pan.get('人盘', {}).get(gong, '')
        star = pan.get('天盘', {}).get(gong, '')
        god = pan.get('神盘', {}).get(gong, '')
        # 根据问题类型和当前盘局动态生成建议
        if question_type == "婚姻感情":
            advice_list = get_love_prediction(pan, door, star, god)
        elif question_type == "工作事业":
            advice_list = get_career_prediction(pan, door, star, god)
        elif question_type == "财运求财":
            advice_list = get_wealth_prediction(pan, door)
        elif question_type == "考试学习":
            advice_list = get_study_prediction(pan, door, star, god)
        elif question_type == "疾病健康":
            advice_list = get_health_prediction(pan, gong, door, star)
        elif question_type == "官司诉讼":
            advice_list = get_lawsuit_prediction(pan, door, star, god)
        elif question_type == "出行安全":
            advice_list = get_travel_prediction(pan, door, god)
        else:
            advice_list = get_general_prediction(door, star, god)
        # 添加通用建议
        add_general_suggestions(advice_list, yinyang, pan.get('基本信息', {}).get('节气', ''))
        # 显示建议
        advice_list = advice_list[:5]
        
    else:
        advice_list.append("请先确定用神位置，才能给出针对性建议")
    # 显示建议
    if advice_list:
        for i, advice in enumerate(advice_list, 1):
            timing_analysis += f"{i}. {advice}\n"
    else:
        timing_analysis += "暂无具体建议\n"
    # 四、特殊提示
    timing_analysis += "\n四、特殊提示\n"
    timing_analysis += "-"*40 + "\n"
    
    special_tips = get_special_tips(pan, yongshen_info)
    for tip in special_tips:
        timing_analysis += f"{tip}\n"
    # 五、简单总结
    timing_analysis += "\n五、总结\n"
    timing_analysis += "-"*40 + "\n"
    
    summary = get_summary(pan, yongshen_info, question_type)
    for i, item in enumerate(summary, 1):
        timing_analysis += f"{i}. {item}\n"
    # 添加预测型分析
    timing_analysis += "\n" + "="*50 + "\n"
    timing_analysis += "【预测分析】\n\n"
    # 根据问题类型添加特定预测
    if question_type == "婚姻感情":
        timing_analysis += get_detailed_love_prediction(pan, yongshen_info)
    elif question_type == "工作事业":
        timing_analysis += get_detailed_career_prediction(pan, yongshen_info)
    elif question_type == "财运求财":
        timing_analysis += get_detailed_wealth_prediction(pan, yongshen_info)
    elif question_type == "考试学习":
        timing_analysis += get_detailed_study_prediction(pan, yongshen_info)
    elif question_type == "疾病健康":
        timing_analysis += get_detailed_health_prediction(pan, yongshen_info)
    elif question_type == "官司诉讼":
        timing_analysis += get_detailed_lawsuit_prediction(pan, yongshen_info)
    elif question_type == "出行安全":
        timing_analysis += get_detailed_travel_prediction(pan, yongshen_info)
    # 最后的实用提醒
    timing_analysis += "\n" + "="*50 + "\n"
    timing_analysis += "【重要提醒】\n"
    timing_analysis += "• 以上分析基于今日排盘，明日盘局变化，建议也会不同\n"
    timing_analysis += "• 真正的决策还需结合实际情况和个人判断\n"
    timing_analysis += "• 命运掌握在自己手中，积极行动才是最好的策略\n"
    timing_analysis += "="*50
    
    return timing_analysis