"""
预测分析模块
包含各类问题的详细预测分析功能
"""

from data import *
from yuce_utils import *
from yuce_yongshen import get_current_season

def get_love_prediction(pan, gong, door, star, god):
    """获取感情预测建议"""
    advice_list = []
    
    # 查找六合位置
    for pos in jiugong:
        if pan.get('神盘', {}).get(pos) == '六合':
            advice_list.append(f"✅ 六合在{pos}宫，这个方位或方向利于感情发展")
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

def get_career_prediction(pan, gong, door, star, god):
    """获取事业预测建议"""
    advice_list = []
    
    # 查找开门位置
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '开门':
            advice_list.append(f"✅ 开门在{pos}宫，事业发展机会在这个方向")
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

def get_wealth_prediction(pan, gong, door, star, god):
    """获取财运预测建议"""
    advice_list = []
    
    # 查找生门位置
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '生门':
            advice_list.append(f"✅ 生门在{pos}宫，求财往这个方向或方位有利")
            break
    
    # 查找开门位置
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '开门':
            advice_list.append(f"✅ 开门在{pos}宫，合作或新项目可考虑这个方向")
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
            advice_list.append(f"💰 戊土在{pos}宫，钱财与这个方位相关")
            break
    
    return advice_list

def get_study_prediction(pan, gong, door, star, god):
    """获取学习预测建议"""
    advice_list = []
    
    # 查找天辅星位置（文曲星）
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天辅':
            advice_list.append(f"✅ 文昌星天辅在{pos}宫，在这个方位学习效果更好")
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

def get_health_prediction(pan, gong, door, star, god):
    """获取健康预测建议"""
    advice_list = []
    
    # 查找天芮星位置（病星）
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天芮':
            advice_list.append(f"⚠️ 病星天芮在{pos}宫，注意相关脏腑健康")
            break
    
    # 查找天心星位置（医星）
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天心':
            advice_list.append(f"✅ 医星天心在{pos}宫，治疗可往这个方向寻找")
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
        analysis += f"✅ 六合（婚姻缘分）在{liuhe_pos}宫，说明：\n"
        analysis += f"   • 你的正缘可能出现在{liuhe_pos}方位\n"
        analysis += f"   • 在{gong_to_time.get(liuhe_pos, '相关时间')}更容易遇到合适的人\n"
    
    # 查找天芮星位置
    tianrui_pos = None
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天芮':
            tianrui_pos = pos
            break
    
    if tianrui_pos:
        analysis += f"⚠️ 天芮星（问题）在{tianrui_pos}宫，提示：\n"
        analysis += f"   • 感情中可能存在{tianrui_pos}宫对应的问题\n"
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
        door = pan.get('人盘', {}).get(gong, '')
        
        if door == '开门':
            analysis += "\n💌 表白建议：\n"
            analysis += "   • 当前开门当值，适合直接表白\n"
            analysis += "   • 选择公开场合或共同朋友见证\n"
            analysis += "   • 真诚表达自己的感受\n"
        elif door == '休门':
            analysis += "\n💌 表白建议：\n"
            analysis += "   • 当前休门当值，适合低调表白\n"
            analysis += "   • 选择安静私密的场合\n"
            analysis += "   • 给对方足够的考虑时间\n"
        elif door == '景门':
            analysis += "\n💌 表白建议：\n"
            analysis += "   • 当前景门当值，适合浪漫表白\n"
            analysis += "   • 准备有意义的礼物或惊喜\n"
            analysis += "   • 创造美好的回忆\n"
        elif door == '惊门':
            analysis += "\n💌 表白建议：\n"
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
        analysis += f"✅ 开门（事业机会）在{kaimen_pos}宫，说明：\n"
        analysis += f"   • 事业发展机会在{kaimen_pos}方位\n"
        analysis += f"   • 在{gong_to_time.get(kaimen_pos, '相关时间')}更容易成功\n"
    
    # 查找生门位置
    shengmen_pos = None
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '生门':
            shengmen_pos = pos
            break
    
    if shengmen_pos:
        analysis += f"💰 生门（财运）在{shengmen_pos}宫，说明：\n"
        analysis += f"   • 财运机会在{shengmen_pos}方位\n"
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
        analysis += f"✅ 生门（财运）在{shengmen_pos}宫，说明：\n"
        analysis += f"   • 求财最佳方向是{shengmen_pos}方位\n"
        analysis += f"   • 在{gong_to_time.get(shengmen_pos, '相关时间')}财运最旺\n"
    
    # 查找开门位置
    kaimen_pos = None
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '开门':
            kaimen_pos = pos
            break
    
    if kaimen_pos:
        analysis += f"🚪 开门（机会）在{kaimen_pos}宫，说明：\n"
        analysis += f"   • 合作机会在{kaimen_pos}方位\n"
        analysis += "   • 适合开展新业务或合作\n"
    
    # 查找戊土位置
    wutu_pos = None
    for pos in jiugong:
        if pan.get('地盘', {}).get(pos) == '戊':
            wutu_pos = pos
            break
    
    if wutu_pos:
        analysis += f"💵 戊土（钱财）在{wutu_pos}宫，说明：\n"
        analysis += f"   • 钱财与{wutu_pos}方位相关\n"
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
        door = pan.get('人盘', {}).get(gong, '')
        
        if door == '生门':
            analysis += "\n🎯 当前时机：\n"
            analysis += "   • 生门当值，财运亨通\n"
            analysis += "   • 可以适当增加投资\n"
            analysis += "   • 把握机会，但勿贪心\n"
        elif door == '休门':
            analysis += "\n🎯 当前时机：\n"
            analysis += "   • 休门当前，财运平缓\n"
            analysis += "   • 不宜大额投资\n"
            analysis += "   • 适合观望和准备\n"
        elif door == '死门':
            analysis += "\n🎯 当前时机：\n"
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
        analysis += f"✅ 天辅星（文曲星）在{tianfu_pos}宫，说明：\n"
        analysis += f"   • 学习最佳方位是{tianfu_pos}方向\n"
        analysis += f"   • 在{gong_to_time.get(tianfu_pos, '相关时间')}学习效果最好\n"
    
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
        door = pan.get('人盘', {}).get(gong, '')
        
        if door == '景门':
            analysis += "\n🎯 考试建议：\n"
            analysis += "   • 景门当值，考试发挥好\n"
            analysis += "   • 但需注意细节，避免粗心\n"
            analysis += "   • 答题时保持冷静\n"
        elif door == '杜门':
            analysis += "\n🎯 考试建议：\n"
            analysis += "   • 杜门当前，思路可能不畅\n"
            analysis += "   • 需要多复习，打好基础\n"
            analysis += "   • 考试时先易后难\n"
        elif door == '开门':
            analysis += "\n🎯 考试建议：\n"
            analysis += "   • 开门当值，新的考试机会\n"
            analysis += "   • 可以尝试新的考试类型\n"
            analysis += "   • 开放心态，接受挑战\n"
    
    # 学习方法建议
    analysis += "\n💡 学习方法建议：\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        
        if gong in ['离', '震']:
            analysis += "   • 东方或南方学习效果更好\n"
            analysis += "   • 早上学习效率较高\n"
        elif gong in ['乾', '兑']:
            analysis += "   • 西方或西北方适合学习\n"
            analysis += "   • 下午或晚上思维更清晰\n"
        elif gong in ['坎']:
            analysis += "   • 北方适合深入学习\n"
            analysis += "   • 夜间学习效果较好\n"
    
    return analysis

def predict_timing(pan, yongshen_info, question_type):
    """预测应期祸福"""
    timing_analysis = f"【详细分析】\n\n"    
    # 获取基本信息
    ju_shu = pan.get('基本信息', {}).get('局数', '')
    yinyang = pan.get('基本信息', {}).get('阴阳遁', '')
    zhifu = pan.get('值符', '')
    zhishi = pan.get('值使', '')    
    timing_analysis += f"当前为{yinyang}遁{ju_shu}局，值符（领导）：{zhifu}，值使（执行）：{zhishi}\n\n"
    
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
        
        timing_analysis += f"1. 你的状态：用神在{gong}宫\n"
        
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
            advice_list = get_love_prediction(pan, gong, door, star, god)
        elif question_type == "工作事业":
            advice_list = get_career_prediction(pan, gong, door, star, god)
        elif question_type == "财运求财":
            advice_list = get_wealth_prediction(pan, gong, door, star, god)
        elif question_type == "考试学习":
            advice_list = get_study_prediction(pan, gong, door, star, god)
        elif question_type == "疾病健康":
            advice_list = get_health_prediction(pan, gong, door, star, god)
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
    
    # 最后的实用提醒
    timing_analysis += "\n" + "="*50 + "\n"
    timing_analysis += "【重要提醒】\n"
    timing_analysis += "• 以上分析基于今日排盘，明日盘局变化，建议也会不同\n"
    timing_analysis += "• 真正的决策还需结合实际情况和个人判断\n"
    timing_analysis += "• 命运掌握在自己手中，积极行动才是最好的策略\n"
    timing_analysis += "="*50
    
    return timing_analysis