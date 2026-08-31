import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from data import *
from yuce_yongshen import analyze_yongshen
from yuce_utils import *
from yuce_predictions import predict_timing
from yuce_patterns import analyze_patterns
from paipan_functions import create_qimen_pan

def create_main_window():
    global root
    root = tk.Tk()
    root.title("奇门遁甲排盘系统")
    root.geometry("600x800")
    main_frame = ttk.Frame(root)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    title_label = ttk.Label(main_frame, text="奇门遁甲排盘分析系统", font=("微软雅黑", 16, "bold"))
    title_label.pack(pady=(0, 20))
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill='both', expand=True)
    input_frame = create_input_tab(notebook)
    pan_frame = create_pan_display_tab(notebook)
    detailed_frame = create_detailed_analysis_tab(notebook)
    root.frames = {'input': input_frame, 'pan': pan_frame, 'detailed': detailed_frame}
    status_frame = ttk.Frame(main_frame)
    status_frame.pack(fill='x', pady=(10, 0))
    status_var = tk.StringVar(value="就绪")
    status_label = ttk.Label(status_frame, textvariable=status_var, font=("微软雅黑", 9), relief="sunken")
    status_label.pack(fill='x')
    root.status_var = status_var
    return root

def create_input_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="输入参数")
    canvas = tk.Canvas(frame)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    container = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=container, anchor="nw", width=canvas.winfo_reqwidth())
    container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    outer_frame = ttk.Frame(container)
    outer_frame.pack(expand=True, fill="both")
    center_frame = ttk.Frame(outer_frame)
    center_frame.pack(expand=True)
    content_frame = ttk.Frame(center_frame)
    content_frame.pack(pady=20)
    
    # 时间输入
    time_frame = ttk.LabelFrame(content_frame, text="📅 时间输入", padding=15)
    time_frame.pack(fill='x', pady=(0, 15))
    time_grid = ttk.Frame(time_frame)
    time_grid.pack(fill='x', padx=10, pady=5)
    now = datetime.now()
    time_fields = [
        ("年", "year", now.year, 0, 0, (0, 5)),
        ("月", "month", now.month, 0, 2, (20, 5)),
        ("日", "day", now.day, 1, 0, (0, 5)),
        ("时", "hour", now.hour, 1, 2, (20, 5))
    ]
    vars_dict = {}
    for label, name, value, row, col, padx in time_fields:
        ttk.Label(time_grid, text=f"{label}:", width=5).grid(row=row, column=col, padx=padx, pady=5, sticky="e")
        var = tk.StringVar(value=str(value))
        ttk.Entry(time_grid, textvariable=var, width=15).grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
        vars_dict[name] = var
    frame.year_var = vars_dict['year']
    frame.month_var = vars_dict['month']
    frame.day_var = vars_dict['day']
    frame.hour_var = vars_dict['hour']
    
    # 问题类型
    question_frame = ttk.LabelFrame(content_frame, text="❓ 问题类型", padding=15)
    question_frame.pack(fill='x', pady=(0, 15))
    question_grid = ttk.Frame(question_frame)
    question_grid.pack(fill='x', padx=10, pady=5)
    question_types = ["工作事业", "财运求财", "婚姻感情", "疾病健康", "考试学习", "官司诉讼", "出行安全"]
    question_type_var = tk.StringVar(value="")
    for i, q_type in enumerate(question_types):
        row, col = i // 2, i % 2
        padx = (0, 30) if col == 0 else 0
        rb_frame = ttk.Frame(question_grid)
        rb_frame.grid(row=row, column=col, sticky='w', padx=padx, pady=2)
        ttk.Radiobutton(rb_frame, text=q_type, variable=question_type_var, value=q_type, width=10).pack(side=tk.LEFT)
    frame.question_type_var = question_type_var
    
    # 用神选择
    yongshen_frame = ttk.LabelFrame(content_frame, text="🧭 用神选择", padding=15)
    yongshen_frame.pack(fill='x', pady=(0, 20))
    type_row = ttk.Frame(yongshen_frame)
    type_row.pack(fill='x', pady=5, padx=10)
    ttk.Label(type_row, text="用神类型:", font=("微软雅黑", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
    yongshen_var = tk.StringVar(value="日干(自己)")
    yongshen_combo = ttk.Combobox(type_row, textvariable=yongshen_var, 
                                 values=["日干(自己)", "年命(他人)", "时干(事体)", "值符(领导)", "年干(上级)", "月干(平辈)", "特定用神"], 
                                 width=18, state="readonly")
    yongshen_combo.pack(side=tk.LEFT, padx=(0, 15))
    specific_frame = ttk.Frame(yongshen_frame)
    specific_var = tk.StringVar()
    specific_label = ttk.Label(specific_frame, text="出生年份/干支:")
    specific_label.pack(side=tk.LEFT, padx=(0, 5))
    specific_entry = ttk.Entry(specific_frame, textvariable=specific_var, width=15)
    specific_entry.pack(side=tk.LEFT)
    hint_label = ttk.Label(yongshen_frame, text="选择日干(自己)进行分析", font=("微软雅黑", 9), foreground="gray")
    hint_label.pack(fill='x', pady=(5, 0), padx=10)
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
    frame.yongshen_var = yongshen_var
    frame.specific_var = specific_var
    
    # 排盘按钮
    button_frame = ttk.Frame(content_frame)
    button_frame.pack(fill='x', pady=(10, 0))
    style = ttk.Style()
    style.configure("Big.TButton", font=("微软雅黑", 12, "bold"), padding=10)
    paipan_btn = ttk.Button(button_frame, text="🚀 开始排盘", command=paipan_callback, style="Big.TButton")
    paipan_btn.pack(pady=20, ipadx=30, ipady=12)
    
    return frame

def paipan_callback():
    global current_pan, current_analysis
    try:
        input_frame = root.frames['input']
        year = int(input_frame.year_var.get())
        month = int(input_frame.month_var.get())
        day = int(input_frame.day_var.get())
        hour = int(input_frame.hour_var.get())
        question_type = input_frame.question_type_var.get()
        if not question_type:
            messagebox.showerror("错误", "请选择问题类型")
            return
        root.status_var.set("正在排盘...")
        root.update()
        current_pan = create_qimen_pan(year, month, day, hour)
        yongshen_type = input_frame.yongshen_var.get()
        specific_yongshen = input_frame.specific_var.get()
        if yongshen_type == "年命(他人)" and not specific_yongshen:
            messagebox.showerror("错误", "年命类型需要输入出生年份或干支")
            root.status_var.set("就绪")
            return
        elif yongshen_type == "特定用神" and not specific_yongshen:
            messagebox.showerror("错误", "特定用神需要输入内容")
            root.status_var.set("就绪")
            return
        current_analysis = analyze_yongshen(current_pan, yongshen_type, specific_yongshen, question_type)
        root.status_var.set("排盘完成")
        update_pan_display(current_pan)
        root.frames['detailed'].analysis_text.delete(1.0, tk.END)
        messagebox.showinfo("成功", "排盘完成！")
    except ValueError as e:
        root.status_var.set("输入参数错误")
        messagebox.showerror("错误", f"请输入正确的数字: {e}")
    except Exception as e:
        root.status_var.set("排盘过程出错")
        messagebox.showerror("错误", f"排盘过程中出现错误: {e}")

def create_pan_display_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="排盘详情")
    left_frame = ttk.Frame(frame)
    left_frame.pack(side=tk.LEFT, fill='y', padx=(0, 10))
    info_frame = ttk.LabelFrame(left_frame, text="基本信息")
    info_frame.pack(fill='x', pady=(0, 10))
    info_text = scrolledtext.ScrolledText(info_frame, height=10, width=30, font=("微软雅黑", 10))
    info_text.pack(fill='both', padx=5, pady=5)
    frame.info_text = info_text
    right_frame = ttk.Frame(frame)
    right_frame.pack(side=tk.RIGHT, fill='both', expand=True)
    detail_notebook = ttk.Notebook(right_frame)
    detail_notebook.pack(fill='both', expand=True)
    pan_types = [("地盘", "地盘（三奇六仪）："), ("天盘", "天盘（九星）："), ("人盘", "人盘（八门）："), ("神盘", "神盘（八神）：")]
    for pan_name, title in pan_types:
        pan_frame = ttk.Frame(detail_notebook)
        detail_notebook.add(pan_frame, text=pan_name)
        pan_text = scrolledtext.ScrolledText(pan_frame, font=("微软雅黑", 10))
        pan_text.pack(fill='both', expand=True, padx=5, pady=5)
        setattr(frame, f"{pan_name.lower()}_text", pan_text)
    return frame

def create_detailed_analysis_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="详细分析")
    control_frame = ttk.Frame(frame)
    control_frame.pack(fill='x', padx=10, pady=10)
    analyze_btn = ttk.Button(control_frame, text="开始详细分析", command=analyze_detailed_callback)
    analyze_btn.pack(pady=5)
    analysis_text = scrolledtext.ScrolledText(frame, font=("微软雅黑", 11), wrap=tk.WORD)
    analysis_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
    frame.analysis_text = analysis_text
    return frame

def analyze_detailed_callback():
    global current_pan, current_analysis
    if not current_pan:
        messagebox.showerror("错误", "请先进行排盘")
        return
    question_type = root.frames['input'].question_type_var.get()
    if not question_type:
        messagebox.showerror("错误", "请先在输入参数页选择问题类型")
        return
    if not current_analysis:
        messagebox.showerror("错误", "请先在输入参数页完成排盘和用神分析")
        return
    yongshen_info = current_analysis.get('yongshen_info', {})
    root.status_var.set("正在分析...")
    root.update()
    patterns_result = analyze_patterns(current_pan)
    timing_result = predict_timing(current_pan, yongshen_info, question_type)
    detailed_result = f"{'='*50}\n奇门遁甲详细分析报告\n{'='*50}\n\n【格局分析】\n{'-'*40}\n{patterns_result}\n\n{timing_result}"
    analysis_text = root.frames['detailed'].analysis_text
    analysis_text.delete(1.0, tk.END)
    analysis_text.insert(tk.END, detailed_result)
    root.status_var.set("详细分析完成")

def update_pan_display(pan):
    pan_frame = root.frames['pan']
    info_text = pan_frame.info_text
    info_text.delete(1.0, tk.END)
    basic_info = pan['基本信息']
    info_text.insert(tk.END, f"📅 时间: {basic_info['时间']}\n")
    info_text.insert(tk.END, f"🌡 节气: {basic_info['节气']}\n")
    info_text.insert(tk.END, f"🌓 阴阳遁: {basic_info['阴阳遁']}\n")
    info_text.insert(tk.END, f"🔢 局数: {basic_info['局数']}局\n")
    info_text.insert(tk.END, f"⭐ 值符: {pan['值符']}\n")
    info_text.insert(tk.END, f"🚪 值使: {pan['值使']}\n")
    four_pillars = basic_info['四柱']
    info_text.insert(tk.END, f"\n📅 四柱:\n")
    info_text.insert(tk.END, f"  年柱: {four_pillars['年']}\n")
    info_text.insert(tk.END, f"  月柱: {four_pillars['月']}\n")
    info_text.insert(tk.END, f"  日柱: {four_pillars['日']}\n")
    info_text.insert(tk.END, f"  时柱: {four_pillars['时']}\n")
    if current_analysis and 'yongshen_info' in current_analysis:
        info_text.insert(tk.END, f"\n🧭 用神分析:\n")
        yongshen = current_analysis['yongshen_info']
        info_text.insert(tk.END, f"  类型: {yongshen.get('类型', '')}\n")
        info_text.insert(tk.END, f"  代表: {yongshen.get('代表', '')}\n")
        info_text.insert(tk.END, f"  符号: {yongshen.get('符号', '')}\n")
        info_text.insert(tk.END, f"  宫位: {yongshen.get('宫位', '')}\n")
        info_text.insert(tk.END, f"  状态: {yongshen.get('状态', '')}\n")
    positions = ['坎', '坤', '震', '巽', '中', '乾', '兑', '艮', '离']
    pan_types = ['地盘', '天盘', '人盘', '神盘']
    for pan_type in pan_types:
        text_widget = getattr(pan_frame, f"{pan_type.lower()}_text")
        text_widget.delete(1.0, tk.END)
        if pan_type == '地盘':
            text_widget.insert(tk.END, "地盘（三奇六仪）：\n\n")
        elif pan_type == '天盘':
            text_widget.insert(tk.END, "天盘（九星）：\n\n")
        elif pan_type == '人盘':
            text_widget.insert(tk.END, "人盘（八门）：\n\n")
        elif pan_type == '神盘':
            text_widget.insert(tk.END, "神盘（八神）：\n\n")
        for pos in positions:
            value = pan[pan_type].get(pos, '')
            text_widget.insert(tk.END, f"{pos}宫: {value}\n")