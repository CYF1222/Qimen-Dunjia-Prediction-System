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
    # 根据门判断
    if door == '休门':
        advice_list.append("✅ 休门当值，适合两人世界，安静相处")
    elif door == '开门':
        advice_list.append("✅ 开门当值，适合表白或公开关系")
    elif door == '惊门':
        advice_list.append("⚠️ 惊门当前，注意沟通方式，避免争吵")
    elif door == '死门':
        advice_list.append("🔴 死门当前，感情可能遇到困难")
    # 根据星判断
    if star == '天芮':
        advice_list.append("⚠️ 天芮星照，感情可能存在问题，需多加沟通")
    elif star == '天心':
        advice_list.append("✅ 天心星现，心意相通，感情发展顺利")
    elif star == '天辅':
        advice_list.append("✅ 天辅星照，感情中学习成长，适合共同进步")
    # 根据神判断
    if god == '六合':
        advice_list.append("✅ 六合守护，有良好的合作和婚姻缘分")
    elif god == '太阴':
        advice_list.append("✅ 太阴守护，适合暗中观察，低调发展感情")
    elif god == '腾蛇':
        advice_list.append("⚠️ 腾蛇临位，感情可能有变化或不确定性")
    
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
    # 根据门判断
    if door == '开门':
        advice_list.append("✅ 当前是开门，机会已经出现，大胆去尝试")
    elif door == '休门':
        advice_list.append("⚠️ 现在是休门，建议先休息调整，等待更好时机")
    elif door == '生门':
        advice_list.append("✅ 生门当值，有利于求财和工作发展")
    elif door == '伤门':
        advice_list.append("⚠️ 伤门临位，注意工作安全和避免冲动行事")
    elif door == '死门':
        advice_list.append("🔴 死门当前，工作可能遇到瓶颈，需另寻出路")
    # 根据星判断
    if star == '天辅':
        advice_list.append("✅ 天辅星照，利于学习和技能提升，可以参加培训")
    elif star == '天心':
        advice_list.append("✅ 天心星现，有领导赏识，多与上司沟通")
    elif star == '天芮':
        advice_list.append("⚠️ 天芮星照，注意同事关系，避免口舌是非")
    elif star == '天蓬':
        advice_list.append("⚠️ 天蓬星照，有野心但需注意风险控制")
    # 根据神判断
    if god == '值符':
        advice_list.append("✅ 值符护佑，有贵人相助，多听取领导意见")
    elif god == '白虎':
        advice_list.append("⚠️ 白虎当头，工作压力大，注意身体健康")
    elif god == '太阴':
        advice_list.append("✅ 太阴守护，适合暗中谋划，低调行事")
    
    return advice_list

def get_wealth_prediction(pan, door):
    """获取财运预测建议"""
    advice_list = []
    # 查找生门位置
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '生门':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"✅ 生门在{pos}宫({direction})，求财往这个方向有利")
            break
    # 查找开门位置
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '开门':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"✅ 开门在{pos}宫({direction})，合作或新项目可考虑这个方向")
            break
    # 根据门判断
    if door == '生门':
        advice_list.append("✅ 当前就在生门宫位，财运机会就在眼前")
    elif door == '开门':
        advice_list.append("✅ 开门当值，求财机会多，但要谨慎选择")
    elif door == '休门':
        advice_list.append("⚠️ 休门当前，财运平缓，不宜大投资")
    elif door == '死门':
        advice_list.append("🔴 死门当前，财运不佳，守成为上")
    elif door == '惊门':
        advice_list.append("⚠️ 惊门当前，投资可能有意外损失，需特别谨慎")
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
    # 根据星判断
    if star == '天辅':
        advice_list.append("✅ 当前有天辅星照，学习考试运势佳")
    elif star == '天芮':
        advice_list.append("⚠️ 天芮星照，学习可能遇到障碍，需加倍努力")
    elif star == '天心':
        advice_list.append("✅ 天心星现，思维清晰，适合解题分析")
    # 根据门判断
    if door == '景门':
        advice_list.append("✅ 景门当前，考试发挥好，但需防粗心")
    elif door == '杜门':
        advice_list.append("⚠️ 杜门当前，思路可能不畅，需要多复习")
    elif door == '休门':
        advice_list.append("✅ 休门当值，适合休息调整学习状态")
    elif door == '开门':
        advice_list.append("✅ 开门当值，新的学习机会或考试机会出现")
    # 根据神判断
    if god == '太阴':
        advice_list.append("✅ 太阴守护，适合安静学习，深思熟虑")
    elif god == '九天':
        advice_list.append("✅ 九天护佑，思维活跃，适合创新学习")
    
    return advice_list

def get_health_prediction(pan, gong, door, star):
    """获取健康预测建议"""
    advice_list = []
    # 查找天芮星位置（病星）
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天芮':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"⚠️ 病星天芮在{pos}宫({direction})，注意相关脏腑健康")
            break
    # 查找天心星位置（医星）
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天心':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"✅ 医星天心在{pos}宫({direction})，治疗可往这个方向寻找")
            break
    # 根据门判断
    if door == '死门':
        advice_list.append("🔴 死门当前，病情需重视，及时就医")
    elif door == '休门':
        advice_list.append("✅ 休门当值，适合静养休息")
    elif door == '生门':
        advice_list.append("✅ 生门当值，康复能力较强，恢复快")
    elif door == '伤门':
        advice_list.append("⚠️ 伤门临位，注意意外伤害或手术")
    # 根据星判断
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
    # 根据门判断
    if door == '景门':
        advice_list.append("✅ 景门当值，注重证据和事实，准备充分")
    elif door == '杜门':
        advice_list.append("⚠️ 杜门当前，诉讼过程可能有阻碍，需耐心")
    elif door == '惊门':
        advice_list.append("⚠️ 惊门临位，可能有意外情况，需谨慎应对")
    elif door == '死门':
        advice_list.append("🔴 死门当前，诉讼结果可能不利")
    # 根据星判断
    if star == '天柱':
        advice_list.append("⚠️ 天柱星照，注意口舌是非，避免情绪化")
    elif star == '天心':
        advice_list.append("✅ 天心星现，思维清晰，利于法律事务")
    # 根据神判断
    if god == '值符':
        advice_list.append("✅ 值符护佑，有官方支持或贵人相助")
    elif god == '腾蛇':
        advice_list.append("⚠️ 腾蛇临位，事情多变，需灵活应对")
    elif god == '白虎':
        advice_list.append("🔴 白虎当头，压力大，注意对方攻击性")
    
    return advice_list

def get_travel_prediction(pan, door, god):
    """获取出行安全预测建议"""
    advice_list = []
    # 查找天冲星位置
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天冲':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"✅ 天冲星在{pos}宫({direction})，这个方向出行较顺利")
            break
    # 查找伤门位置
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '伤门':
            direction = convert_gong_to_direction(pos)
            advice_list.append(f"⚠️ 伤门在{pos}宫({direction})，这个方位需注意安全")
            break
    # 根据门判断
    if door == '开门':
        advice_list.append("✅ 开门当值，出行顺利，可以尝试新路线")
    elif door == '休门':
        advice_list.append("✅ 休门当前，适合休闲旅行，放松心情")
    elif door == '死门':
        advice_list.append("🔴 死门当前，出行需特别谨慎，避免长途")
    elif door == '伤门':
        advice_list.append("⚠️ 伤门临位，注意交通安全，避免意外")
    # 根据神判断
    if god == '太阴':
        advice_list.append("✅ 太阴守护，适合隐秘出行，低调行事")
    elif god == '白虎':
        advice_list.append("🔴 白虎当头，出行风险较大，需做好安全措施")
    elif god == '六合':
        advice_list.append("✅ 六合护佑，适合结伴出行，互相照应")
    
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
    if season == '春':
        advice_list.append("🌱 春季生机勃勃，是开始新计划的好时机")
    elif season == '夏':
        advice_list.append("☀️ 夏季炎热，做事需冷静，避免急躁")
    elif season == '秋':
        advice_list.append("🍂 秋季收获，也是反思总结的好时机")
    elif season == '冬':
        advice_list.append("❄️ 冬季收藏，适合养精蓄锐，等待时机")
    
    if yinyang == '阳':
        advice_list.append("☀️ 阳遁当前，主动出击效果更好")
    else:
        advice_list.append("🌙 阴遁当前，保守等待更为有利")
    return advice_list

def get_detailed_love_prediction(pan, yongshen_info):
    """详细的感情预测分析"""
    analysis = "💖 详细感情预测：\n\n"
    # 查找六合位置
    liuhe_pos = None
    for pos in jiugong:
        if pan.get('神盘', {}).get(pos) == '六合':
            liuhe_pos = pos
            break
    
    if liuhe_pos:
        direction = convert_gong_to_direction(liuhe_pos)
        analysis += f"✅ 六合（婚姻缘分）在{liuhe_pos}宫({direction})，说明：\n"
        analysis += f"   • 你的正缘可能出现在{direction}\n"
        time_desc = gong_to_time.get(liuhe_pos, '相关时间')
        analysis += f"   • 在{time_desc}更容易遇到合适的人\n"
    # 查找天芮星位置
    tianrui_pos = None
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天芮':
            tianrui_pos = pos
            break
    
    if tianrui_pos:
        direction = convert_gong_to_direction(tianrui_pos)
        analysis += f"⚠️ 天芮星（问题）在{tianrui_pos}宫({direction})，提示：\n"
        analysis += f"   • 感情中可能存在{direction}相关的问题\n"
        analysis += "   • 需要更多的沟通和理解\n"
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
    if season == '春':
        analysis += "   • 春季（2-4月）生机勃勃，适合开始新感情\n"
    elif season == '夏':
        analysis += "   • 夏季（5-7月）热情如火，感情容易升温\n"
    elif season == '秋':
        analysis += "   • 秋季（8-10月）收获季节，适合确定关系\n"
    elif season == '冬':
        analysis += "   • 冬季（11-1月）收藏时节，适合培养感情\n"
    # 根据门判断
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = convert_gong_to_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        
        if door == '开门':
            analysis += f"\n💌 表白建议（{direction}）：\n"
            analysis += "   • 当前开门当值，适合直接表白\n"
            analysis += "   • 选择公开场合或共同朋友见证\n"
            analysis += "   • 真诚表达自己的感受\n"
        elif door == '休门':
            analysis += f"\n💌 表白建议（{direction}）：\n"
            analysis += "   • 当前休门当值，适合低调表白\n"
            analysis += "   • 选择安静私密的场合\n"
            analysis += "   • 给对方足够的考虑时间\n"
        elif door == '景门':
            analysis += f"\n💌 表白建议（{direction}）：\n"
            analysis += "   • 当前景门当值，适合浪漫表白\n"
            analysis += "   • 准备有意义的礼物或惊喜\n"
            analysis += "   • 创造美好的回忆\n"
        elif door == '惊门':
            analysis += f"\n💌 表白建议（{direction}）：\n"
            analysis += "   • 当前惊门当值，表白需谨慎\n"
            analysis += "   • 避免在情绪激动时表白\n"
            analysis += "   • 准备好应对可能的拒绝\n"
    
    return analysis

def get_detailed_career_prediction(pan, yongshen_info):
    """详细的事业预测分析"""
    analysis = "💼 详细事业预测：\n\n"
    # 查找开门位置
    kaimen_pos = None
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '开门':
            kaimen_pos = pos
            break
    
    if kaimen_pos:
        direction = convert_gong_to_direction(kaimen_pos)
        analysis += f"✅ 开门（事业机会）在{kaimen_pos}宫({direction})，说明：\n"
        analysis += f"   • 事业发展机会在{direction}\n"
        time_desc = gong_to_time.get(kaimen_pos, '相关时间')
        analysis += f"   • 在{time_desc}更容易成功\n"
    # 查找生门位置
    shengmen_pos = None
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '生门':
            shengmen_pos = pos
            break
    
    if shengmen_pos:
        direction = convert_gong_to_direction(shengmen_pos)
        analysis += f"💰 生门（财运）在{shengmen_pos}宫({direction})，说明：\n"
        analysis += f"   • 财运机会在{direction}\n"
        analysis += "   • 适合投资或创业\n"
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
        analysis += "   • 当前阳遁，适合主动寻求机会\n"
        analysis += "   • 可以大胆尝试新领域\n"
    else:
        analysis += "   • 当前阴遁，适合等待合适时机\n"
        analysis += "   • 保守行事，稳固现有基础\n"
    # 根据值符值使判断
    zhifu = pan.get('值符', '')
    zhishi = pan.get('值使', '')
    analysis += f"\n👔 贵人提示：\n"
    analysis += f"   • 值符（{zhifu}）代表领导贵人\n"
    analysis += f"   • 值使（{zhishi}）代表执行贵人\n"
    analysis += "   • 多与相关人士沟通合作\n"
    
    return analysis

def get_detailed_wealth_prediction(pan, yongshen_info):
    """详细的财运预测分析"""
    analysis = "💰 详细财运预测：\n\n"
    # 查找生门位置
    shengmen_pos = None
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '生门':
            shengmen_pos = pos
            break
    
    if shengmen_pos:
        direction = convert_gong_to_direction(shengmen_pos)
        analysis += f"✅ 生门（财运）在{shengmen_pos}宫({direction})，说明：\n"
        analysis += f"   • 求财最佳方向是{direction}\n"
        time_desc = gong_to_time.get(shengmen_pos, '相关时间')
        analysis += f"   • 在{time_desc}财运最旺\n"
    # 查找开门位置
    kaimen_pos = None
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '开门':
            kaimen_pos = pos
            break
    
    if kaimen_pos:
        direction = convert_gong_to_direction(kaimen_pos)
        analysis += f"🚪 开门（机会）在{kaimen_pos}宫({direction})，说明：\n"
        analysis += f"   • 合作机会在{direction}\n"
        analysis += "   • 适合开展新业务或合作\n"
    # 查找戊土位置
    wutu_pos = None
    for pos in jiugong:
        if pan.get('地盘', {}).get(pos) == '戊':
            wutu_pos = pos
            break
    
    if wutu_pos:
        direction = convert_gong_to_direction(wutu_pos)
        analysis += f"💵 戊土（钱财）在{wutu_pos}宫({direction})，说明：\n"
        analysis += f"   • 钱财与{direction}相关\n"
        analysis += "   • 注意财务管理和投资方向\n"
    # 投资建议
    analysis += "\n📈 投资建议：\n"
    # 根据季节判断
    solar_term = pan.get('基本信息', {}).get('节气', '')
    season = get_current_season(solar_term)
    
    if season == '春':
        analysis += "   • 春季适合投资新兴行业\n"
        analysis += "   • 可考虑科技、教育等领域\n"
    elif season == '夏':
        analysis += "   • 夏季适合短期投资\n"
        analysis += "   • 注意风险控制，及时止盈\n"
    elif season == '秋':
        analysis += "   • 秋季适合收获投资\n"
        analysis += "   • 可以考虑套现部分收益\n"
    elif season == '冬':
        analysis += "   • 冬季适合保守投资\n"
        analysis += "   • 养精蓄锐，等待来年机会\n"
    # 根据门判断
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = convert_gong_to_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        
        if door == '生门':
            analysis += f"\n🎯 当前时机（{direction}）：\n"
            analysis += "   • 生门当值，财运亨通\n"
            analysis += "   • 可以适当增加投资\n"
            analysis += "   • 把握机会，但勿贪心\n"
        elif door == '休门':
            analysis += f"\n🎯 当前时机（{direction}）：\n"
            analysis += "   • 休门当前，财运平缓\n"
            analysis += "   • 不宜大额投资\n"
            analysis += "   • 适合观望和准备\n"
        elif door == '死门':
            analysis += f"\n🎯 当前时机（{direction}）：\n"
            analysis += "   • 死门当前，财运不佳\n"
            analysis += "   • 避免高风险投资\n"
            analysis += "   • 守住本金，等待时机\n"
    
    return analysis

def get_detailed_study_prediction(pan, yongshen_info):
    """详细的学习预测分析"""
    analysis = "📚 详细学习预测：\n\n"
    # 查找天辅星位置
    tianfu_pos = None
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天辅':
            tianfu_pos = pos
            break
    
    if tianfu_pos:
        direction = convert_gong_to_direction(tianfu_pos)
        analysis += f"✅ 天辅星（文曲星）在{tianfu_pos}宫({direction})，说明：\n"
        analysis += f"   • 学习最佳方位是{direction}\n"
        time_desc = gong_to_time.get(tianfu_pos, '相关时间')
        analysis += f"   • 在{time_desc}学习效果最好\n"
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
    
    if season == '春':
        analysis += "   • 春季适合开始新的学习计划\n"
        analysis += "   • 记忆力较好，吸收能力强\n"
    elif season == '夏':
        analysis += "   • 夏季适合强化训练\n"
        analysis += "   • 注意防暑，保持良好状态\n"
    elif season == '秋':
        analysis += "   • 秋季适合复习总结\n"
        analysis += "   • 思维清晰，适合应试\n"
    elif season == '冬':
        analysis += "   • 冬季适合深入学习\n"
        analysis += "   • 专注力强，适合攻克难点\n"
    # 根据门判断
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = convert_gong_to_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        
        if door == '景门':
            analysis += f"\n🎯 考试建议（{direction}）：\n"
            analysis += "   • 景门当值，考试发挥好\n"
            analysis += "   • 但需注意细节，避免粗心\n"
            analysis += "   • 答题时保持冷静\n"
        elif door == '杜门':
            analysis += f"\n🎯 考试建议（{direction}）：\n"
            analysis += "   • 杜门当前，思路可能不畅\n"
            analysis += "   • 需要多复习，打好基础\n"
            analysis += "   • 考试时先易后难\n"
        elif door == '开门':
            analysis += f"\n🎯 考试建议（{direction}）：\n"
            analysis += "   • 开门当值，新的考试机会\n"
            analysis += "   • 可以尝试新的考试类型\n"
            analysis += "   • 开放心态，接受挑战\n"
    # 学习方法建议
    analysis += "\n💡 学习方法建议：\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = convert_gong_to_direction(gong)
        
        if gong in ['离', '震']:
            analysis += f"   • {direction}学习效果更好\n"
            analysis += "   • 早上学习效率较高\n"
        elif gong in ['乾', '兑']:
            analysis += f"   • {direction}适合学习\n"
            analysis += "   • 下午或晚上思维更清晰\n"
        elif gong in ['坎']:
            analysis += f"   • {direction}适合深入学习\n"
            analysis += "   • 夜间学习效果较好\n"
    
    return analysis

def get_detailed_health_prediction(pan, yongshen_info):
    """详细的健康预测分析"""
    analysis = "💊 详细健康预测：\n\n"
    # 查找天芮星位置
    tianrui_pos = None
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天芮':
            tianrui_pos = pos
            break
    
    if tianrui_pos:
        direction = convert_gong_to_direction(tianrui_pos)
        analysis += f"⚠️ 病星天芮在{tianrui_pos}宫({direction})，说明：\n"
        analysis += f"   • 健康问题与{direction}相关\n"
        time_desc = gong_to_time.get(tianrui_pos, '相关时间')
        analysis += f"   • 在{time_desc}症状可能加重\n"
    # 查找天心星位置
    tianxin_pos = None
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天心':
            tianxin_pos = pos
            break
    
    if tianxin_pos:
        direction = convert_gong_to_direction(tianxin_pos)
        analysis += f"✅ 医星天心在{tianxin_pos}宫({direction})，说明：\n"
        analysis += f"   • 医疗资源在{direction}更有效\n"
        analysis += "   • 治疗效果较好，康复顺利\n"
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
    
    if season == '春':
        analysis += "   • 春季养肝，注意肝脏和神经系统\n"
        analysis += "   • 多吃绿色蔬菜，适度运动\n"
    elif season == '夏':
        analysis += "   • 夏季养心，注意心血管系统\n"
        analysis += "   • 防暑降温，保持心情舒畅\n"
    elif season == '秋':
        analysis += "   • 秋季养肺，注意呼吸系统\n"
        analysis += "   • 防燥润肺，多吃梨、百合\n"
    elif season == '冬':
        analysis += "   • 冬季养肾，注意泌尿系统\n"
        analysis += "   • 保暖防寒，适当进补\n"
    # 根据门判断
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = convert_gong_to_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        
        if door == '休门':
            analysis += f"\n🛏️ 休养建议（{direction}）：\n"
            analysis += "   • 休门当值，需要充分休息\n"
            analysis += "   • 避免劳累，保证睡眠\n"
            analysis += "   • 适当静养，不宜剧烈运动\n"
        elif door == '生门':
            analysis += f"\n🛏️ 休养建议（{direction}）：\n"
            analysis += "   • 生门当值，康复能力较强\n"
            analysis += "   • 可进行温和的康复训练\n"
            analysis += "   • 保持乐观心态\n"
        elif door == '死门':
            analysis += f"\n🛏️ 休养建议（{direction}）：\n"
            analysis += "   • 死门当前，病情需重视\n"
            analysis += "   • 及时就医，不可拖延\n"
            analysis += "   • 遵医嘱，系统治疗\n"
        elif door == '伤门':
            analysis += f"\n🛏️ 休养建议（{direction}）：\n"
            analysis += "   • 伤门临位，注意意外伤害\n"
            analysis += "   • 避免危险活动\n"
            analysis += "   • 如有手术，选择吉日\n"
    # 养生方法
    analysis += "\n🌿 养生方法建议：\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        
        if gong in gong_to_organ:
            analysis += f"   • 重点调理：{gong_to_organ[gong]}\n"
        
        if gong in ['离', '震']:
            analysis += "   • 东方养生法：晨练、绿色饮食\n"
            analysis += "   • 木属性食物：蔬菜、水果\n"
        elif gong in ['乾', '兑']:
            analysis += "   • 西方养生法：深呼吸、白色食物\n"
            analysis += "   • 金属性食物：梨、百合、杏仁\n"
        elif gong in ['坎']:
            analysis += "   • 北方养生法：充足睡眠、黑色食物\n"
            analysis += "   • 水属性食物：黑豆、黑芝麻\n"
        elif gong in ['坤', '艮', '中']:
            analysis += "   • 中央养生法：均衡饮食、黄色食物\n"
            analysis += "   • 土属性食物：山药、小米、南瓜\n"
    
    return analysis

def get_detailed_lawsuit_prediction(pan, yongshen_info):
    """详细的官司诉讼预测分析"""
    analysis = "⚖️ 详细官司诉讼预测：\n\n"
    # 查找值符位置
    zhifu_pos = None
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == pan.get('值符', ''):
            zhifu_pos = pos
            break
    
    if zhifu_pos:
        direction = convert_gong_to_direction(zhifu_pos)
        analysis += f"⭐ 值符（法官/裁决者）在{zhifu_pos}宫({direction})，说明：\n"
        analysis += f"   • 司法资源或法官态度在{direction}有利\n"
        analysis += "   • 寻求官方渠道解决更有效\n"
    # 查找天柱星位置（主口舌是非）
    tianzhu_pos = None
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天柱':
            tianzhu_pos = pos
            break
    
    if tianzhu_pos:
        direction = convert_gong_to_direction(tianzhu_pos)
        analysis += f"⚠️ 天柱星（口舌）在{tianzhu_pos}宫({direction})，提示：\n"
        analysis += f"   • 争议焦点与{direction}相关\n"
        analysis += "   • 注意法律文书的准确性\n"
        analysis += "   • 避免口头承诺，以书面为准\n"
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
        
        if door == '景门':
            analysis += f"\n💼 诉讼策略（{direction}）：\n"
            analysis += "   • 景门当值，注重证据和事实\n"
            analysis += "   • 准备充分的书面材料\n"
            analysis += "   • 逻辑清晰，条理分明\n"
        elif door == '杜门':
            analysis += f"\n💼 诉讼策略（{direction}）：\n"
            analysis += "   • 杜门当前，可能遇到程序障碍\n"
            analysis += "   • 耐心等待，不要急于求成\n"
            analysis += "   • 寻求专业人士帮助\n"
        elif door == '惊门':
            analysis += f"\n💼 诉讼策略（{direction}）：\n"
            analysis += "   • 惊门当值，可能有意外情况\n"
            analysis += "   • 做好多手准备\n"
            analysis += "   • 保持冷静，避免情绪化\n"
    # 和解建议
    analysis += "\n🤝 和解建议：\n"
    # 查找六合位置
    liuhe_pos = None
    for pos in jiugong:
        if pan.get('神盘', {}).get(pos) == '六合':
            liuhe_pos = pos
            break
    
    if liuhe_pos:
        direction = convert_gong_to_direction(liuhe_pos)
        analysis += f"   • 六合在{liuhe_pos}宫({direction})，和解机会存在\n"
        analysis += f"   • 通过{direction}的中间人调解\n"
        analysis += "   • 考虑妥协方案，避免两败俱伤\n"
    else:
        analysis += "   • 当前和解机会较小，需做好诉讼准备\n"
    
    return analysis

def get_detailed_travel_prediction(pan, yongshen_info):
    """详细的出行安全预测分析"""
    analysis = "✈️ 详细出行安全预测：\n\n"
    # 查找天冲星位置（主出行）
    tianchong_pos = None
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天冲':
            tianchong_pos = pos
            break
    
    if tianchong_pos:
        direction = convert_gong_to_direction(tianchong_pos)
        analysis += f"🚗 天冲星（出行）在{tianchong_pos}宫({direction})，说明：\n"
        analysis += f"   • 出行方向以{direction}较佳\n"
        time_desc = gong_to_time.get(tianchong_pos, '相关时间')
        analysis += f"   • 在{time_desc}出行更顺利\n"
    # 查找伤门位置（主伤害）
    shangmen_pos = None
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '伤门':
            shangmen_pos = pos
            break
    
    if shangmen_pos:
        direction = convert_gong_to_direction(shangmen_pos)
        analysis += f"⚠️ 伤门（伤害）在{shangmen_pos}宫({direction})，提示：\n"
        analysis += f"   • {direction}需注意安全\n"
        analysis += "   • 避免高风险活动\n"
        analysis += "   • 注意交通安全\n"
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
        
        if door == '开门':
            analysis += f"\n🎯 出行建议（{direction}）：\n"
            analysis += "   • 开门当值，出行顺利\n"
            analysis += "   • 可以尝试新的路线\n"
            analysis += "   • 与人结伴同行更佳\n"
        elif door == '休门':
            analysis += f"\n🎯 出行建议（{direction}）：\n"
            analysis += "   • 休门当值，适合休闲旅行\n"
            analysis += "   • 不要安排过于紧凑的行程\n"
            analysis += "   • 注重休息，享受过程\n"
        elif door == '死门':
            analysis += f"\n🎯 出行建议（{direction}）：\n"
            analysis += "   • 死门当前，出行需谨慎\n"
            analysis += "   • 尽量避免长途旅行\n"
            analysis += "   • 做好应急准备\n"
    # 交通工具选择
    analysis += "\n🚗 交通工具选择：\n"
    # 根据宫位判断
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = convert_gong_to_direction(gong)
        
        if gong in ['乾', '兑']:
            analysis += f"   • {direction}金属类交通工具（飞机、高铁）较安全\n"
            analysis += f"   • {direction}的交通更顺利\n"
        elif gong in ['离', '震']:
            analysis += f"   • {direction}火类交通工具（汽车、火车）较合适\n"
            analysis += f"   • {direction}的交通更顺利\n"
        elif gong in ['坎']:
            analysis += f"   • {direction}水类交通工具（船舶）需谨慎\n"
            analysis += f"   • {direction}的交通需注意安全\n"
        elif gong in ['坤', '艮', '中']:
            analysis += f"   • {direction}陆地交通工具较安全\n"
            analysis += f"   • {direction}较顺利\n"
    # 安全注意事项
    analysis += "\n🔒 安全注意事项：\n"
    # 查找白虎位置
    baihu_pos = None
    for pos in jiugong:
        if pan.get('神盘', {}).get(pos) == '白虎':
            baihu_pos = pos
            break
    
    if baihu_pos:
        direction = convert_gong_to_direction(baihu_pos)
        analysis += f"   • 白虎在{baihu_pos}宫({direction})，该方位可能有风险\n"
        analysis += "   • 避免夜间单独出行\n"
        analysis += "   • 保管好贵重物品\n"
    # 查找太阴位置
    taiyin_pos = None
    for pos in jiugong:
        if pan.get('神盘', {}).get(pos) == '太阴':
            taiyin_pos = pos
            break
    
    if taiyin_pos:
        direction = convert_gong_to_direction(taiyin_pos)
        analysis += f"   • 太阴在{taiyin_pos}宫({direction})，适合隐秘出行\n"
        analysis += "   • 低调行事，避免张扬\n"
    
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
            advice_list = get_love_prediction(pan,  door, star, god)
        elif question_type == "工作事业":
            advice_list = get_career_prediction(pan, door, star, god)
        elif question_type == "财运求财":
            advice_list = get_wealth_prediction(pan, door)
        elif question_type == "考试学习":
            advice_list = get_study_prediction(pan, door, star, god)
        elif question_type == "疾病健康":
            advice_list = get_health_prediction(pan, gong, door, star)
        elif question_type == "官司诉讼":
            advice_list = get_lawsuit_prediction(pan,  door, star, god)
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