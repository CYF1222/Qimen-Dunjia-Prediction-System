"""
预测分析模块
包含各类问题的详细预测分析功能
优化版：配置驱动，减少重复代码
"""

from data import *
from yuce_utils import *
from yuce_yongshen import get_current_season


# ==================== 工具函数 ====================
def _find_first(pan, layer, symbol):
    """在指定盘中查找第一个匹配符号的宫位"""
    for pos in jiugong:
        if pan.get(layer, {}).get(pos) == symbol:
            return pos
    return None


def _get_direction(pos):
    return convert_gong_to_direction(pos) if pos else "未知"


def _get_time_desc(pos):
    return gong_to_time.get(pos, "相关时间") if pos else ""


# ==================== 基础建议获取（保留原有逻辑，但用配置表） ====================
# 各个问题类型的建议生成函数（统一接口：接收 pan, door, star, god, gong 等）
def _get_advice_by_type(question_type, pan, door, star, god, gong):
    """根据问题类型返回建议列表"""
    if question_type == "婚姻感情":
        return _get_love_advice(pan, door, star, god)
    elif question_type == "工作事业":
        return _get_career_advice(pan, door, star, god)
    elif question_type == "财运求财":
        return _get_wealth_advice(pan, door)
    elif question_type == "考试学习":
        return _get_study_advice(pan, door, star, god)
    elif question_type == "疾病健康":
        return _get_health_advice(pan, gong, door, star)
    elif question_type == "官司诉讼":
        return _get_lawsuit_advice(pan, door, star, god)
    elif question_type == "出行安全":
        return _get_travel_advice(pan, door, god)
    else:
        return _get_general_advice(door, star, god)


# ---- 各类型建议实现（保持原有逻辑，但用辅助函数简化） ----
def _get_love_advice(pan, door, star, god):
    advice = []
    pos = _find_first(pan, '神盘', '六合')
    if pos:
        advice.append(f"✅ 六合在{pos}宫({_get_direction(pos)})，这个方位利于感情发展")
    advice.extend(love_advice.get('door', {}).get(door, []))  # 假设为列表，若为字符串则单独处理
    # 注意：原有数据是字符串，我们统一转为列表处理，方便扩展
    for key in ['door', 'star', 'god']:
        d = {'door': door, 'star': star, 'god': god}
        val = d.get(key)
        if val:
            item = love_advice.get(key, {}).get(val)
            if item:
                advice.append(item)
    return advice


def _get_career_advice(pan, door, star, god):
    advice = []
    pos = _find_first(pan, '人盘', '开门')
    if pos:
        advice.append(f"✅ 开门在{pos}宫({_get_direction(pos)})，事业发展机会在这个方向")
    for key in ['door', 'star', 'god']:
        d = {'door': door, 'star': star, 'god': god}
        val = d.get(key)
        if val:
            item = career_advice.get(key, {}).get(val)
            if item:
                advice.append(item)
    return advice


def _get_wealth_advice(pan, door):
    advice = []
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '生门':
            advice.append(f"✅ 生门在{pos}宫({_get_direction(pos)})，求财往这个方向有利")
        if pan.get('人盘', {}).get(pos) == '开门':
            advice.append(f"✅ 开门在{pos}宫({_get_direction(pos)})，合作或新项目可考虑这个方向")
    # 财运建议（门）
    if door in wealth_advice.get('door', {}):
        advice.append(wealth_advice['door'][door])
    # 找戊土
    pos = _find_first(pan, '地盘', '戊')
    if pos:
        advice.append(f"💰 戊土在{pos}宫({_get_direction(pos)})，钱财与这个方位相关")
    return advice


def _get_study_advice(pan, door, star, god):
    advice = []
    pos = _find_first(pan, '天盘', '天辅')
    if pos:
        advice.append(f"✅ 文昌星天辅在{pos}宫({_get_direction(pos)})，在这个方位学习效果更好")
    for key in ['star', 'door', 'god']:
        d = {'star': star, 'door': door, 'god': god}
        val = d.get(key)
        if val:
            item = study_advice.get(key, {}).get(val)
            if item:
                advice.append(item)
    return advice


def _get_health_advice(pan, gong, door, star):
    advice = []
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天芮':
            advice.append(f"⚠️ 病星天芮在{pos}宫({_get_direction(pos)})，注意相关脏腑健康")
        if pan.get('天盘', {}).get(pos) == '天心':
            advice.append(f"✅ 医星天心在{pos}宫({_get_direction(pos)})，治疗可往这个方向寻找")
    if door in health_advice.get('door', {}):
        advice.append(health_advice['door'][door])
    if star == '天芮':
        advice.append("⚠️ 当前有天芮星照，需特别注意健康问题")
    elif star == '天心':
        advice.append("✅ 天心星现，医疗效果较好，康复顺利")
    if gong in gong_to_organ:
        advice.append(f"📍 当前宫位对应：{gong_to_organ[gong]}")
    return advice


def _get_lawsuit_advice(pan, door, star, god):
    advice = []
    zhifu = pan.get('值符', '')
    pos = _find_first(pan, '天盘', zhifu)
    if pos:
        advice.append(f"✅ 值符在{pos}宫({_get_direction(pos)})，这个方位寻求司法帮助更有效")
    for key in ['door', 'star', 'god']:
        d = {'door': door, 'star': star, 'god': god}
        val = d.get(key)
        if val:
            item = lawsuit_advice.get(key, {}).get(val)
            if item:
                advice.append(item)
    return advice


def _get_travel_advice(pan, door, god):
    advice = []
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天冲':
            advice.append(f"✅ 天冲星在{pos}宫({_get_direction(pos)})，这个方向出行较顺利")
        if pan.get('人盘', {}).get(pos) == '伤门':
            advice.append(f"⚠️ 伤门在{pos}宫({_get_direction(pos)})，这个方位需注意安全")
    if door in travel_advice.get('door', {}):
        advice.append(travel_advice['door'][door])
    if god in travel_advice.get('god', {}):
        advice.append(travel_advice['god'][god])
    return advice


def _get_general_advice(door, star, god):
    advice = []
    if door in ji_gates:
        advice.append("✅ 当前吉门当值，可以积极行动")
    elif door in xiong_gates:
        advice.append("⚠️ 当前凶门当值，需谨慎行事")
    if god in ji_gods:
        advice.append("✅ 吉神护佑，有贵人相助")
    elif god in xiong_gods:
        advice.append("⚠️ 凶神临位，需小心应对")
    if star in ['天辅', '天心', '天任']:
        advice.append("✅ 当前吉星当值，运势较为顺利")
    elif star in ['天芮', '天蓬']:
        advice.append("⚠️ 当前需要注意，可能有挑战")
    return advice


def add_general_suggestions(advice_list, yinyang, solar_term):
    """添加通用建议（原样保留，作为独立工具）"""
    season = get_current_season(solar_term)
    if season in general_suggestions.get('season', {}):
        advice_list.append(general_suggestions['season'][season])
    if yinyang in general_suggestions.get('yinyang', {}):
        advice_list.append(general_suggestions['yinyang'][yinyang])
    return advice_list


# ==================== 详细预测（重构成模板方法） ====================
def _build_detailed_base(pan, yongshen_info, title, find_pairs):
    """
    构造详细预测的通用框架
    :param pan: 盘数据
    :param yongshen_info: 用神信息
    :param title: 标题（如"💖 详细感情预测"）
    :param find_pairs: 列表，每个元素为 (查找盘层, 符号, 提示前缀, 额外描述函数)
    :return: 生成的文本
    """
    lines = [f"{title}\n"]
    # 第一部分：查找特定符号
    for layer, symbol, prefix, extra_func in find_pairs:
        pos = _find_first(pan, layer, symbol)
        if pos:
            direction = _get_direction(pos)
            time_desc = _get_time_desc(pos)
            lines.append(f"{prefix}在{pos}宫({direction})，说明：")
            lines.append(f"   • 这个方位是{direction}")
            if time_desc:
                lines.append(f"   • 在{time_desc}更有效")
            if extra_func:
                lines.append(f"   • {extra_func(pos, pan)}")
        else:
            lines.append(f"{prefix}未找到，可能影响较小")
    lines.append("")  # 空行

    # 第二部分：时间建议（用神宫位）
    lines.append("📅 最佳时机：")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = _get_time_desc(gong)
        if time_desc:
            lines.append(f"   • 在{time_desc}处理此事更有利")
        else:
            lines.append("   • 近期内即可行动")
    else:
        lines.append("   • 请先用神分析")
    lines.append("")

    # 第三部分：季节/阴阳遁等通用建议
    solar_term = pan.get('基本信息', {}).get('节气', '')
    season = get_current_season(solar_term)
    yinyang = pan.get('基本信息', {}).get('阴阳遁', '')
    # 可以在这里添加季节相关建议（由子类覆盖）
    lines.append("🌿 环境提示：")
    if season:
        lines.append(f"   • 当前季节：{season}")
    if yinyang:
        lines.append(f"   • 当前遁法：{yinyang}")
    lines.append("")

    return "\n".join(lines)


# ---- 各详细预测函数（使用模板 + 特定逻辑） ----
def get_detailed_love_prediction(pan, yongshen_info):
    lines = []
    # 六合
    pos = _find_first(pan, '神盘', '六合')
    if pos:
        direction = _get_direction(pos)
        time_desc = _get_time_desc(pos)
        lines.append("💖 详细感情预测：\n")
        lines.append(f"✅ 六合（婚姻缘分）在{pos}宫({direction})，说明：")
        lines.append(f"   • 你的正缘可能出现在{direction}")
        if time_desc:
            lines.append(f"   • 在{time_desc}更容易遇到合适的人")
    else:
        lines.append("💖 详细感情预测：\n未找到六合，缘分可能较隐蔽")

    # 天芮星（问题）
    pos = _find_first(pan, '天盘', '天芮')
    if pos:
        direction = _get_direction(pos)
        lines.append(f"⚠️ 天芮星（问题）在{pos}宫({direction})，提示：")
        lines.append(f"   • 感情中可能存在{direction}相关的问题")
        lines.append("   • 需要更多的沟通和理解")

    # 表白时机
    lines.append("\n📅 最佳表白时机：")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = _get_time_desc(gong)
        if time_desc:
            lines.append(f"   • 在{time_desc}表白效果更佳")
    solar_term = pan.get('基本信息', {}).get('节气', '')
    season = get_current_season(solar_term)
    if season in love_timing:
        lines.append(f"   • {love_timing[season]}")
    # 门建议
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = _get_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        if door in love_confession:
            lines.append(f"   • {love_confession[door].format(direction=direction)}")
    return "\n".join(lines)


def get_detailed_career_prediction(pan, yongshen_info):
    lines = ["💼 详细事业预测：\n"]
    # 开门
    pos = _find_first(pan, '人盘', '开门')
    if pos:
        direction = _get_direction(pos)
        time_desc = _get_time_desc(pos)
        lines.append(f"✅ 开门（事业机会）在{pos}宫({direction})，说明：")
        lines.append(f"   • 事业发展机会在{direction}")
        if time_desc:
            lines.append(f"   • 在{time_desc}更容易成功")
    # 生门
    pos = _find_first(pan, '人盘', '生门')
    if pos:
        direction = _get_direction(pos)
        lines.append(f"💰 生门（财运）在{pos}宫({direction})，说明：")
        lines.append(f"   • 财运机会在{direction}")
        lines.append("   • 适合投资或创业")

    # 工作变动时机
    lines.append("\n📅 最佳工作变动时机：")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = _get_time_desc(gong)
        if time_desc:
            lines.append(f"   • 在{time_desc}考虑变动更有利")
    yinyang = pan.get('基本信息', {}).get('阴阳遁', '')
    if yinyang == '阳遁':
        lines.append("   • 当前阳遁，适合主动寻求机会")
        lines.append("   • 可以大胆尝试新领域")
    else:
        lines.append("   • 当前阴遁，适合等待合适时机")
        lines.append("   • 保守行事，稳固现有基础")
    # 贵人
    zhifu = pan.get('值符', '')
    zhishi = pan.get('值使', '')
    lines.append(f"\n👔 贵人提示：")
    lines.append(f"   • 值符（{zhifu}）代表领导贵人")
    lines.append(f"   • 值使（{zhishi}）代表执行贵人")
    lines.append("   • 多与相关人士沟通合作")
    return "\n".join(lines)


def get_detailed_wealth_prediction(pan, yongshen_info):
    lines = ["💰 详细财运预测：\n"]
    # 生门、开门、戊土
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '生门':
            direction = _get_direction(pos)
            time_desc = _get_time_desc(pos)
            lines.append(f"✅ 生门（财运）在{pos}宫({direction})，说明：")
            lines.append(f"   • 求财最佳方向是{direction}")
            if time_desc:
                lines.append(f"   • 在{time_desc}财运最旺")
        if pan.get('人盘', {}).get(pos) == '开门':
            direction = _get_direction(pos)
            lines.append(f"🚪 开门（机会）在{pos}宫({direction})，说明：")
            lines.append(f"   • 合作机会在{direction}")
            lines.append("   • 适合开展新业务或合作")
    pos = _find_first(pan, '地盘', '戊')
    if pos:
        direction = _get_direction(pos)
        lines.append(f"💵 戊土（钱财）在{pos}宫({direction})，说明：")
        lines.append(f"   • 钱财与{direction}相关")
        lines.append("   • 注意财务管理和投资方向")

    # 投资建议
    lines.append("\n📈 投资建议：")
    solar_term = pan.get('基本信息', {}).get('节气', '')
    season = get_current_season(solar_term)
    if season in investment_advice:
        lines.append(f"   • {investment_advice[season]}")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = _get_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        if door in wealth_timing:
            lines.append(wealth_timing[door].format(direction=direction))
    return "\n".join(lines)


def get_detailed_study_prediction(pan, yongshen_info):
    lines = ["📚 详细学习预测：\n"]
    pos = _find_first(pan, '天盘', '天辅')
    if pos:
        direction = _get_direction(pos)
        time_desc = _get_time_desc(pos)
        lines.append(f"✅ 天辅星（文曲星）在{pos}宫({direction})，说明：")
        lines.append(f"   • 学习最佳方位是{direction}")
        if time_desc:
            lines.append(f"   • 在{time_desc}学习效果最好")
    lines.append("\n📅 最佳考试时间：")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = _get_time_desc(gong)
        if time_desc:
            lines.append(f"   • 在{time_desc}考试状态更佳")
    solar_term = pan.get('基本信息', {}).get('节气', '')
    season = get_current_season(solar_term)
    if season in study_season:
        lines.append(f"   • {study_season[season]}")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = _get_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        if door in study_suggestions:
            lines.append(study_suggestions[door].format(direction=direction))
    # 学习方法
    lines.append("\n💡 学习方法建议：")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = _get_direction(gong)
        if gong in study_methods:
            lines.append(study_methods[gong].format(direction=direction))
    return "\n".join(lines)


def get_detailed_health_prediction(pan, yongshen_info):
    lines = ["💊 详细健康预测：\n"]
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天芮':
            direction = _get_direction(pos)
            time_desc = _get_time_desc(pos)
            lines.append(f"⚠️ 病星天芮在{pos}宫({direction})，说明：")
            lines.append(f"   • 健康问题与{direction}相关")
            if time_desc:
                lines.append(f"   • 在{time_desc}症状可能加重")
        if pan.get('天盘', {}).get(pos) == '天心':
            direction = _get_direction(pos)
            lines.append(f"✅ 医星天心在{pos}宫({direction})，说明：")
            lines.append("   • 医疗资源在{direction}更有效")
            lines.append("   • 治疗效果较好，康复顺利")
    lines.append("\n📅 最佳治疗时机：")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = _get_time_desc(gong)
        if time_desc:
            lines.append(f"   • 在{time_desc}治疗效果更佳")
    solar_term = pan.get('基本信息', {}).get('节气', '')
    season = get_current_season(solar_term)
    if season in health_season:
        lines.append(f"   • {health_season[season]}")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = _get_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        if door in rest_advice:
            lines.append(rest_advice[door].format(direction=direction))
    # 养生
    lines.append("\n🌿 养生方法建议：")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        if gong in gong_to_organ:
            lines.append(f"   • 重点调理：{gong_to_organ[gong]}")
        if gong in health_methods:
            lines.append(health_methods[gong])
    return "\n".join(lines)


def get_detailed_lawsuit_prediction(pan, yongshen_info):
    lines = ["⚖️ 详细官司诉讼预测：\n"]
    zhifu = pan.get('值符', '')
    pos = _find_first(pan, '天盘', zhifu)
    if pos:
        direction = _get_direction(pos)
        lines.append(f"⭐ 值符（法官/裁决者）在{pos}宫({direction})，说明：")
        lines.append("   • 司法资源或法官态度在{direction}有利")
        lines.append("   • 寻求官方渠道解决更有效")
    pos = _find_first(pan, '天盘', '天柱')
    if pos:
        direction = _get_direction(pos)
        lines.append(f"⚠️ 天柱星（口舌）在{pos}宫({direction})，提示：")
        lines.append("   • 争议焦点与{direction}相关")
        lines.append("   • 注意法律文书的准确性")
        lines.append("   • 避免口头承诺，以书面为准")
    lines.append("\n📅 最佳解决时机：")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = _get_time_desc(gong)
        if time_desc:
            lines.append(f"   • 在{time_desc}处理法律事务更有利")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = _get_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        if door in lawsuit_strategy:
            lines.append(lawsuit_strategy[door].format(direction=direction))
    # 和解
    lines.append("\n🤝 和解建议：")
    pos = _find_first(pan, '神盘', '六合')
    if pos:
        direction = _get_direction(pos)
        lines.append(f"   • 六合在{pos}宫({direction})，和解机会存在")
        lines.append(f"   • 通过{direction}的中间人调解")
        lines.append("   • 考虑妥协方案，避免两败俱伤")
    else:
        lines.append("   • 当前和解机会较小，需做好诉讼准备")
    return "\n".join(lines)


def get_detailed_travel_prediction(pan, yongshen_info):
    lines = ["✈️ 详细出行安全预测：\n"]
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天冲':
            direction = _get_direction(pos)
            time_desc = _get_time_desc(pos)
            lines.append(f"🚗 天冲星（出行）在{pos}宫({direction})，说明：")
            lines.append(f"   • 出行方向以{direction}较佳")
            if time_desc:
                lines.append(f"   • 在{time_desc}出行更顺利")
        if pan.get('人盘', {}).get(pos) == '伤门':
            direction = _get_direction(pos)
            lines.append(f"⚠️ 伤门（伤害）在{pos}宫({direction})，提示：")
            lines.append("   • {direction}需注意安全")
            lines.append("   • 避免高风险活动")
            lines.append("   • 注意交通安全")
    lines.append("\n📅 最佳出行时间：")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = _get_time_desc(gong)
        if time_desc:
            lines.append(f"   • 在{time_desc}出行更安全顺利")
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        direction = _get_direction(gong)
        door = pan.get('人盘', {}).get(gong, '')
        if door in travel_suggestions:
            lines.append(travel_suggestions[door].format(direction=direction))
    # 安全提示
    lines.append("\n🔒 安全注意事项：")
    for pos in jiugong:
        if pan.get('神盘', {}).get(pos) == '白虎':
            direction = _get_direction(pos)
            lines.append(f"   • 白虎在{pos}宫({direction})，该方位可能有风险")
            lines.append("   • 避免夜间单独出行")
            lines.append("   • 保管好贵重物品")
        if pan.get('神盘', {}).get(pos) == '太阴':
            direction = _get_direction(pos)
            lines.append(f"   • 太阴在{pos}宫({direction})，适合隐秘出行")
            lines.append("   • 低调行事，避免张扬")
    return "\n".join(lines)


# ==================== 主预测函数 ====================
def predict_timing(pan, yongshen_info, question_type):
    """预测应期祸福（主要对外接口）"""
    timing_analysis = "【详细分析】\n\n"

    # 获取基本信息
    ju_shu = pan.get('基本信息', {}).get('局数', '')
    yinyang = pan.get('基本信息', {}).get('阴阳遁', '')

    # 一、时间判断
    timing_analysis += "一、时间判断（什么时候会有什么变化？）\n" + "-"*40 + "\n"
    if yongshen_info and '宫位' in yongshen_info:
        yongshen_gong = yongshen_info['宫位']
        time_desc = _get_time_desc(yongshen_gong)
        timing_analysis += f"1. 关键时间点：{time_desc}\n"
        if 1 <= ju_shu <= 3:
            timing_analysis += "2. 时间快慢：较快，可能在几天到一周内有结果\n"
        elif 4 <= ju_shu <= 6:
            timing_analysis += "2. 时间快慢：中等，大概需要一到两周\n"
        else:
            timing_analysis += "2. 时间快慢：较慢，可能需要一个月左右\n"
    else:
        timing_analysis += "1. 请先确定用神位置，才能准确判断时间\n"

    # 二、现状分析
    timing_analysis += "\n二、当前情况分析\n" + "-"*40 + "\n"
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        door = pan.get('人盘', {}).get(gong, '')
        star = pan.get('天盘', {}).get(gong, '')
        god = pan.get('神盘', {}).get(gong, '')

        timing_analysis += f"1. 你的状态：用神在{gong}宫({_get_direction(gong)})\n"
        timing_analysis += f"2. 当前机会：{door_desc.get(door, '需要结合具体分析')}\n"
        timing_analysis += f"3. 个人状态：{star_desc.get(star, '状态平稳')}\n"
        timing_analysis += f"4. 外部环境：{god_desc.get(god, '环境一般')}\n"
    else:
        timing_analysis += "无法分析现状，请先确定用神位置\n"

    # 三、行动建议
    timing_analysis += "\n三、行动建议\n" + "-"*40 + "\n"
    advice_list = []
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        door = pan.get('人盘', {}).get(gong, '')
        star = pan.get('天盘', {}).get(gong, '')
        god = pan.get('神盘', {}).get(gong, '')
        # 调用统一的建议生成
        advice_list = _get_advice_by_type(question_type, pan, door, star, god, gong)
        # 添加通用建议
        solar_term = pan.get('基本信息', {}).get('节气', '')
        add_general_suggestions(advice_list, yinyang, solar_term)
        advice_list = advice_list[:5]  # 限制条数
    else:
        advice_list.append("请先确定用神位置，才能给出针对性建议")

    for i, advice in enumerate(advice_list, 1):
        timing_analysis += f"{i}. {advice}\n"

    # 四、特殊提示
    timing_analysis += "\n四、特殊提示\n" + "-"*40 + "\n"
    special_tips = get_special_tips(pan, yongshen_info)
    for tip in special_tips:
        timing_analysis += f"{tip}\n"

    # 五、总结
    timing_analysis += "\n五、总结\n" + "-"*40 + "\n"
    summary = get_summary(pan, yongshen_info, question_type)
    for i, item in enumerate(summary, 1):
        timing_analysis += f"{i}. {item}\n"

    # 六、详细预测（根据问题类型调用对应函数）
    timing_analysis += "\n" + "="*50 + "\n"
    timing_analysis += "【预测分析】\n\n"
    detailed_funcs = {
        "婚姻感情": get_detailed_love_prediction,
        "工作事业": get_detailed_career_prediction,
        "财运求财": get_detailed_wealth_prediction,
        "考试学习": get_detailed_study_prediction,
        "疾病健康": get_detailed_health_prediction,
        "官司诉讼": get_detailed_lawsuit_prediction,
        "出行安全": get_detailed_travel_prediction,
    }
    func = detailed_funcs.get(question_type)
    if func:
        timing_analysis += func(pan, yongshen_info)

    # 最后提醒
    timing_analysis += "\n" + "="*50 + "\n"
    timing_analysis += "【重要提醒】\n"
    timing_analysis += "• 以上分析基于今日排盘，明日盘局变化，建议也会不同\n"
    timing_analysis += "• 真正的决策还需结合实际情况和个人判断\n"
    timing_analysis += "• 命运掌握在自己手中，积极行动才是最好的策略\n"
    timing_analysis += "="*50

    return timing_analysis


# ==================== 特殊提示和总结（保持不变，但可优化） ====================
def get_special_tips(pan, yongshen_info):
    """获取特殊提示（原样保留，也可按需扩展）"""
    tips = []
    # 这里可以加入之前未覆盖的特殊判断，比如空亡、门迫等
    # 目前保持原逻辑，你可以后续扩展
    # 示例：检查空亡
    if '空亡' in pan:
        tips.append("⚠️ 当前有空亡，注意信息不实或机会落空")
    # 检查门迫
    for pos in jiugong:
        door = pan.get('人盘', {}).get(pos, '')
        if door in ['惊门', '伤门'] and pan.get('天盘', {}).get(pos, '') in ['天蓬', '天芮']:
            tips.append(f"⚠️ {pos}宫门迫星凶，需特别注意")
    if not tips:
        tips.append("✅ 当前盘局无明显凶象，但仍需谨慎")
    return tips


def get_summary(pan, yongshen_info, question_type):
    """获取总结（原样保留）"""
    summary = []
    # 这里可以根据盘局给出概括性总结
    yinyang = pan.get('基本信息', {}).get('阴阳遁', '')
    if yinyang == '阳遁':
        summary.append("当前阳遁，运势上升，宜主动进取")
    else:
        summary.append("当前阴遁，运势平稳，宜守不宜攻")
    # 根据用神宫位
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        door = pan.get('人盘', {}).get(gong, '')
        if door in ji_gates:
            summary.append(f"用神宫位得吉门{door}，事情顺利")
        elif door in xiong_gates:
            summary.append(f"用神宫位逢凶门{door}，需多加努力")
        else:
            summary.append("用神宫位门星平和，按计划行事即可")
    else:
        summary.append("请完善用神信息，以获得更准确的总结")
    return summary