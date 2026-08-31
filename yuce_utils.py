"""
工具函数模块
包含通用的工具和辅助函数
"""

from data import *
from paipan_functions import get_year_ganzhi


# ==================== 方位转换 ====================
def convert_gong_to_direction(gong):
    """将宫位转换为方位描述"""
    return gong_to_direction.get(gong, gong)


def convert_zhi_to_direction(zhi):
    """将地支转换为方位描述"""
    return zhi_to_direction_detail.get(zhi, zhi)


def get_direction_by_gong(gong):
    """根据宫位获取方位描述（更详细的版本）"""
    return direction_map.get(gong, f'{gong}宫')


def find_gan_conversion(gan):
    """查找天干转换"""
    return jia_conversion.get(gan, gan)


# ==================== 年命解析 ====================
def parse_nianming(input_str):
    """
    解析年命
    支持两种格式：
    1. 年份数字（如 1984）→ 自动转换为该年的干支
    2. 干支字符串（如 甲子）→ 直接返回
    """
    input_str = input_str.strip()
    
    if input_str.isdigit():
        year = int(input_str)
        gan, zhi = get_year_ganzhi(year)
        return {
            'ganzhi': f"{gan}{zhi}",
            'gan': gan
        }
    
    # 检查是否为有效的干支组合（2个字符，天干+地支）
    if len(input_str) == 2:
        gan, zhi = input_str[0], input_str[1]
        if gan in '甲乙丙丁戊己庚辛壬癸' and zhi in '子丑寅卯辰巳午未申酉戌亥':
            return {
                'ganzhi': input_str,
                'gan': gan
            }
    
    return None


# ==================== 季节 ====================
def get_current_season(solar_term):
    """根据节气获取当前季节"""
    if solar_term in spring_terms:
        return '春'
    elif solar_term in summer_terms:
        return '夏'
    elif solar_term in autumn_terms:
        return '秋'
    elif solar_term in winter_terms:
        return '冬'
    return '季'  # 默认


# ==================== 特殊格局检测（核心工具） ====================
def detect_special_patterns(pan, target_gong=None):
    """
    检测盘中的特殊格局
    返回字典：{宫位: (格局名称, 吉凶, 描述)}
    """
    patterns = {}
    pattern_map = {
        ('戊', '丙'): ('青龙返首', '吉', '事情会出乎意料地顺利解决'),
        ('丙', '戊'): ('飞鸟跌穴', '吉', '抓住机会，事半功倍'),
        ('乙', '辛'): ('青龙逃走', '凶', '事情容易半途而废，需要坚持到底'),
        ('辛', '乙'): ('白虎猖狂', '凶', '可能有突发状况，需做好应急预案'),
        ('癸', '丁'): ('蛇夭矫', '凶', '可能有口舌是非'),
        ('庚', '丙'): ('贼必来', '凶', '可能有竞争或阻碍'),
    }
    
    for pos in jiugong:
        earth = pan.get('地盘', {}).get(pos, '')
        heaven = pan.get('天盘', {}).get(pos, '')
        key = (earth, heaven)
        
        if key in pattern_map:
            name, level, desc = pattern_map[key]
            # 只返回目标宫位或全部
            if target_gong is None or pos == target_gong:
                patterns[pos] = (name, level, desc)
    
    # 特殊：玉女守门（丁 + 值使）
    zhishi = pan.get('值使', '')
    for pos in jiugong:
        earth = pan.get('地盘', {}).get(pos, '')
        door = pan.get('人盘', {}).get(pos, '')
        if earth == '丁' and door == zhishi:
            if target_gong is None or pos == target_gong:
                patterns[pos] = ('玉女守门', '吉', '适合暗中操作，保密进行效果更好')
    
    return patterns


def get_special_tips(pan, yongshen_info):
    """
    获取特殊提示（供预测模块调用）
    注意：此函数与 yuce_predictions.py 中的同名函数共存，
    建议统一使用此版本，删除 yuce_predictions 中的副本。
    """
    tips = []
    
    if not yongshen_info or '宫位' not in yongshen_info:
        tips.append("• 无法判断特殊格局，请先确定用神")
        return tips
    
    gong = yongshen_info['宫位']
    
    # 检测所有格局
    all_patterns = detect_special_patterns(pan)
    
    # 用神宫位的格局
    if gong in all_patterns:
        name, level, desc = all_patterns[gong]
        icon = "✅" if level == '吉' else "⚠️" if level == '凶' else "🔴"
        tips.append(f"{icon} {name}：{desc}")
    
    # 其他宫位的格局（供参考）
    for pos, (name, level, desc) in all_patterns.items():
        if pos != gong:
            direction = convert_gong_to_direction(pos)
            icon = "✅" if level == '吉' else "⚠️" if level == '凶' else "🔴"
            tips.append(f"{icon} {name}在{pos}宫({direction})，{desc}")
    
    # 空亡检测（如果 pan 中有空亡信息）
    if pan.get('空亡'):
        tips.append("⚠️ 当前有空亡，注意信息不实或机会落空")
    
    if not tips:
        tips.append("• 当前没有特别需要注意的特殊格局，按正常情况处理即可")
    
    return tips


def get_summary(pan, yongshen_info, question_type):
    """
    获取总结（供预测模块调用）
    注意：此函数与 yuce_predictions.py 中的同名函数共存，
    建议统一使用此版本，删除 yuce_predictions 中的副本。
    """
    summary = []
    
    if not yongshen_info or '宫位' not in yongshen_info:
        summary.append("请先完成用神分析，才能进行总结判断")
        return summary
    
    gong = yongshen_info['宫位']
    door = pan.get('人盘', {}).get(gong, '')
    god = pan.get('神盘', {}).get(gong, '')
    
    # 门判断
    if door in ji_gates:
        summary.append("总体运势：吉利，可以积极行动")
    elif door in xiong_gates:
        summary.append("总体运势：需谨慎行事")
    else:
        summary.append("总体运势：平稳，按计划行事即可")
    
    # 神判断
    if god in ji_gods:
        summary.append("贵人运：有贵人相助或合作机会")
    elif god in xiong_gods:
        summary.append("需注意：可能有阻碍或意外情况")
    
    # 根据问题类型给出总结
    advice_map = {
        "婚姻感情": "感情建议：真诚沟通，给予空间",
        "工作事业": "事业建议：把握机会，稳扎稳打",
        "财运求财": "财运建议：谨慎投资，稳健为主",
        "考试学习": "学习建议：勤奋复习，注意细节",
        "疾病健康": "健康建议：及时就医，注意调理",
        "官司诉讼": "诉讼建议：收集证据，寻求专业帮助",
        "出行安全": "出行建议：规划路线，注意安全",
    }
    if question_type in advice_map:
        summary.append(advice_map[question_type])
    
    # 方位提示（更简洁的写法）
    direction_hint = _get_direction_hint(gong)
    if direction_hint:
        summary.append(f"方位提示：{direction_hint}")
    
    return summary


def _get_direction_hint(gong):
    """获取宫位对应的方位提示（辅助函数）"""
    # 使用预定义的宫位-方位映射
    direction_map_simple = {
        '离': '南方',
        '震': '东方',
        '巽': '东南方',
        '乾': '西北方',
        '兑': '西方',
        '坎': '北方',
        '坤': '西南方',
        '艮': '东北方',
        '中': '中央',
    }
    return direction_map_simple.get(gong, '')


# ==================== 综合报告（已修复循环导入） ====================
def generate_comprehensive_report(pan, analysis):
    """
    生成综合报告
    """
    # 延迟导入，避免循环依赖
    from yuce_patterns import analyze_patterns
    
    basic_info = pan.get('基本信息', {})
    
    report = f"""
奇门遁甲综合分析报告
========================

排盘信息:
--------
时间: {basic_info.get('时间', '未知')}
节气: {basic_info.get('节气', '未知')}
局数: {basic_info.get('局数', '未知')}局
阴阳遁: {basic_info.get('阴阳遁', '未知')}
值符: {pan.get('值符', '未知')}
值使: {pan.get('值使', '未知')}

四柱信息:
--------
年柱: {basic_info.get('四柱', {}).get('年', '未知')}
月柱: {basic_info.get('四柱', {}).get('月', '未知')}
日柱: {basic_info.get('四柱', {}).get('日', '未知')}
时柱: {basic_info.get('四柱', {}).get('时', '未知')}

盘局详情:
--------
"""
    for pos in jiugong:
        earth = pan.get('地盘', {}).get(pos, '')
        heaven = pan.get('天盘', {}).get(pos, '')
        human = pan.get('人盘', {}).get(pos, '')
        god = pan.get('神盘', {}).get(pos, '')
        
        yongshen_gong = analysis.get('yongshen_info', {}).get('宫位', '')
        marker = "[用神]" if pos == yongshen_gong else ""
        report += f"{pos}宫{marker}: 地盘{earth} 天盘{heaven} 人盘{human} 神盘{god}\n"
    
    # 用神分析
    if analysis and 'yongshen_report' in analysis:
        report += f"\n用神分析:\n------------\n{analysis.get('yongshen_report', '暂无详细分析')}"
    else:
        report += "\n用神分析:\n------------\n请先进行用神分析"
    
    # 格局分析
    patterns_analysis = analyze_patterns(pan)
    report += f"\n\n格局分析:\n------------\n{patterns_analysis}"
    
    report += """
综合建议:
------------
根据排盘结果，结合具体问题进行深入分析。
注意考虑用神所在宫位的旺衰、生克关系以及特殊格局的影响。

重要提示:
--------
本分析结果仅供参考，实际决策请结合现实情况。
奇门遁甲是传统文化遗产，请理性看待预测结果。
祸福相依，事在人为，积极面对生活中的各种挑战。
"""
    return report