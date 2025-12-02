# main.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime
from data import *
from yuce_yongshen import analyze_yongshen
from yuce_utils import *
from yuce_predictions import predict_timing
from yuce_patterns import analyze_patterns
from paipan_functions import *

# 全局变量
current_pan = None
current_analysis = None
root = None

def create_main_window():
    """创建主窗口"""
    global root
    root = tk.Tk()
    root.title("奇门遁甲排盘系统")
    root.geometry("1200x800")
    
    # 创建主框架
    main_frame = ttk.Frame(root)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # 创建标题
    title_label = ttk.Label(main_frame, text="奇门遁甲排盘分析系统", 
                           font=("微软雅黑", 16, "bold"))
    title_label.pack(pady=(0, 20))
    
    # 创建标签页
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill='both', expand=True)
    
    # 创建各个标签页
    input_frame = create_input_tab(notebook)
    pan_frame = create_pan_display_tab(notebook)
    detailed_frame = create_detailed_analysis_tab(notebook)
    
    # 存储框架引用
    root.frames = {
        'input': input_frame,
        'pan': pan_frame,
        'detailed': detailed_frame
    }
    
    # 状态栏
    status_frame = ttk.Frame(main_frame)
    status_frame.pack(fill='x', pady=(10, 0))
    
    status_var = tk.StringVar(value="就绪")
    status_label = ttk.Label(status_frame, textvariable=status_var, 
                            font=("微软雅黑", 9), relief="sunken")
    status_label.pack(fill='x')
    
    root.status_var = status_var
    
    return root

def create_input_tab(notebook):
    """创建输入参数标签页（居中简化版）"""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="输入参数")
    
    # 创建Canvas和滚动条，使页面可滚动
    canvas = tk.Canvas(frame)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    
    # 创建一个内部框架用于存放内容
    container = ttk.Frame(canvas)
    
    # 创建一个窗口在canvas中
    canvas.create_window((0, 0), window=container, anchor="nw", width=canvas.winfo_reqwidth())
    
    def on_configure(event):
        # 更新滚动区域
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    container.bind("<Configure>", on_configure)
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # ========== 主内容容器 ==========
    # 创建一个用于居中的外层框架
    outer_frame = ttk.Frame(container)
    outer_frame.pack(expand=True, fill="both")
    
    # 创建一个中心内容框架
    center_frame = ttk.Frame(outer_frame)
    center_frame.pack(expand=True)
    
    content_frame = ttk.Frame(center_frame)
    content_frame.pack(pady=20)
    
    # ========== 第一部分：时间输入 ==========
    time_frame = ttk.LabelFrame(content_frame, text="📅 时间输入", padding=15)
    time_frame.pack(fill='x', pady=(0, 15))
    
    # 创建时间输入的网格布局
    time_grid = ttk.Frame(time_frame)
    time_grid.pack(fill='x', padx=10, pady=5)
    
    # 年
    ttk.Label(time_grid, text="年:", width=5).grid(row=0, column=0, padx=(0, 5), pady=5, sticky="e")
    year_var = tk.StringVar(value=str(datetime.datetime.now().year))
    year_entry = ttk.Entry(time_grid, textvariable=year_var, width=15)
    year_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    # 月
    ttk.Label(time_grid, text="月:", width=5).grid(row=0, column=2, padx=(20, 5), pady=5, sticky="e")
    month_var = tk.StringVar(value=str(datetime.datetime.now().month))
    month_entry = ttk.Entry(time_grid, textvariable=month_var, width=15)
    month_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
    
    # 日
    ttk.Label(time_grid, text="日:", width=5).grid(row=1, column=0, padx=(0, 5), pady=5, sticky="e")
    day_var = tk.StringVar(value=str(datetime.datetime.now().day))
    day_entry = ttk.Entry(time_grid, textvariable=day_var, width=15)
    day_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    # 时
    ttk.Label(time_grid, text="时:", width=5).grid(row=1, column=2, padx=(20, 5), pady=5, sticky="e")
    hour_var = tk.StringVar(value=str(datetime.datetime.now().hour))
    hour_entry = ttk.Entry(time_grid, textvariable=hour_var, width=15)
    hour_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    
    # ========== 第二部分：问题类型 ==========
    question_frame = ttk.LabelFrame(content_frame, text="❓ 问题类型", padding=15)
    question_frame.pack(fill='x', pady=(0, 15))
    
    question_type_var = tk.StringVar(value="")
    question_types = [
        "工作事业", "财运求财", "婚姻感情", "疾病健康", 
        "考试学习", "官司诉讼", "出行安全"
    ]
    
    # 创建两列的问题类型选项
    question_grid = ttk.Frame(question_frame)
    question_grid.pack(fill='x', padx=10, pady=5)
    
    for i, q_type in enumerate(question_types):
        row = i // 2
        col = i % 2
        if col == 0:
            rb_frame = ttk.Frame(question_grid)
            rb_frame.grid(row=row, column=0, sticky='w', padx=(0, 30), pady=2)
        else:
            rb_frame = ttk.Frame(question_grid)
            rb_frame.grid(row=row, column=1, sticky='w', pady=2)
        
        ttk.Radiobutton(rb_frame, text=q_type, variable=question_type_var, 
                       value=q_type, width=10).pack(side=tk.LEFT)
    
    # ========== 第三部分：用神选择 ==========
    yongshen_frame = ttk.LabelFrame(content_frame, text="🧭 用神选择", padding=15)
    yongshen_frame.pack(fill='x', pady=(0, 20))
    
    # 用神类型选择
    type_row = ttk.Frame(yongshen_frame)
    type_row.pack(fill='x', pady=5, padx=10)
    ttk.Label(type_row, text="用神类型:", font=("微软雅黑", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
    
    yongshen_var = tk.StringVar(value="日干(自己)")
    yongshen_combo = ttk.Combobox(type_row, textvariable=yongshen_var, 
                                 values=["日干(自己)", "年命(他人)", "时干(事体)", "值符(领导)", 
                                         "年干(上级)", "月干(平辈)", "特定用神"], 
                                 width=18, state="readonly")
    yongshen_combo.pack(side=tk.LEFT, padx=(0, 15))
    
    # 特定输入框架
    specific_frame = ttk.Frame(yongshen_frame)
    
    specific_var = tk.StringVar()
    specific_label = ttk.Label(specific_frame, text="出生年份/干支:")
    specific_entry = ttk.Entry(specific_frame, textvariable=specific_var, width=15)
    
    # 用神提示标签
    hint_label = ttk.Label(yongshen_frame, text="选择日干(自己)进行分析", 
                          font=("微软雅黑", 9), foreground="gray")
    hint_label.pack(fill='x', pady=(5, 0), padx=10)
    
    # 用神选择变化时的处理
    def on_yongshen_change(event):
        selected = yongshen_var.get()
        if selected == "年命(他人)":
            specific_label.config(text="出生年份/干支:")
            specific_frame.pack(fill='x', pady=(10, 5), padx=10)
            hint_label.config(text="请输入出生年份(如1984)或干支(如甲子)")
        elif selected == "特定用神":
            specific_label.config(text="特定符号:")
            specific_frame.pack(fill='x', pady=(10, 5), padx=10)
            hint_label.config(text="请输入天干、九星、八门等符号")
        else:
            specific_frame.pack_forget()
            hint_label.config(text=f"自动获取{selected}进行分析")
    
    yongshen_combo.bind("<<ComboboxSelected>>", on_yongshen_change)
    
    # 特定输入布局
    specific_label.pack(side=tk.LEFT, padx=(0, 5))
    specific_entry.pack(side=tk.LEFT)
    
    # ========== 第四部分：排盘按钮 ==========
    button_frame = ttk.Frame(content_frame)
    button_frame.pack(fill='x', pady=(10, 0))
    
    def paipan_callback():
        global current_pan, current_analysis
        try:
            year = int(year_var.get())
            month = int(month_var.get())
            day = int(day_var.get())
            hour = int(hour_var.get())
            question_type = question_type_var.get()
            
            if not question_type:
                messagebox.showerror("错误", "请选择问题类型")
                return
            
            root.status_var.set("正在排盘...")
            root.update()
            
            # 调用排盘函数
            current_pan = create_qimen_pan(year, month, day, hour)
            
            # 获取用神参数
            yongshen_type = yongshen_var.get()
            specific_yongshen = specific_var.get()
            
            # 检查用神输入
            if yongshen_type == "年命(他人)" and not specific_yongshen:
                messagebox.showerror("错误", "年命类型需要输入出生年份或干支")
                root.status_var.set("就绪")
                return
            elif yongshen_type == "特定用神" and not specific_yongshen:
                messagebox.showerror("错误", "特定用神需要输入内容")
                root.status_var.set("就绪")
                return
            
            # 进行用神分析
            current_analysis = analyze_yongshen(current_pan, yongshen_type, specific_yongshen, question_type)
            
            # 更新状态
            root.status_var.set("排盘完成")
            
            # 更新其他标签页
            update_pan_display(current_pan)
            
            # 清空详细分析
            root.frames['detailed'].analysis_text.delete(1.0, tk.END)
            
            messagebox.showinfo("成功", "排盘完成！")
            
        except ValueError as e:
            root.status_var.set("输入参数错误")
            messagebox.showerror("错误", f"请输入正确的数字: {e}")
        except Exception as e:
            root.status_var.set("排盘过程出错")
            messagebox.showerror("错误", f"排盘过程中出现错误: {e}")
    
    paipan_btn = ttk.Button(button_frame, text="🚀 开始排盘", 
                           command=paipan_callback,
                           style="Big.TButton")
    paipan_btn.pack(pady=20, ipadx=30, ipady=12)
    
    # 创建自定义样式
    style = ttk.Style()
    style.configure("Big.TButton", font=("微软雅黑", 12, "bold"), padding=10)
    
    # 存储变量
    frame.year_var = year_var
    frame.month_var = month_var
    frame.day_var = day_var
    frame.hour_var = hour_var
    frame.question_type_var = question_type_var
    frame.yongshen_var = yongshen_var
    frame.specific_var = specific_var
    
    return frame

def create_pan_display_tab(notebook):
    """创建排盘显示标签页"""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="排盘详情")
    
    # 左侧基本信息框架
    left_frame = ttk.Frame(frame)
    left_frame.pack(side=tk.LEFT, fill='y', padx=(0, 10))
    
    # 基本信息显示
    info_frame = ttk.LabelFrame(left_frame, text="基本信息")
    info_frame.pack(fill='x', pady=(0, 10))
    
    info_text = scrolledtext.ScrolledText(info_frame, height=10, width=30, font=("微软雅黑", 10))
    info_text.pack(fill='both', padx=5, pady=5)
    frame.info_text = info_text
    
    # 右侧排盘详情框架
    right_frame = ttk.Frame(frame)
    right_frame.pack(side=tk.RIGHT, fill='both', expand=True)
    
    # 排盘详情标签页
    detail_notebook = ttk.Notebook(right_frame)
    detail_notebook.pack(fill='both', expand=True)
    
    # 地盘显示
    di_frame = ttk.Frame(detail_notebook)
    detail_notebook.add(di_frame, text="地盘")
    di_text = scrolledtext.ScrolledText(di_frame, font=("微软雅黑", 10))
    di_text.pack(fill='both', expand=True, padx=5, pady=5)
    frame.di_text = di_text
    
    # 天盘显示
    tian_frame = ttk.Frame(detail_notebook)
    detail_notebook.add(tian_frame, text="天盘")
    tian_text = scrolledtext.ScrolledText(tian_frame, font=("微软雅黑", 10))
    tian_text.pack(fill='both', expand=True, padx=5, pady=5)
    frame.tian_text = tian_text
    
    # 人盘显示
    ren_frame = ttk.Frame(detail_notebook)
    detail_notebook.add(ren_frame, text="人盘")
    ren_text = scrolledtext.ScrolledText(ren_frame, font=("微软雅黑", 10))
    ren_text.pack(fill='both', expand=True, padx=5, pady=5)
    frame.ren_text = ren_text
    
    # 神盘显示
    shen_frame = ttk.Frame(detail_notebook)
    detail_notebook.add(shen_frame, text="神盘")
    shen_text = scrolledtext.ScrolledText(shen_frame, font=("微软雅黑", 10))
    shen_text.pack(fill='both', expand=True, padx=5, pady=5)
    frame.shen_text = shen_text
    
    return frame

def create_detailed_analysis_tab(notebook):
    """创建详细分析标签页"""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="详细分析")
    
    # 顶部控制面板
    control_frame = ttk.Frame(frame)
    control_frame.pack(fill='x', padx=10, pady=10)
    
    def analyze_detailed_callback():
        global current_pan, current_analysis
        if not current_pan:
            messagebox.showerror("错误", "请先进行排盘")
            return
        
        # 获取问题类型
        question_type = root.frames['input'].question_type_var.get()
        if not question_type:
            messagebox.showerror("错误", "请先在输入参数页选择问题类型")
            return
        
        # 检查是否有用神分析
        if not current_analysis:
            messagebox.showerror("错误", "请先在输入参数页完成排盘和用神分析")
            return
        
        yongshen_info = current_analysis.get('yongshen_info', {})
        
        # 进行详细分析
        root.status_var.set("正在分析...")
        root.update()
        
        # 格局分析
        patterns_result = analyze_patterns(current_pan)
        
        # 应期分析
        timing_result = predict_timing(current_pan, yongshen_info, question_type)
        
        # 合并结果
        detailed_result = f"{'='*50}\n"
        detailed_result += "奇门遁甲详细分析报告\n"
        detailed_result += f"{'='*50}\n\n"
        
        detailed_result += "【格局分析】\n"
        detailed_result += "-"*40 + "\n"
        detailed_result += patterns_result + "\n\n"
        
        detailed_result += timing_result
        
        # 显示结果
        analysis_text.delete(1.0, tk.END)
        analysis_text.insert(tk.END, detailed_result)
        
        root.status_var.set("详细分析完成")
    
    analyze_btn = ttk.Button(control_frame, text="开始详细分析", command=analyze_detailed_callback)
    analyze_btn.pack(pady=5)
    
    # 分析结果显示
    analysis_text = scrolledtext.ScrolledText(frame, font=("微软雅黑", 11), wrap=tk.WORD)
    analysis_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
    
    frame.analysis_text = analysis_text
    
    return frame
    
def update_pan_display(pan):
    """更新排盘显示（添加用神信息）"""
    pan_frame = root.frames['pan']
    
    # 更新基本信息
    info_text = pan_frame.info_text
    info_text.delete(1.0, tk.END)
    
    basic_info = pan['基本信息']
    info_text.insert(tk.END, f"📅 时间: {basic_info['时间']}\n")
    info_text.insert(tk.END, f"🌡 节气: {basic_info['节气']}\n")
    info_text.insert(tk.END, f"🌓 阴阳遁: {basic_info['阴阳遁']}\n")
    info_text.insert(tk.END, f"🔢 局数: {basic_info['局数']}局\n")
    info_text.insert(tk.END, f"⭐ 值符: {pan['值符']}\n")
    info_text.insert(tk.END, f"🚪 值使: {pan['值使']}\n")
    
    # 更新四柱信息
    four_pillars = basic_info['四柱']
    info_text.insert(tk.END, f"\n📅 四柱:\n")
    info_text.insert(tk.END, f"  年柱: {four_pillars['年']}\n")
    info_text.insert(tk.END, f"  月柱: {four_pillars['月']}\n")
    info_text.insert(tk.END, f"  日柱: {four_pillars['日']}\n")
    info_text.insert(tk.END, f"  时柱: {four_pillars['时']}\n")
    
    # 添加用神分析结果
    if current_analysis and 'yongshen_info' in current_analysis:
        info_text.insert(tk.END, f"\n🧭 用神分析:\n")
        yongshen = current_analysis['yongshen_info']
        info_text.insert(tk.END, f"  类型: {yongshen.get('类型', '')}\n")
        info_text.insert(tk.END, f"  代表: {yongshen.get('代表', '')}\n")
        info_text.insert(tk.END, f"  符号: {yongshen.get('符号', '')}\n")
        info_text.insert(tk.END, f"  宫位: {yongshen.get('宫位', '')}\n")
        info_text.insert(tk.END, f"  状态: {yongshen.get('状态', '')}\n")
    
    # 更新排盘详情
    positions = ['坎', '坤', '震', '巽', '中', '乾', '兑', '艮', '离']
    
    # 地盘
    di_text = pan_frame.di_text
    di_text.delete(1.0, tk.END)
    di_text.insert(tk.END, "地盘（三奇六仪）：\n\n")
    for pos in positions:
        earth = pan['地盘'].get(pos, '')
        di_text.insert(tk.END, f"{pos}宫: {earth}\n")
    
    # 天盘
    tian_text = pan_frame.tian_text
    tian_text.delete(1.0, tk.END)
    tian_text.insert(tk.END, "天盘（九星）：\n\n")
    for pos in positions:
        heaven = pan['天盘'].get(pos, '')
        tian_text.insert(tk.END, f"{pos}宫: {heaven}\n")
    
    # 人盘
    ren_text = pan_frame.ren_text
    ren_text.delete(1.0, tk.END)
    ren_text.insert(tk.END, "人盘（八门）：\n\n")
    for pos in positions:
        human = pan['人盘'].get(pos, '')
        ren_text.insert(tk.END, f"{pos}宫: {human}\n")
    
    # 神盘
    shen_text = pan_frame.shen_text
    shen_text.delete(1.0, tk.END)
    shen_text.insert(tk.END, "神盘（八神）：\n\n")
    for pos in positions:
        god = pan['神盘'].get(pos, '')
        shen_text.insert(tk.END, f"{pos}宫: {god}\n")

def main():
    """主程序"""
    global root
    root = create_main_window()
    root.mainloop()

if __name__ == "__main__":
    main()