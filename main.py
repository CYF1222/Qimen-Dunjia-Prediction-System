# qimen_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime
import sys
import io
from yuce_functions import *

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 全局变量
current_pan = None
current_analysis = None
root = None

def create_main_window():
    """创建主窗口 - 全屏优化版本"""
    global root
    root = tk.Tk()
    root.title("奇门遁甲排盘分析系统")
    
    # 设置窗口最大化
    root.state('zoomed')
    
    # 设置窗口图标（如果有的话）
    # root.iconbitmap('qimen_icon.ico')
    
    # 绑定快捷键
    root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))
    root.bind('<F11>', lambda e: root.attributes('-fullscreen', 
                not root.attributes('-fullscreen')))
    
    # 创建主框架
    main_frame = ttk.Frame(root)
    main_frame.pack(fill='both', expand=True)
    
    # 创建标题栏
    title_frame = ttk.Frame(main_frame)
    title_frame.pack(fill='x', pady=5)
    
    title_label = ttk.Label(title_frame, text="奇门遁甲排盘分析系统", 
                           font=("Arial", 16, "bold"))
    title_label.pack(side="left", padx=10)
    
    # 创建标签页
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill='both', expand=True, padx=5, pady=5)
    
    # 创建各个标签页
    input_frame = create_input_tab(notebook)
    pan_frame = create_pan_display_tab(notebook)
    analysis_frame = create_analysis_tab(notebook)
    yongshen_frame = create_yongshen_tab(notebook)
    timing_frame = create_timing_tab(notebook)
    report_frame = create_report_tab(notebook)
    
    # 存储框架引用
    root.frames = {
        'input': input_frame,
        'pan': pan_frame,
        'analysis': analysis_frame,
        'yongshen': yongshen_frame,
        'timing': timing_frame,
        'report': report_frame
    }
    
    # 状态栏
    status_frame = ttk.Frame(main_frame)
    status_frame.pack(fill='x', pady=(5, 0))
    
    status_var = tk.StringVar(value="就绪 - 按F11切换全屏，按Esc退出全屏")
    status_label = ttk.Label(status_frame, textvariable=status_var, 
                            font=("Arial", 9), relief="sunken")
    status_label.pack(fill='x', padx=2, pady=2)
    
    root.status_var = status_var
    
    return root

def create_input_tab(notebook):
    """创建输入参数标签页 - 居中显示"""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="📅 输入参数")
    
    # 配置网格权重，使内容居中
    for i in range(5):
        frame.grid_rowconfigure(i, weight=1)
    for i in range(4):
        frame.grid_columnconfigure(i, weight=1)
    
    # 创建主内容容器，使其居中
    content_frame = ttk.Frame(frame)
    content_frame.grid(row=2, column=2, sticky="nsew", padx=20, pady=20)
    
    # 时间输入
    ttk.Label(content_frame, text="时间输入", font=("Arial", 14, "bold")).grid(
        row=0, column=0, columnspan=4, pady=15
    )
    
    # 年
    ttk.Label(content_frame, text="年:", font=("Arial", 11)).grid(
        row=1, column=0, padx=10, pady=8, sticky="e"
    )
    year_var = tk.StringVar(value=str(datetime.datetime.now().year))
    year_entry = ttk.Entry(content_frame, textvariable=year_var, width=10, font=("Arial", 11))
    year_entry.grid(row=1, column=1, padx=5, pady=8, sticky="w")
    
    # 月
    ttk.Label(content_frame, text="月:", font=("Arial", 11)).grid(
        row=1, column=2, padx=10, pady=8, sticky="e"
    )
    month_var = tk.StringVar(value=str(datetime.datetime.now().month))
    month_entry = ttk.Entry(content_frame, textvariable=month_var, width=10, font=("Arial", 11))
    month_entry.grid(row=1, column=3, padx=5, pady=8, sticky="w")
    
    # 日
    ttk.Label(content_frame, text="日:", font=("Arial", 11)).grid(
        row=2, column=0, padx=10, pady=8, sticky="e"
    )
    day_var = tk.StringVar(value=str(datetime.datetime.now().day))
    day_entry = ttk.Entry(content_frame, textvariable=day_var, width=10, font=("Arial", 11))
    day_entry.grid(row=2, column=1, padx=5, pady=8, sticky="w")
    
    # 时
    ttk.Label(content_frame, text="时:", font=("Arial", 11)).grid(
        row=2, column=2, padx=10, pady=8, sticky="e"
    )
    hour_var = tk.StringVar(value=str(datetime.datetime.now().hour))
    hour_entry = ttk.Entry(content_frame, textvariable=hour_var, width=10, font=("Arial", 11))
    hour_entry.grid(row=2, column=3, padx=5, pady=8, sticky="w")
    
    # 问题类型选择
    ttk.Label(content_frame, text="问题类型", font=("Arial", 14, "bold")).grid(
        row=3, column=0, columnspan=4, pady=15
    )
    
    # 移除了默认值，让用户手动选择
    question_type_var = tk.StringVar(value="")
    question_types = [
        "工作事业", "财运求财", "婚姻感情", "疾病健康", 
        "考试学习", "官司诉讼", "出行安全", "其他"
    ]
    
    # 使用 tk.Radiobutton，因为 ttk.Radiobutton 不支持 font 参数
    for i, q_type in enumerate(question_types):
        tk.Radiobutton(content_frame, text=q_type, variable=question_type_var, 
                       value=q_type, font=("Arial", 10)).grid(
            row=4 + i, column=0, columnspan=4, sticky="w", padx=20, pady=3
        )
    
    # 排盘按钮 - 居中显示
    def paipan_callback():
        global current_pan
        try:
            year = int(year_var.get())
            month = int(month_var.get())
            day = int(day_var.get())
            hour = int(hour_var.get())
            question_type = question_type_var.get()
            
            if not question_type:
                messagebox.showerror("错误", "请选择问题类型")
                return
            
            # 更新状态
            root.status_var.set("正在排盘...")
            
            # 调用排盘函数
            current_pan = create_qimen_pan(year, month, day, hour)
            
            # 更新状态
            root.status_var.set("排盘完成！")
            messagebox.showinfo("成功", "排盘完成！")
            
            # 更新其他标签页
            update_pan_display(current_pan)
            update_analysis_tab(current_pan, question_type)
            
        except ValueError as e:
            root.status_var.set("输入参数错误")
            messagebox.showerror("错误", f"输入参数错误: {e}")
        except Exception as e:
            root.status_var.set("排盘过程出错")
            messagebox.showerror("错误", f"排盘过程中出现错误: {e}")
        finally:
            root.status_var.set("就绪")
    
    # 创建按钮框架，使其居中
    button_frame = ttk.Frame(content_frame)
    button_frame.grid(row=12, column=0, columnspan=4, pady=25)
    
    paipan_btn = ttk.Button(button_frame, text="开始排盘", 
                           command=paipan_callback)
    paipan_btn.pack(pady=10, ipadx=20, ipady=10)
    
    # 存储变量供其他函数使用
    frame.year_var = year_var
    frame.month_var = month_var
    frame.day_var = day_var
    frame.hour_var = hour_var
    frame.question_type_var = question_type_var
    
    return frame

def create_pan_display_tab(notebook):
    """创建排盘显示标签页"""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="排盘显示")
    
    # 基本信息显示
    info_frame = ttk.LabelFrame(frame, text="基本信息")
    info_frame.pack(fill='x', padx=20, pady=10)
    
    info_text = scrolledtext.ScrolledText(info_frame, height=6, font=("Arial", 10))
    info_text.pack(fill='both', padx=10, pady=10)
    frame.info_text = info_text
    
    # 创建九宫格显示区域
    pan_frame = ttk.LabelFrame(frame, text="奇门盘局")
    pan_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    # 创建表格显示
    tree = ttk.Treeview(pan_frame, columns=('宫位', '地盘', '天盘', '人盘', '神盘'), show='headings', height=9)
    
    # 设置列标题
    tree.heading('宫位', text='宫位')
    tree.heading('地盘', text='地盘')
    tree.heading('天盘', text='天盘') 
    tree.heading('人盘', text='人盘')
    tree.heading('神盘', text='神盘')
    
    # 设置列宽
    tree.column('宫位', width=80)
    tree.column('地盘', width=120)
    tree.column('天盘', width=120)
    tree.column('人盘', width=120)
    tree.column('神盘', width=120)
    
    tree.pack(fill='both', expand=True, padx=10, pady=10)
    frame.tree = tree
    
    return frame

def create_analysis_tab(notebook):
    """创建分析标签页"""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="格局分析")
    
    # 创建分析结果显示区域
    analysis_text = scrolledtext.ScrolledText(frame, font=("Arial", 11), wrap=tk.WORD)
    analysis_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    frame.analysis_text = analysis_text
    
    return frame

def create_yongshen_tab(notebook):
    """创建用神分析标签页 - 优化布局版本"""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="用神分析")
    
    # 配置网格权重，使结果区域可以扩展
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    # 上部控制面板框架
    control_frame = ttk.Frame(frame)
    control_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
    control_frame.grid_columnconfigure(0, weight=1)
    
    # 用神选择框架
    yongshen_frame = ttk.LabelFrame(control_frame, text="用神选择")
    yongshen_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    
    # 使用网格布局来组织控件
    yongshen_frame.grid_columnconfigure(1, weight=1)
    
    # 用神选择标签
    ttk.Label(yongshen_frame, text="选择用神类型:", font=("Arial", 10, "bold")).grid(
        row=0, column=0, sticky="w", padx=10, pady=5
    )
    
    # 用神选择单选按钮
    yongshen_var = tk.StringVar(value="")
    yongshen_options = [
        "日干(自己)", "年命(他人)", "时干(事体)", "值符(领导)", 
        "年干(上级)", "月干(平辈)", "特定用神"
    ]
    
    # 创建单选按钮并布局
    for i, option in enumerate(yongshen_options):
        tk.Radiobutton(yongshen_frame, text=option, variable=yongshen_var, 
                       value=option).grid(
            row=1 + i, column=0, columnspan=2, sticky="w", padx=20, pady=2
        )
    
    # 特定用神输入框架
    input_frame = ttk.Frame(yongshen_frame)
    input_frame.grid(row=len(yongshen_options) + 1, column=0, columnspan=2, sticky="w", padx=20, pady=10)
    
    ttk.Label(input_frame, text="输入内容:").pack(side=tk.LEFT, padx=(0, 5))
    specific_yongshen_var = tk.StringVar()
    specific_entry = ttk.Entry(input_frame, textvariable=specific_yongshen_var, width=25)
    specific_entry.pack(side=tk.LEFT)
    
    # 输入提示标签
    input_tip_var = tk.StringVar(value="请选择用神类型")
    input_tip_label = ttk.Label(input_frame, textvariable=input_tip_var, 
                                font=("Arial", 9), foreground="blue")
    input_tip_label.pack(side=tk.LEFT, padx=(10, 0))
    
    # 分析按钮框架
    button_frame = ttk.Frame(yongshen_frame)
    button_frame.grid(row=len(yongshen_options) + 2, column=0, columnspan=2, pady=15)
    
    def analyze_yongshen_callback():
        global current_pan, current_analysis
        if not current_pan:
            messagebox.showerror("错误", "请先进行排盘")
            return
        
        yongshen_type = yongshen_var.get()
        if not yongshen_type:
            messagebox.showerror("错误", "请选择用神类型")
            return
        
        # 检查年命类型是否需要输入
        if yongshen_type == "年命(他人)" and not specific_yongshen_var.get():
            messagebox.showerror("错误", "年命类型需要输入出生年份或干支")
            return
        
        # 进行用神分析
        current_analysis = analyze_yongshen(current_pan, yongshen_type, specific_yongshen_var.get())
        
        # 显示分析结果
        yongshen_text.delete(1.0, tk.END)
        result = current_analysis.get('yongshen_report', '分析结果')
        yongshen_text.insert(tk.END, result)
        
        # 更新状态
        root.status_var.set("用神分析完成")
    
    analyze_btn = ttk.Button(button_frame, text="分析用神", command=analyze_yongshen_callback)
    analyze_btn.pack(padx=10, pady=5)
    
    # 动态更新输入提示
    def update_input_tip(*args):
        selected_type = yongshen_var.get()
        if selected_type == "年命(他人)":
            input_tip_var.set("请输入出生年份(如1984)或干支(如甲子)")
            specific_entry.config(state="normal")
        elif selected_type == "特定用神":
            input_tip_var.set("请输入天干、九星、八门等符号")
            specific_entry.config(state="normal")
        else:
            input_tip_var.set("自动获取，无需输入")
            specific_yongshen_var.set("")  # 清空输入框
            specific_entry.config(state="disabled")
    
    yongshen_var.trace('w', update_input_tip)
    
    # 下部结果区域 - 使用更大的空间
    result_frame = ttk.LabelFrame(frame, text="用神分析结果")
    result_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
    result_frame.grid_rowconfigure(0, weight=1)
    result_frame.grid_columnconfigure(0, weight=1)
    
    # 用神分析结果显示 - 更大的文本区域
    yongshen_text = scrolledtext.ScrolledText(
        result_frame, 
        font=("Arial", 11), 
        wrap=tk.WORD,
        padx=10,
        pady=10
    )
    yongshen_text.grid(row=0, column=0, sticky="nsew")
    
    # 添加滚动条增强
    scrollbar = ttk.Scrollbar(result_frame, command=yongshen_text.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    yongshen_text.config(yscrollcommand=scrollbar.set)
    
    # 存储变量供其他函数使用
    frame.yongshen_var = yongshen_var
    frame.specific_yongshen_var = specific_yongshen_var
    frame.yongshen_text = yongshen_text
    frame.input_tip_var = input_tip_var
    
    return frame

def create_timing_tab(notebook):
    """创建应期判断标签页"""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="应期判断")
    
    # 应期分析按钮
    def analyze_timing_callback():
        global current_pan
        if not current_pan:
            messagebox.showerror("错误", "请先进行排盘")
            return
        
        # 获取问题类型
        question_type = root.frames['input'].question_type_var.get()
        if not question_type:
            messagebox.showerror("错误", "请先在输入参数页选择问题类型")
            return
        
        # 进行应期分析
        timing_result = predict_timing(current_pan, question_type)
        
        # 显示分析结果
        timing_text.delete(1.0, tk.END)
        timing_text.insert(tk.END, timing_result)
    
    ttk.Button(frame, text="分析应期", command=analyze_timing_callback).pack(pady=10)
    
    # 应期分析结果显示
    timing_text = scrolledtext.ScrolledText(frame, font=("Arial", 11), wrap=tk.WORD)
    timing_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    frame.timing_text = timing_text
    
    return frame

def create_report_tab(notebook):
    """创建综合报告标签页"""
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="综合报告")
    
    # 报告生成按钮
    def generate_report_callback():
        global current_pan, current_analysis
        if not current_pan:
            messagebox.showerror("错误", "请先完成排盘")
            return
        
        # 生成综合报告
        report = generate_comprehensive_report(current_pan, current_analysis)
        
        # 显示报告
        report_text.delete(1.0, tk.END)
        report_text.insert(tk.END, report)
    
    ttk.Button(frame, text="生成综合报告", command=generate_report_callback).pack(pady=10)
    
    # 报告显示区域
    report_text = scrolledtext.ScrolledText(frame, font=("Arial", 11), wrap=tk.WORD)
    report_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    frame.report_text = report_text
    
    return frame

def update_pan_display(pan):
    """更新排盘显示"""
    # 获取排盘显示标签页的frame
    pan_frame = root.frames['pan']
    
    # 更新基本信息
    info_text = pan_frame.info_text
    info_text.delete(1.0, tk.END)
    
    basic_info = pan['基本信息']
    info_text.insert(tk.END, f"时间: {basic_info['时间']}\n")
    info_text.insert(tk.END, f"节气: {basic_info['节气']}\n")
    info_text.insert(tk.END, f"阴阳遁: {basic_info['阴阳遁']}\n")
    info_text.insert(tk.END, f"局数: {basic_info['局数']}局\n")
    info_text.insert(tk.END, f"值符: {pan['值符']}\n")
    info_text.insert(tk.END, f"值使: {pan['值使']}\n")
    
    # 更新四柱信息
    four_pillars = basic_info['四柱']
    info_text.insert(tk.END, f"\n四柱:\n")
    info_text.insert(tk.END, f"  年柱: {four_pillars['年']}\n")
    info_text.insert(tk.END, f"  月柱: {four_pillars['月']}\n")
    info_text.insert(tk.END, f"  日柱: {four_pillars['日']}\n")
    info_text.insert(tk.END, f"  时柱: {four_pillars['时']}\n")
    
    # 更新九宫格显示
    tree = pan_frame.tree
    # 清空现有数据
    for item in tree.get_children():
        tree.delete(item)
    
    # 宫位顺序
    positions = ['坎', '坤', '震', '巽', '中', '乾', '兑', '艮', '离']
    
    for pos in positions:
        earth = pan['地盘'].get(pos, '')
        heaven = pan['天盘'].get(pos, '')
        human = pan['人盘'].get(pos, '')
        god = pan['神盘'].get(pos, '')
        
        tree.insert('', 'end', values=(pos, earth, heaven, human, god))

def update_analysis_tab(pan, question_type):
    """更新分析标签页"""
    # 获取分析标签页的frame
    analysis_frame = root.frames['analysis']
    
    # 进行格局分析
    analysis_result = analyze_patterns(pan)
    
    # 显示分析结果
    analysis_text = analysis_frame.analysis_text
    analysis_text.delete(1.0, tk.END)
    
    analysis_text.insert(tk.END, f"问题类型: {question_type}\n\n")
    analysis_text.insert(tk.END, analysis_result)

# 主程序
def main():
    global root
    root = create_main_window()
    root.mainloop()

if __name__ == "__main__":
    main()