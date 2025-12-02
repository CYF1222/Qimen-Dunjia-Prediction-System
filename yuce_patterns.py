from data import jiugong, special_patterns_names

def analyze_patterns(pan):
    """分析格局与祸福"""
    analysis = "格局与祸福分析:\n\n"
    analysis += "十干克应分析:\n"
    for pos in jiugong:
        earth = pan.get('地盘', {}).get(pos, '')
        if earth:
            analysis += f"  {pos}宫: {earth}\n"
    
    analysis += "\n特殊格局与祸福判断:\n"
    special_patterns = []
    fortune_advice = []
    
    for pos in jiugong:
        earth = pan.get('地盘', {}).get(pos, '')
        heaven = pan.get('天盘', {}).get(pos, '')
        human = pan.get('人盘', {}).get(pos, '')
        
        pattern_key = (earth, heaven)
        if pattern_key in special_patterns_names:
            pattern_name = special_patterns_names[pattern_key]
            special_patterns.append(f"{pos}宫: {pattern_name}")
            
            if pattern_name == "青龙返首":
                fortune_advice.append("当前时机有利，可积极行动")
            elif pattern_name == "飞鸟跌穴":
                fortune_advice.append("机遇来临，应把握时机")
            elif pattern_name == "青龙逃走":
                fortune_advice.append("当前不宜大动，应保守行事")
            elif pattern_name == "白虎猖狂":
                fortune_advice.append("需谨慎防范意外，避免冲突")
        
        if earth == '丁' and human == pan.get('值使', ''):
            special_patterns.append(f"{pos}宫: 玉女守门 - 吉，利于隐秘之事")
            fortune_advice.append("适合暗中谋划，不宜张扬")
    
    if special_patterns:
        for pattern in special_patterns:
            analysis += f"  {pattern}\n"
    else:
        analysis += "  暂无特殊格局\n"
    
    analysis += "\n祸福分析与建议:\n"
    if fortune_advice:
        for advice in set(fortune_advice):
            analysis += f"  • {advice}\n"
    else:
        analysis += "  当前局势平稳，宜按部就班\n"
    
    return analysis