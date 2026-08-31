"""
用神分析模块
包含用神定位和宫位分析功能
"""

from data import *
from yuce_utils import *
from yuce_predictions import predict_timing


# ==================== 主函数 ====================
def analyze_yongshen(pan, yongshen_type, specific_yongshen, question_type=""):
    """
    用神祸福分析主函数

    参数:
        pan: 排盘数据字典
        yongshen_type: 用神类型（如 "日干(自己)"）
        specific_yongshen: 特定用神输入（年命或特定符号）
        question_type: 问题类型（用于调用预测）

    返回:
        dict: 包含 'yongshen_report' 和 'yongshen_info'
    """
    # 确定用神
    yongshen_info = determine_yongshen(pan, yongshen_type, specific_yongshen)

    # 构建报告
    report_parts = [
        "用神祸福分析",
        "",
        f"类型: {yongshen_type}",
        f"特定用神: {specific_yongshen or '无'}",
        "",
        f"用神定位: {_format_yongshen_info(yongshen_info)}",
    ]

    # 宫位祸福分析
    if yongshen_info and yongshen_info.get('宫位'):
        gong_analysis = analyze_gong_fortune(pan, yongshen_info['宫位'])
        report_parts.append(f"宫位祸福分析:\n{gong_analysis}")

    # 旺衰祸福
    strength_analysis = analyze_fortune_strength(pan, yongshen_info)
    report_parts.append(f"旺衰祸福:\n{strength_analysis}")

    # 预测分析（如果提供了问题类型）
    if question_type:
        timing_analysis = predict_timing(pan, yongshen_info, question_type)
        report_parts.append(f"\n{timing_analysis}")

    return {
        'yongshen_report': "\n".join(report_parts),
        'yongshen_info': yongshen_info
    }


def _format_yongshen_info(info):
    """格式化用神信息为可读字符串"""
    if not info:
        return "未能确定用神"

    parts = []
    for key in ['类型', '代表', '符号', '宫位', '状态', '说明']:
        if key in info and info[key]:
            parts.append(f"{key}: {info[key]}")

    return " | ".join(parts) if parts else "信息不完整"


# ==================== 用神定位（策略模式） ====================
def determine_yongshen(pan, yongshen_type, specific_yongshen):
    """
    确定用神（根据类型分发到具体处理函数）
    """
    # 用神类型 → 处理函数映射
    handlers = {
        "日干(自己)": _handle_self_yongshen,
        "年命(他人)": _handle_nianming_yongshen,
        "时干(事体)": _handle_shigan_yongshen,
        "值符(领导)": _handle_zhifu_yongshen,
        "年干(上级)": _handle_niangan_yongshen,
        "月干(平辈)": _handle_yuegan_yongshen,
        "特定用神": _handle_specific_yongshen,
    }

    handler = handlers.get(yongshen_type)
    if handler:
        try:
            return handler(pan, specific_yongshen)
        except Exception as e:
            return {
                '类型': yongshen_type,
                '代表': '未知',
                '符号': f'错误: {str(e)}',
                '宫位': None,
                '状态': '确定用神时发生错误',
                '说明': str(e)
            }

    # 未知类型
    return {
        '类型': yongshen_type,
        '代表': '未知',
        '符号': '不支持的类型',
        '宫位': None,
        '状态': '错误',
        '说明': f'不支持的用神类型: {yongshen_type}'
    }


# ---- 各类型用神处理函数 ----
def _handle_self_yongshen(pan, _):
    """日干(自己)"""
    day_gan = pan.get('基本信息', {}).get('四柱', {}).get('日', '  ')[0]
    converted = find_gan_conversion(day_gan)
    position = find_gan_position(pan, day_gan)

    return {
        '类型': '日干',
        '代表': '自己',
        '符号': f"{day_gan}(转换为{converted})",
        '宫位': position,
        '状态': '找到' if position else '未找到',
        '说明': f'日干{day_gan}在地盘中对应{converted}'
    }


def _handle_nianming_yongshen(pan, specific_yongshen):
    """年命(他人)"""
    if not specific_yongshen:
        return {
            '类型': '年命',
            '代表': '他人',
            '符号': '未输入',
            '宫位': None,
            '状态': '需要输入具体年命',
            '说明': '请在"特定用神"框中输入出生年份或干支，如：1984 或 甲子'
        }

    nianming_info = parse_nianming(specific_yongshen)
    if not nianming_info:
        return {
            '类型': '年命',
            '代表': '他人',
            '符号': specific_yongshen,
            '宫位': None,
            '状态': '格式错误',
            '说明': f'无法解析年命输入: {specific_yongshen}，请使用年份数字(如1984)或干支(如甲子)'
        }

    position = find_gan_position(pan, nianming_info['gan'])
    return {
        '类型': '年命',
        '代表': '他人',
        '符号': f"{nianming_info['ganzhi']}(年干:{nianming_info['gan']})",
        '宫位': position,
        '状态': '找到' if position else '未找到',
        '说明': f'年命{nianming_info["ganzhi"]}对应年干{nianming_info["gan"]}'
    }


def _handle_shigan_yongshen(pan, _):
    """时干(事体)"""
    hour_gan = pan.get('基本信息', {}).get('四柱', {}).get('时', '  ')[0]
    position = find_gan_position(pan, hour_gan)

    return {
        '类型': '时干',
        '代表': '事体',
        '符号': hour_gan,
        '宫位': position,
        '状态': '找到' if position else '未找到',
        '说明': f'时干{hour_gan}在地盘中查找'
    }


def _handle_zhifu_yongshen(pan, _):
    """值符(领导)"""
    zhifu = pan.get('值符', '')
    if not zhifu:
        return {
            '类型': '值符',
            '代表': '领导',
            '符号': '未找到值符',
            '宫位': None,
            '状态': '错误',
            '说明': '盘中未找到值符信息'
        }
    position = find_star_position(pan, zhifu)

    return {
        '类型': '值符',
        '代表': '领导',
        '符号': zhifu,
        '宫位': position,
        '状态': '找到' if position else '未找到',
        '说明': f'值符{zhifu}在天盘中查找'
    }


def _handle_niangan_yongshen(pan, _):
    """年干(上级)"""
    year_gan = pan.get('基本信息', {}).get('四柱', {}).get('年', '  ')[0]
    position = find_gan_position(pan, year_gan)

    return {
        '类型': '年干',
        '代表': '上级',
        '符号': year_gan,
        '宫位': position,
        '状态': '找到' if position else '未找到',
        '说明': f'年干{year_gan}在地盘中查找'
    }


def _handle_yuegan_yongshen(pan, _):
    """月干(平辈)"""
    month_gan = pan.get('基本信息', {}).get('四柱', {}).get('月', '  ')[0]
    position = find_gan_position(pan, month_gan)

    return {
        '类型': '月干',
        '代表': '平辈',
        '符号': month_gan,
        '宫位': position,
        '状态': '找到' if position else '未找到',
        '说明': f'月干{month_gan}在地盘中查找'
    }


def _handle_specific_yongshen(pan, specific_yongshen):
    """特定用神"""
    if not specific_yongshen:
        return {
            '类型': '特定',
            '代表': '未指定',
            '符号': '无',
            '宫位': None,
            '状态': '请输入特定用神',
            '说明': '请在地盘、天盘或人盘中选择一个符号'
        }

    position = find_specific_yongshen(pan, specific_yongshen)
    return {
        '类型': '特定',
        '代表': specific_yongshen,
        '符号': specific_yongshen,
        '宫位': position,
        '状态': '找到' if position else '未找到',
        '说明': f'在盘中查找符号: {specific_yongshen}'
    }


# ==================== 查找函数 ====================
def find_gan_position(pan, gan):
    """
    查找天干在地盘中的位置
    """
    target_gan = jia_conversion.get(gan, gan)
    for pos in jiugong:
        if pan.get('地盘', {}).get(pos) == target_gan:
            return pos
    return None


def find_star_position(pan, star):
    """
    查找星（九星）在天盘中的位置
    """
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == star:
            return pos
    return None


def find_specific_yongshen(pan, specific_yongshen):
    """
    在盘中查找特定符号（按优先级：地盘 > 天盘 > 人盘）
    """
    # 先在地盘查找
    for pos in jiugong:
        if pan.get('地盘', {}).get(pos) == specific_yongshen:
            return pos

    # 在天盘查找
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == specific_yongshen:
            return pos

    # 在人盘查找
    for pos in jiugong:
        if pan.get('人盘', {}).get(pos) == specific_yongshen:
            return pos

    return None


# ==================== 宫位分析 ====================
def analyze_gong_fortune(pan, gong):
    """
    分析宫位祸福
    """
    if not gong:
        return "无法定位用神宫位"

    earth = pan.get('地盘', {}).get(gong, '')
    heaven = pan.get('天盘', {}).get(gong, '')
    human = pan.get('人盘', {}).get(gong, '')
    god = pan.get('神盘', {}).get(gong, '')

    lines = [
        f"{gong}宫祸福分析:",
        f"  地盘: {earth}",
        f"  天盘: {heaven}",
        f"  人盘: {human}",
        f"  神盘: {god}",
    ]

    # 门判断
    if human in ji_gates:
        lines.append(f"  八门: 吉门 ({human}) - 主吉利")
    elif human in xiong_gates:
        lines.append(f"  八门: 凶门 ({human}) - 需谨慎")

    # 神判断
    if god in ji_gods:
        lines.append(f"  八神: 吉神 ({god}) - 有助力")
    elif god in xiong_gods:
        lines.append(f"  八神: 凶神 ({god}) - 有阻碍")

    # 空亡检测（如果盘中有空亡信息）
    if pan.get('空亡', ''):
        lines.append("  ⚠️ 空亡: 此宫为空亡，信息可能有缺失或机会落空")

    return "\n".join(lines)


# ==================== 旺衰分析 ====================
def analyze_fortune_strength(pan, yongshen_info):
    """
    分析旺衰祸福
    基于宫位与季节的关系判断旺衰
    """
    if not yongshen_info or not yongshen_info.get('宫位'):
        return "无法进行旺衰祸福分析，请先确定用神位置"

    gong = yongshen_info['宫位']
    season = get_current_season(pan.get('基本信息', {}).get('节气', ''))

    # 宫位与季节的旺衰关系
    # 定义：宫位 → 旺相的季节
    prosperity_map = {
        ('离', '震', '巽'): ('春', '旺', '运势强盛，可积极进取，把握机会'),
        ('离',): ('夏', '旺', '运势强盛，可积极进取，把握机会'),
        ('坤', '艮', '中'): ('季', '旺', '运势稳定，宜稳扎稳打，巩固基础'),
        ('乾', '兑'): ('秋', '旺', '收获时节，宜收割成果，总结经验'),
        ('坎',): ('冬', '旺', '积蓄力量，宜养精蓄锐，等待时机'),
    }

    # 查找匹配
    matched = False
    for gongs, (s, state, advice) in prosperity_map.items():
        if gong in gongs and season == s:
            return f"旺衰祸福分析 ({gong}宫):\n  旺相状态: {state}\n  建议: {advice}"

    # 默认：平
    return f"旺衰祸福分析 ({gong}宫):\n  旺相状态: 平 - 运势一般\n  建议: 宜保守行事，避免冒险"