import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from data import *
from yuce_yongshen import analyze_yongshen
from yuce_utils import *
from yuce_predictions import predict_timing
from yuce_patterns import analyze_patterns
from paipan_functions import create_qimen_pan

# 设置外观模式和颜色主题
ctk.set_appearance_mode("System")  # 跟随系统（也可设为 "Dark"/"Light"）
ctk.set_default_color_theme("blue")

# 全局变量（保持与原代码一致）
current_pan = None
current_analysis = None
root = None


def create_main_window():
    global root
    root = ctk.CTk()
    root.title("奇门遁甲排盘系统")
    root.geometry("800x900")
    root.minsize(700, 800)

    # 主容器
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=15, pady=15)

    # 标题
    title_label = ctk.CTkLabel(
        main_frame,
        text="奇门遁甲排盘分析系统",
        font=("微软雅黑", 20, "bold")
    )
    title_label.pack(pady=(0, 15))

    # Tab 视图
    tabview = ctk.CTkTabview(main_frame)
    tabview.pack(fill="both", expand=True)

    # 创建三个标签页
    input_tab = tabview.add("输入参数")
    pan_tab = tabview.add("排盘详情")
    detail_tab = tabview.add("详细分析")

    # 构建各标签页内容
    create_input_tab(input_tab)
    create_pan_display_tab(pan_tab)
    create_detailed_analysis_tab(detail_tab)

    # 保存引用（供回调函数使用）
    root.tabview = tabview
    root.input_tab = input_tab
    root.pan_tab = pan_tab
    root.detail_tab = detail_tab

    # 状态栏
    status_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    status_frame.pack(fill="x", pady=(10, 0))
    status_var = ctk.StringVar(value="就绪")
    status_label = ctk.CTkLabel(
        status_frame,
        textvariable=status_var,
        font=("微软雅黑", 11),
        anchor="w",
        fg_color=("gray85", "gray25"),
        corner_radius=5,
        height=30
    )
    status_label.pack(fill="x", padx=5)
    root.status_var = status_var

    return root


def create_input_tab(parent):
    """输入参数标签页"""
    # 使用可滚动框架（内容可能超出高度）
    scroll_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ---- 时间输入 ----
    time_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    time_frame.pack(fill="x", pady=(0, 15))

    ctk.CTkLabel(time_frame, text="📅 时间输入", font=("微软雅黑", 14, "bold")).pack(anchor="w", pady=(0, 10))

    time_grid = ctk.CTkFrame(time_frame, fg_color="transparent")
    time_grid.pack(fill="x")

    now = datetime.now()
    # 定义行、列布局
    fields = [
        ("年", "year", now.year, 0, 0),
        ("月", "month", now.month, 0, 2),
        ("日", "day", now.day, 1, 0),
        ("时", "hour", now.hour, 1, 2),
    ]
    vars_dict = {}
    for label, name, value, row, col in fields:
        ctk.CTkLabel(time_grid, text=f"{label}：", width=60, anchor="e").grid(
            row=row, column=col, padx=(0, 5), pady=8, sticky="e"
        )
        var = ctk.StringVar(value=str(value))
        entry = ctk.CTkEntry(time_grid, textvariable=var, width=120)
        entry.grid(row=row, column=col + 1, padx=(0, 20), pady=8, sticky="w")
        vars_dict[name] = var

    parent.year_var = vars_dict["year"]
    parent.month_var = vars_dict["month"]
    parent.day_var = vars_dict["day"]
    parent.hour_var = vars_dict["hour"]

    # ---- 问题类型 ----
    question_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    question_frame.pack(fill="x", pady=(0, 15))

    ctk.CTkLabel(question_frame, text="❓ 问题类型", font=("微软雅黑", 14, "bold")).pack(anchor="w", pady=(0, 10))

    # 使用单选按钮（分组）
    question_types = ["工作事业", "财运求财", "婚姻感情", "疾病健康", "考试学习", "官司诉讼", "出行安全"]
    question_type_var = ctk.StringVar(value="")

    # 用网格布局放置单选按钮
    radio_frame = ctk.CTkFrame(question_frame, fg_color="transparent")
    radio_frame.pack(fill="x", pady=5)

    for i, q_type in enumerate(question_types):
        row = i // 3
        col = i % 3
        rb = ctk.CTkRadioButton(
            radio_frame,
            text=q_type,
            variable=question_type_var,
            value=q_type,
            font=("微软雅黑", 12)
        )
        rb.grid(row=row, column=col, padx=(0, 20), pady=5, sticky="w")

    parent.question_type_var = question_type_var

    # ---- 用神选择 ----
    yongshen_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    yongshen_frame.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(yongshen_frame, text="🧭 用神选择", font=("微软雅黑", 14, "bold")).pack(anchor="w", pady=(0, 10))

    # 选择行
    select_row = ctk.CTkFrame(yongshen_frame, fg_color="transparent")
    select_row.pack(fill="x", pady=5)

    ctk.CTkLabel(select_row, text="用神类型：", font=("微软雅黑", 12)).pack(side="left", padx=(0, 10))

    yongshen_var = ctk.StringVar(value="日干(自己)")
    yongshen_combo = ctk.CTkComboBox(
        select_row,
        variable=yongshen_var,
        values=["日干(自己)", "年命(他人)", "时干(事体)", "值符(领导)", "年干(上级)", "月干(平辈)", "特定用神"],
        width=160,
        state="readonly"
    )
    yongshen_combo.pack(side="left")

    # 特定输入（初始隐藏）
    specific_frame = ctk.CTkFrame(yongshen_frame, fg_color="transparent")
    specific_var = ctk.StringVar()
    specific_label = ctk.CTkLabel(specific_frame, text="出生年份/干支：", font=("微软雅黑", 12))
    specific_label.pack(side="left", padx=(0, 5))
    specific_entry = ctk.CTkEntry(specific_frame, textvariable=specific_var, width=150)
    specific_entry.pack(side="left")
    # 默认隐藏
    specific_frame.pack_forget()

    # 提示标签
    hint_label = ctk.CTkLabel(
        yongshen_frame,
        text="自动获取日干(自己)进行分析",
        font=("微软雅黑", 11),
        text_color=("gray40", "gray70")
    )
    hint_label.pack(anchor="w", pady=(5, 0))

    # 用神切换事件
    def on_yongshen_change(choice):
        selected = yongshen_var.get()
        if selected == "年命(他人)":
            specific_label.configure(text="出生年份/干支：")
            specific_frame.pack(fill="x", pady=(10, 5))
            hint_label.configure(text="请输入出生年份（如1984）或干支（如甲子）")
        elif selected == "特定用神":
            specific_label.configure(text="特定符号：")
            specific_frame.pack(fill="x", pady=(10, 5))
            hint_label.configure(text="请输入天干、九星、八门等符号")
        else:
            specific_frame.pack_forget()
            hint_label.configure(text=f"自动获取{selected}进行分析")

    yongshen_combo.configure(command=on_yongshen_change)

    parent.yongshen_var = yongshen_var
    parent.specific_var = specific_var

    # ---- 排盘按钮 ----
    btn_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    btn_frame.pack(fill="x", pady=(10, 5))

    paipan_btn = ctk.CTkButton(
        btn_frame,
        text="🚀 开始排盘",
        font=("微软雅黑", 14, "bold"),
        height=50,
        corner_radius=10,
        command=paipan_callback
    )
    paipan_btn.pack(pady=10)


def paipan_callback():
    global current_pan, current_analysis
    try:
        input_tab = root.input_tab

        # 获取时间
        year = int(input_tab.year_var.get())
        month = int(input_tab.month_var.get())
        day = int(input_tab.day_var.get())
        hour = int(input_tab.hour_var.get())

        # 验证时间范围（简单）
        if not (1 <= month <= 12 and 1 <= day <= 31 and 0 <= hour <= 23):
            messagebox.showerror("错误", "请输入有效的时间（月1-12，日1-31，时0-23）")
            return

        question_type = input_tab.question_type_var.get()
        if not question_type:
            messagebox.showerror("错误", "请选择问题类型")
            return

        root.status_var.set("正在排盘...")
        root.update()

        # 排盘
        current_pan = create_qimen_pan(year, month, day, hour)

        # 用神分析
        yongshen_type = input_tab.yongshen_var.get()
        specific_yongshen = input_tab.specific_var.get()

        if yongshen_type == "年命(他人)" and not specific_yongshen:
            messagebox.showerror("错误", "年命类型需要输入出生年份或干支")
            root.status_var.set("就绪")
            return
        elif yongshen_type == "特定用神" and not specific_yongshen:
            messagebox.showerror("错误", "特定用神需要输入内容")
            root.status_var.set("就绪")
            return

        current_analysis = analyze_yongshen(
            current_pan, yongshen_type, specific_yongshen, question_type
        )

        root.status_var.set("排盘完成")
        update_pan_display(current_pan)
        # 清空详细分析内容
        root.detail_tab.analysis_text.delete("0.0", "end")
        messagebox.showinfo("成功", "排盘完成！")

    except ValueError as e:
        root.status_var.set("输入参数错误")
        messagebox.showerror("错误", f"请输入正确的数字：{e}")
    except Exception as e:
        root.status_var.set("排盘过程出错")
        messagebox.showerror("错误", f"排盘过程中出现错误：{e}")


def create_pan_display_tab(parent):
    """排盘详情标签页"""
    # 左右分栏
    left_frame = ctk.CTkFrame(parent, fg_color="transparent", width=300)
    left_frame.pack(side="left", fill="y", padx=(0, 10), pady=10)
    left_frame.pack_propagate(False)  # 固定宽度

    # 基本信息区域
    info_frame = ctk.CTkFrame(left_frame)
    info_frame.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(info_frame, text="基本信息", font=("微软雅黑", 13, "bold")).pack(anchor="w", padx=5, pady=(5, 0))

    info_text = ctk.CTkTextbox(info_frame, height=200, font=("微软雅黑", 11))
    info_text.pack(fill="both", expand=True, padx=5, pady=5)
    parent.info_text = info_text

    # 右侧：四个子标签
    right_frame = ctk.CTkFrame(parent, fg_color="transparent")
    right_frame.pack(side="right", fill="both", expand=True, pady=10)

    detail_tabview = ctk.CTkTabview(right_frame)
    detail_tabview.pack(fill="both", expand=True)

    pan_types = [("地盘", "地盘（三奇六仪）："), ("天盘", "天盘（九星）："), ("人盘", "人盘（八门）："), ("神盘", "神盘（八神）：")]
    for pan_name, title in pan_types:
        tab = detail_tabview.add(pan_name)
        text_widget = ctk.CTkTextbox(tab, font=("微软雅黑", 11))
        text_widget.pack(fill="both", expand=True, padx=5, pady=5)
        # 存储引用
        setattr(parent, f"{pan_name.lower()}_text", text_widget)


def create_detailed_analysis_tab(parent):
    """详细分析标签页"""
    # 按钮
    btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
    btn_frame.pack(fill="x", padx=10, pady=10)

    analyze_btn = ctk.CTkButton(
        btn_frame,
        text="开始详细分析",
        font=("微软雅黑", 13, "bold"),
        height=40,
        corner_radius=8,
        command=analyze_detailed_callback
    )
    analyze_btn.pack(pady=5)

    # 结果显示文本框
    analysis_text = ctk.CTkTextbox(parent, font=("微软雅黑", 12), wrap="word")
    analysis_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    parent.analysis_text = analysis_text


def analyze_detailed_callback():
    global current_pan, current_analysis
    if not current_pan:
        messagebox.showerror("错误", "请先进行排盘")
        return

    question_type = root.input_tab.question_type_var.get()
    if not question_type:
        messagebox.showerror("错误", "请先在输入参数页选择问题类型")
        return

    if not current_analysis:
        messagebox.showerror("错误", "请先在输入参数页完成排盘和用神分析")
        return

    yongshen_info = current_analysis.get("yongshen_info", {})
    root.status_var.set("正在分析...")
    root.update()

    patterns_result = analyze_patterns(current_pan)
    timing_result = predict_timing(current_pan, yongshen_info, question_type)

    detailed_result = f"{'='*50}\n奇门遁甲详细分析报告\n{'='*50}\n\n【格局分析】\n{'-'*40}\n{patterns_result}\n\n{timing_result}"

    analysis_text = root.detail_tab.analysis_text
    analysis_text.delete("0.0", "end")
    analysis_text.insert("0.0", detailed_result)

    root.status_var.set("详细分析完成")


def update_pan_display(pan):
    """更新排盘详情标签页的内容"""
    pan_tab = root.pan_tab
    info_text = pan_tab.info_text
    info_text.delete("0.0", "end")

    basic_info = pan["基本信息"]
    info_text.insert("end", f"📅 时间: {basic_info['时间']}\n")
    info_text.insert("end", f"🌡 节气: {basic_info['节气']}\n")
    info_text.insert("end", f"🌓 阴阳遁: {basic_info['阴阳遁']}\n")
    info_text.insert("end", f"🔢 局数: {basic_info['局数']}局\n")
    info_text.insert("end", f"⭐ 值符: {pan['值符']}\n")
    info_text.insert("end", f"🚪 值使: {pan['值使']}\n")

    four_pillars = basic_info["四柱"]
    info_text.insert("end", "\n📅 四柱:\n")
    info_text.insert("end", f"  年柱: {four_pillars['年']}\n")
    info_text.insert("end", f"  月柱: {four_pillars['月']}\n")
    info_text.insert("end", f"  日柱: {four_pillars['日']}\n")
    info_text.insert("end", f"  时柱: {four_pillars['时']}\n")

    if current_analysis and "yongshen_info" in current_analysis:
        info_text.insert("end", "\n🧭 用神分析:\n")
        yongshen = current_analysis["yongshen_info"]
        info_text.insert("end", f"  类型: {yongshen.get('类型', '')}\n")
        info_text.insert("end", f"  代表: {yongshen.get('代表', '')}\n")
        info_text.insert("end", f"  符号: {yongshen.get('符号', '')}\n")
        info_text.insert("end", f"  宫位: {yongshen.get('宫位', '')}\n")
        info_text.insert("end", f"  状态: {yongshen.get('状态', '')}\n")

    # 更新四盘内容
    positions = ["坎", "坤", "震", "巽", "中", "乾", "兑", "艮", "离"]
    pan_types = ["地盘", "天盘", "人盘", "神盘"]
    for pan_type in pan_types:
        text_widget = getattr(pan_tab, f"{pan_type.lower()}_text")
        text_widget.delete("0.0", "end")
        # 标题
        titles = {
            "地盘": "地盘（三奇六仪）：\n\n",
            "天盘": "天盘（九星）：\n\n",
            "人盘": "人盘（八门）：\n\n",
            "神盘": "神盘（八神）：\n\n"
        }
        text_widget.insert("end", titles[pan_type])
        for pos in positions:
            value = pan[pan_type].get(pos, "")
            text_widget.insert("end", f"{pos}宫: {value}\n")