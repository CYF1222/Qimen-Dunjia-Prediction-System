"""
工具函数模块
包含通用的工具和辅助函数
"""

from data import *
from paipan_functions import *

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

def parse_nianming(input_str):
    """解析年命 - 使用排盘文件的算法"""
    # 导入排盘文件的函数
    from paipan_functions import get_year_ganzhi
    
    input_str = input_str.strip()
    
    if input_str.isdigit():
        year = int(input_str)
        # 调用排盘文件的函数
        gan, zhi = get_year_ganzhi(year)
        return {
            'ganzhi': f"{gan}{zhi}",
            'gan': gan
        }
    
    elif len(input_str) == 2 and all(c in '甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥' for c in input_str):
        return {
            'ganzhi': input_str,
            'gan': input_str[0]
        }
    
    return None

def get_current_season(solar_term):
    """获取当前季节"""
    if solar_term in spring_terms:
        return '春'
    elif solar_term in summer_terms:
        return '夏'
    elif solar_term in autumn_terms:
        return '秋'
    elif solar_term in winter_terms:
        return '冬'
    else:
        return '季'
    
def get_special_tips(pan, yongshen_info):
    """获取特殊提示"""
    special_tips = []
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        earth = pan.get('地盘', {}).get(gong, '')
        heaven = pan.get('天盘', {}).get(gong, '')
        # 特殊格局提示
        if earth == '戊' and heaven == '丙':
            special_tips.append("🔴 青龙返首：大吉格局，事情会出乎意料地顺利解决")
        elif earth == '丙' and heaven == '戊':
            special_tips.append("🔴 飞鸟跌穴：吉上加吉，抓住机会，事半功倍")
        elif earth == '乙' and heaven == '辛':
            special_tips.append("🔴 青龙逃走：事情容易半途而废，需要坚持到底")
        elif earth == '辛' and heaven == '乙':
            special_tips.append("🔴 白虎猖狂：可能有突发状况，需做好应急预案")
        elif earth == '丁' and pan.get('人盘', {}).get(gong, '') == pan.get('值使', ''):
            special_tips.append("🔴 玉女守门：适合暗中操作，保密进行效果更好")
        # 检查其他宫位是否有特殊格局 - 改为具体方位
        for pos in jiugong:
            if pos != gong:
                e = pan.get('地盘', {}).get(pos, '')
                h = pan.get('天盘', {}).get(pos, '')
                direction = convert_gong_to_direction(pos)
                
                if e == '戊' and h == '丙':
                    special_tips.append(f"✅ 青龙返首在{pos}宫({direction})，这个方位可能有意外之喜")
                elif e == '丙' and h == '戊':
                    special_tips.append(f"✅ 飞鸟跌穴在{pos}宫({direction})，这个方向做事更顺利")
                elif e == '癸' and h == '丁':
                    special_tips.append(f"⚠️ 癸+丁（蛇夭矫）在{pos}宫({direction})，这个方向可能有口舌是非")
                elif e == '庚' and h == '丙':
                    special_tips.append(f"⚠️ 庚+丙（贼必来）在{pos}宫({direction})，这个方向可能有竞争或阻碍")
        
        if not special_tips:
            special_tips.append("• 当前没有特别需要注意的特殊格局，按正常情况处理即可")
    
    else:
        special_tips.append("• 无法判断特殊格局，请先确定用神")
    
    return special_tips

def get_summary(pan, yongshen_info, question_type):
    """获取总结"""
    summary = []
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        door = pan.get('人盘', {}).get(gong, '')
        god = pan.get('神盘', {}).get(gong, '')
        # 门判断
        if door in ji_gates:
            summary.append("总体运势：吉利，可以积极行动")
        elif door in xiong_gates:
            summary.append("总体运势：需谨慎行事")
        # 神判断
        if god in ji_gods:
            summary.append("贵人运：有贵人相助或合作机会")
        elif god in xiong_gods:
            summary.append("需注意：可能有阻碍或意外情况")
        # 根据问题类型给出总结
        if question_type == "婚姻感情":
            summary.append("感情建议：真诚沟通，给予空间")
        elif question_type == "工作事业":
            summary.append("事业建议：把握机会，稳扎稳打")
        elif question_type == "财运求财":
            summary.append("财运建议：谨慎投资，稳健为主")
        elif question_type == "考试学习":
            summary.append("学习建议：勤奋复习，注意细节")
        elif question_type == "疾病健康":
            summary.append("健康建议：及时就医，注意调理")
        # 宫位判断 - 改为具体方位
        if gong in ['离', '震', '巽']:
            directions = []
            if gong == '离':
                directions.append('南方')
            if gong == '震':
                directions.append('东方')
            if gong == '巽':
                directions.append('东南方')
            summary.append(f"方位提示：{', '.join(directions)}可能更有利")
        elif gong in ['乾', '兑']:
            directions = []
            if gong == '乾':
                directions.append('西北方')
            if gong == '兑':
                directions.append('西方')
            summary.append(f"方位提示：{', '.join(directions)}可能更有利")
        elif gong in ['坎']:
            summary.append("方位提示：北方可能更有利")
        elif gong in ['坤', '艮', '中']:
            directions = []
            if gong == '坤':
                directions.append('西南方')
            if gong == '艮':
                directions.append('东北方')
            if gong == '中':
                directions.append('中央')
            summary.append(f"方位提示：{', '.join(directions)}可能更有利")
    
    else:
        summary.append("请先完成用神分析，才能进行总结判断")
    
    return summary

def generate_comprehensive_report(pan, analysis):
    """生成综合报告"""
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
        # 标记用神宫位
        yongshen_gong = analysis.get('yongshen_info', {}).get('宫位', '')
        if pos == yongshen_gong:
            report += f"{pos}宫[用神]: 地盘{earth} 天盘{heaven} 人盘{human} 神盘{god}\n"
        else:
            report += f"{pos}宫: 地盘{earth} 天盘{heaven} 人盘{human} 神盘{god}\n"
    # 添加用神分析
    if analysis and 'yongshen_report' in analysis:
        report += f"\n用神分析:\n------------\n{analysis.get('yongshen_report', '暂无详细分析')}"
    else:
        report += "\n用神分析:\n------------\n请先进行用神分析"
    # 添加格局分析
    from yuce_patterns import analyze_patterns
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
    
def analyze_love_prediction(pan, yongshen_info):
    """分析感情预测"""
    analysis = "💖 感情预测分析：\n\n"
    # 查找六合位置
    for pos in jiugong:
        if pan.get('神盘', {}).get(pos) == '六合':
            analysis += f"✅ 六合星在{pos}宫，表明：\n"
            analysis += "   • 有良好的婚姻缘分机会\n"
            analysis += "   • 当前适合发展长期关系\n"
            analysis += f"   • 在{pos}方位或时间更有利\n"
            break
    # 查找天芮星（可能有问题）
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == '天芮':
            analysis += f"⚠️ 天芮星在{pos}宫，提示：\n"
            analysis += "   • 感情中可能存在隐性问题\n"
            analysis += "   • 需要更多的沟通和理解\n"
            analysis += "   • 注意避免误会和猜忌\n"
            break
    # 根据门判断
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        door = pan.get('人盘', {}).get(gong, '')
        
        if door == '休门':
            analysis += "\n💤 当前休门当值：\n"
            analysis += "   • 适合两人世界，安静相处\n"
            analysis += "   • 不宜过于急躁推进关系\n"
            analysis += "   • 给彼此一些空间和时间\n"
        elif door == '开门':
            analysis += "\n🚪 当前开门当值：\n"
            analysis += "   • 适合表白或公开关系\n"
            analysis += "   • 感情发展有新的机会\n"
            analysis += "   • 主动出击效果更好\n"
        elif door == '惊门':
            analysis += "\n⚠️ 当前惊门当值：\n"
            analysis += "   • 注意沟通方式，避免争吵\n"
            analysis += "   • 感情中可能有意外情况\n"
            analysis += "   • 保持冷静，理性处理\n"
    # 什么时候表白合适
    analysis += "\n📅 表白时机建议：\n"
    # 根据地支判断
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = gong_to_time.get(gong, '')
        if time_desc:
            analysis += f"   • 在{time_desc}时表白效果更佳\n"
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
    
    return analysis

def analyze_career_prediction(pan, yongshen_info):
    """分析事业预测"""
    analysis = "💼 事业预测分析：\n\n"
    # 查找开门位置
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == '开门':
            analysis += f"✅ 开门在{pos}宫，表明：\n"
            analysis += "   • 事业发展有新的机会\n"
            analysis += f"   • 在{pos}方位发展更有利\n"
            analysis += "   • 适合开展新项目\n"
            break
    # 查找值符星位置
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == pan.get('值符', ''):
            analysis += f"⭐ 值符星在{pos}宫，提示：\n"
            analysis += "   • 有贵人相助，多与领导沟通\n"
            analysis += "   • 事业上可能有重要机会\n"
            analysis += f"   • 关注{pos}方位的人脉关系\n"
            break
    # 工作变动时机
    analysis += "\n📅 工作变动时机：\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong = yongshen_info['宫位']
        time_desc = gong_to_time.get(gong, '')
        if time_desc:
            analysis += f"   • 在{time_desc}时考虑变动更有利\n"
    
    return analysis
