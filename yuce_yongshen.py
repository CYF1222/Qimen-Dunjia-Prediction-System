"""
用神分析模块
包含用神定位和宫位分析功能
"""

from data import *
from yuce_utils import *
from yuce_predictions import predict_timing

def analyze_yongshen(pan, yongshen_type, specific_yongshen, question_type=""):
    """用神祸福分析主函数"""
    analysis_report = f"用神祸福分析\n\n类型: {yongshen_type}\n特定用神: {specific_yongshen}\n\n"
    
    yongshen_info = determine_yongshen(pan, yongshen_type, specific_yongshen)
    analysis_report += f"用神定位: {yongshen_info}\n\n"
    
    if yongshen_info and '宫位' in yongshen_info:
        gong_analysis = analyze_gong_fortune(pan, yongshen_info['宫位'])
        analysis_report += f"宫位祸福分析:\n{gong_analysis}\n"
    
    strength_analysis = analyze_fortune_strength(pan, yongshen_info)
    analysis_report += f"旺衰祸福:\n{strength_analysis}\n"
    
    if question_type:
        timing_analysis = predict_timing(pan, yongshen_info, question_type)
        analysis_report += f"\n{timing_analysis}\n"
    
    return {
        'yongshen_report': analysis_report,
        'yongshen_info': yongshen_info
    }

def determine_yongshen(pan, yongshen_type, specific_yongshen):
    """确定用神"""
    try:
        if yongshen_type == "年命(他人)":
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
                    '说明': f'无法解析年命输入: {specific_yongshen}'
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
        
        if yongshen_type == "日干(自己)":
            day_gan = pan.get('基本信息', {}).get('四柱', {}).get('日', '  ')[0]
            position = find_gan_position(pan, day_gan)
            return {
                '类型': '日干', 
                '代表': '自己', 
                '符号': f"{day_gan}(转换为{find_gan_conversion(day_gan)})",
                '宫位': position,
                '状态': '找到' if position else '未找到',
                '说明': f'日干{day_gan}在地盘中对应{find_gan_conversion(day_gan)}'
            }
            
        elif yongshen_type == "时干(事体)":
            hour_gan = pan.get('基本信息', {}).get('四柱', {}).get('时', '  ')[0]
            position = find_gan_position(pan, hour_gan)
            return {
                '类型': '时干', 
                '代表': '事体', 
                '符号': hour_gan,
                '宫位': position,
                '状态': '找到' if position else '未找到',
                '说明': f'时干{hour_gan}直接在地盘中查找'
            }
            
        elif yongshen_type == "值符(领导)":
            zhifu = pan.get('值符', '')
            position = find_star_position(pan, zhifu)
            return {
                '类型': '值符', 
                '代表': '领导', 
                '符号': zhifu,
                '宫位': position,
                '状态': '找到' if position else '未找到'
            }
            
        elif yongshen_type == "年干(上级)":
            year_gan = pan.get('基本信息', {}).get('四柱', {}).get('年', '  ')[0]
            position = find_gan_position(pan, year_gan)
            return {
                '类型': '年干', 
                '代表': '上级', 
                '符号': year_gan,
                '宫位': position,
                '状态': '找到' if position else '未找到'
            }
            
        elif yongshen_type == "月干(平辈)":
            month_gan = pan.get('基本信息', {}).get('四柱', {}).get('月', '  ')[0]
            position = find_gan_position(pan, month_gan)
            return {
                '类型': '月干', 
                '代表': '平辈', 
                '符号': month_gan,
                '宫位': position,
                '状态': '找到' if position else '未找到'
            }
            
        elif yongshen_type == "特定用神":
            if not specific_yongshen:
                return {
                    '类型': '特定', 
                    '代表': '未指定',
                    '符号': '无',
                    '宫位': None,
                    '状态': '请输入特定用神'
                }
            position = find_specific_yongshen(pan, specific_yongshen)
            return {
                '类型': '特定', 
                '代表': specific_yongshen,
                '符号': specific_yongshen,
                '宫位': position,
                '状态': '找到' if position else '未找到'
            }
            
    except Exception as e:
        return {
            '类型': '错误',
            '代表': '未知',
            '符号': f'错误: {str(e)}',
            '宫位': None,
            '状态': '确定用神时发生错误'
        }
    
    return None

def find_gan_position(pan, gan):
    """查找天干位置"""
    target_gan = jia_conversion.get(gan, gan)
    
    for pos in jiugong:
        if pan.get('地盘', {}).get(pos) == target_gan:
            return pos
    
    return None

def find_star_position(pan, star):
    """查找星的位置"""
    for pos in jiugong:
        if pan.get('天盘', {}).get(pos) == star:
            return pos
    return None

def find_specific_yongshen(pan, specific_yongshen):
    """查找特定用神位置"""
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

def analyze_gong_fortune(pan, gong):
    """分析宫位祸福"""
    if not gong:
        return "无法定位用神宫位"
    
    analysis = f"{gong}宫祸福分析:\n"
    
    earth = pan.get('地盘', {}).get(gong, '')
    heaven = pan.get('天盘', {}).get(gong, '')
    human = pan.get('人盘', {}).get(gong, '')
    god = pan.get('神盘', {}).get(gong, '')
    
    analysis += f"  地盘: {earth}\n"
    analysis += f"  天盘: {heaven}\n"
    analysis += f"  人盘: {human}\n"
    analysis += f"  神盘: {god}\n"
    
    if human in ji_gates:
        analysis += f"  八门: 吉门 ({human}) - 主吉利\n"
    elif human in xiong_gates:
        analysis += f"  八门: 凶门 ({human}) - 需谨慎\n"
    
    if god in ji_gods:
        analysis += f"  八神: 吉神 ({god}) - 有助力\n"
    elif god in xiong_gods:
        analysis += f"  八神: 凶神 ({god}) - 有阻碍\n"
    
    return analysis

def analyze_fortune_strength(pan, yongshen_info):
    """分析旺衰祸福"""
    if not yongshen_info or '宫位' not in yongshen_info:
        return "无法进行旺衰祸福分析"
    
    gong = yongshen_info['宫位']
    season = get_current_season(pan.get('基本信息', {}).get('节气', ''))
    
    analysis = f"旺衰祸福分析 ({gong}宫):\n"
    
    if gong in ['离', '震', '巽'] and season == '春':
        analysis += "  旺相状态: 旺 - 运势强盛\n"
        analysis += "  建议: 可积极进取，把握机会\n"
    elif gong in ['离'] and season == '夏':
        analysis += "  旺相状态: 旺 - 运势强盛\n"
        analysis += "  建议: 可积极进取，把握机会\n"
    elif gong in ['坤', '艮', '中'] and season == '季':
        analysis += "  旺相状态: 旺 - 运势稳定\n"
        analysis += "  建议: 宜稳扎稳打，巩固基础\n"
    elif gong in ['乾', '兑'] and season == '秋':
        analysis += "  旺相状态: 旺 - 收获时节\n"
        analysis += "  建议: 宜收割成果，总结经验\n"
    elif gong in ['坎'] and season == '冬':
        analysis += "  旺相状态: 旺 - 积蓄力量\n"
        analysis += "  建议: 宜养精蓄锐，等待时机\n"
    else:
        analysis += "  旺相状态: 平 - 运势一般\n"
        analysis += "  建议: 宜保守行事，避免冒险\n"
    
    return analysis