#!/usr/bin/env python3
"""
AC Engine v1.2 — Team Flames / Samsoft / Flames Co.
A fork of Cocos2d & Clickteam Fusion concepts
Clickteam Fusion 3 HUD + Cocos/Unreal Blueprints + Vibe Coding AI
Trilingual: English / Japanese / Chinese Mandarin
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog, colorchooser
import json, math, random, os, time
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  LOCALIZATION — English / 日本語 / 中文
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LANG = {
  "English": {
    "title":"AC Engine v1.2 — Team Flames","file":"File","edit":"Edit",
    "view":"View","run":"Run","project":"Project","insert":"Insert",
    "help":"Help","language":"Language","new":"New Project","open":"Open Project",
    "save":"Save Project","save_as":"Save As...","export":"Export Game",
    "exit":"Exit","undo":"Undo","redo":"Redo","cut":"Cut","copy":"Copy",
    "paste":"Paste","delete":"Delete","select_all":"Select All","preferences":"Preferences",
    "zoom_in":"Zoom In","zoom_out":"Zoom Out","grid":"Toggle Grid","snap":"Toggle Snap",
    "play":"▶ Play","pause":"⏸ Pause","stop":"⏹ Stop","build":"Build",
    "debug":"Debug","settings":"Project Settings","scenes":"Frame Manager",
    "about":"About AC Engine","docs":"Documentation","shortcuts":"Keyboard Shortcuts",
    "tab_scene":"Frame Editor","tab_events":"Event Editor",
    "tab_blueprints":"Blueprints","tab_vibe":"Vibe Coder AI",
    "objects":"Objects","layers":"Layers","scenes_panel":"Frames",
    "properties":"Properties","console":"Console",
    "t_select":"⊹ Select","t_move":"✥ Move","t_rect":"▢ Rect",
    "t_circle":"◯ Circle","t_text":"A Text","t_active":"★ Active",
    "t_backdrop":"▦ Backdrop","t_counter":"# Counter",
    "obj_active":"Active","obj_backdrop":"Backdrop","obj_quick_bg":"Quick Backdrop",
    "obj_counter":"Counter","obj_string":"String","obj_lives":"Lives",
    "obj_score":"Score","obj_player":"Player","obj_timer":"Timer",
    "add_event":"+ New Event","add_cond":"+ Condition","add_action":"+ Action",
    "event_grp":"Event Group",
    "evt_always":"Always","evt_start":"Start of Frame","evt_end":"End of Frame",
    "evt_timer":"Timer","evt_collision":"Collision","evt_keyboard":"Keyboard",
    "evt_mouse":"Mouse Click","evt_animation":"Animation End",
    "act_move":"Set Position","act_speed":"Set Speed","act_dir":"Set Direction",
    "act_destroy":"Destroy","act_create":"Create Object","act_anim":"Set Animation",
    "act_visible":"Set Visibility","act_var":"Set Variable","act_sound":"Play Sound",
    "act_score":"Add to Score","act_lives":"Set Lives","act_next":"Next Frame",
    "act_restart":"Restart Frame","act_jump":"Jump to Frame",
    "bp_add":"+ Add Node","bp_connect":"Link","bp_clear":"Clear All",
    "bp_event":"Events","bp_flow":"Flow Control","bp_math":"Math",
    "bp_physics":"Physics","bp_audio":"Audio",
    "bp_on_start":"On Start","bp_on_tick":"On Tick","bp_on_collide":"On Collision",
    "bp_branch":"Branch","bp_sequence":"Sequence","bp_for_each":"For Each",
    "bp_delay":"Delay","bp_move":"Move To","bp_force":"Apply Force",
    "bp_velocity":"Set Velocity","bp_gravity":"Set Gravity",
    "bp_play_sfx":"Play SFX","bp_play_bgm":"Play BGM",
    "bp_add_num":"Add","bp_multiply":"Multiply","bp_clamp":"Clamp",
    "bp_random":"Random","bp_lerp":"Lerp",
    "vibe_prompt":"Describe your game idea and I'll generate it...",
    "vibe_go":"✦ Generate","vibe_apply":"Apply to Scene","vibe_clear":"Clear",
    "vibe_templates":"Templates","vibe_platformer":"Platformer",
    "vibe_shooter":"Top-Down Shooter","vibe_puzzle":"Puzzle Game","vibe_rpg":"RPG Starter",
    "p_name":"Name","p_x":"X","p_y":"Y","p_w":"Width","p_h":"Height",
    "p_rot":"Rotation","p_color":"Color","p_visible":"Visible","p_solid":"Solid",
    "p_layer":"Layer","p_tag":"Tag","p_speed":"Speed","p_dir":"Direction",
    "ready":"Ready","saved":"Saved","running":"Running...",
    "obj_count":"Objects: {}","frame":"Frame 1","fps_target":"60 FPS","res":"640×480",
  },
  "日本語": {
    "title":"AC Engine v1.2 — チームフレームス","file":"ファイル","edit":"編集",
    "view":"表示","run":"実行","project":"プロジェクト","insert":"挿入",
    "help":"ヘルプ","language":"言語","new":"新規プロジェクト","open":"プロジェクトを開く",
    "save":"プロジェクト保存","save_as":"名前を付けて保存...","export":"ゲームをエクスポート",
    "exit":"終了","undo":"元に戻す","redo":"やり直し","cut":"切り取り","copy":"コピー",
    "paste":"貼り付け","delete":"削除","select_all":"すべて選択","preferences":"設定",
    "zoom_in":"ズームイン","zoom_out":"ズームアウト","grid":"グリッド切替","snap":"スナップ切替",
    "play":"▶ 再生","pause":"⏸ 一時停止","stop":"⏹ 停止","build":"ビルド",
    "debug":"デバッグ","settings":"プロジェクト設定","scenes":"フレーム管理",
    "about":"AC Engineについて","docs":"ドキュメント","shortcuts":"キーボードショートカット",
    "tab_scene":"フレームエディタ","tab_events":"イベントエディタ",
    "tab_blueprints":"ブループリント","tab_vibe":"バイブコーダーAI",
    "objects":"オブジェクト","layers":"レイヤー","scenes_panel":"フレーム",
    "properties":"プロパティ","console":"コンソール",
    "t_select":"⊹ 選択","t_move":"✥ 移動","t_rect":"▢ 四角",
    "t_circle":"◯ 円","t_text":"A テキスト","t_active":"★ アクティブ",
    "t_backdrop":"▦ 背景","t_counter":"# カウンタ",
    "obj_active":"アクティブオブジェクト","obj_backdrop":"背景","obj_quick_bg":"クイック背景",
    "obj_counter":"カウンタ","obj_string":"文字列オブジェクト","obj_lives":"ライフ",
    "obj_score":"スコア","obj_player":"プレイヤー","obj_timer":"タイマー",
    "add_event":"+ 新規イベント","add_cond":"+ 条件","add_action":"+ アクション",
    "event_grp":"イベントグループ",
    "evt_always":"常時","evt_start":"フレーム開始","evt_end":"フレーム終了",
    "evt_timer":"タイマー","evt_collision":"衝突","evt_keyboard":"キーボード",
    "evt_mouse":"マウスクリック","evt_animation":"アニメーション終了",
    "act_move":"位置設定","act_speed":"速度設定","act_dir":"方向設定",
    "act_destroy":"破棄","act_create":"オブジェクト生成","act_anim":"アニメーション設定",
    "act_visible":"表示設定","act_var":"変数設定","act_sound":"サウンド再生",
    "act_score":"スコア加算","act_lives":"ライフ設定","act_next":"次のフレーム",
    "act_restart":"フレーム再開","act_jump":"フレームジャンプ",
    "bp_add":"+ ノード追加","bp_connect":"接続","bp_clear":"全クリア",
    "bp_event":"イベント","bp_flow":"フロー制御","bp_math":"数学",
    "bp_physics":"物理","bp_audio":"オーディオ",
    "bp_on_start":"開始時","bp_on_tick":"更新時","bp_on_collide":"衝突時",
    "bp_branch":"分岐","bp_sequence":"シーケンス","bp_for_each":"各要素",
    "bp_delay":"遅延","bp_move":"移動","bp_force":"力を適用",
    "bp_velocity":"速度設定","bp_gravity":"重力設定",
    "bp_play_sfx":"効果音再生","bp_play_bgm":"BGM再生",
    "bp_add_num":"加算","bp_multiply":"乗算","bp_clamp":"クランプ",
    "bp_random":"ランダム","bp_lerp":"線形補間",
    "vibe_prompt":"ゲームのアイデアを説明してください...",
    "vibe_go":"✦ 生成","vibe_apply":"シーンに適用","vibe_clear":"クリア",
    "vibe_templates":"テンプレート","vibe_platformer":"プラットフォーマー",
    "vibe_shooter":"シューター","vibe_puzzle":"パズル","vibe_rpg":"RPG",
    "p_name":"名前","p_x":"X座標","p_y":"Y座標","p_w":"幅","p_h":"高さ",
    "p_rot":"回転","p_color":"色","p_visible":"表示","p_solid":"固体",
    "p_layer":"レイヤー","p_tag":"タグ","p_speed":"速度","p_dir":"方向",
    "ready":"準備完了","saved":"保存完了","running":"実行中...",
    "obj_count":"オブジェクト: {}","frame":"フレーム 1","fps_target":"60 FPS","res":"640×480",
  },
  "中文": {
    "title":"AC Engine v1.2 — 火焰团队","file":"文件","edit":"编辑",
    "view":"视图","run":"运行","project":"项目","insert":"插入",
    "help":"帮助","language":"语言","new":"新建项目","open":"打开项目",
    "save":"保存项目","save_as":"另存为...","export":"导出游戏",
    "exit":"退出","undo":"撤销","redo":"重做","cut":"剪切","copy":"复制",
    "paste":"粘贴","delete":"删除","select_all":"全选","preferences":"偏好设置",
    "zoom_in":"放大","zoom_out":"缩小","grid":"切换网格","snap":"切换吸附",
    "play":"▶ 播放","pause":"⏸ 暂停","stop":"⏹ 停止","build":"构建",
    "debug":"调试","settings":"项目设置","scenes":"帧管理",
    "about":"关于AC Engine","docs":"文档","shortcuts":"快捷键",
    "tab_scene":"帧编辑器","tab_events":"事件编辑器",
    "tab_blueprints":"蓝图","tab_vibe":"氛围编码AI",
    "objects":"对象","layers":"图层","scenes_panel":"帧",
    "properties":"属性","console":"控制台",
    "t_select":"⊹ 选择","t_move":"✥ 移动","t_rect":"▢ 矩形",
    "t_circle":"◯ 圆形","t_text":"A 文本","t_active":"★ 活动",
    "t_backdrop":"▦ 背景","t_counter":"# 计数器",
    "obj_active":"活动对象","obj_backdrop":"背景","obj_quick_bg":"快速背景",
    "obj_counter":"计数器","obj_string":"字符串对象","obj_lives":"生命",
    "obj_score":"分数","obj_player":"玩家","obj_timer":"计时器",
    "add_event":"+ 新事件","add_cond":"+ 条件","add_action":"+ 动作",
    "event_grp":"事件组",
    "evt_always":"始终","evt_start":"帧开始","evt_end":"帧结束",
    "evt_timer":"计时器","evt_collision":"碰撞","evt_keyboard":"键盘",
    "evt_mouse":"鼠标点击","evt_animation":"动画结束",
    "act_move":"设置位置","act_speed":"设置速度","act_dir":"设置方向",
    "act_destroy":"销毁","act_create":"创建对象","act_anim":"设置动画",
    "act_visible":"设置可见性","act_var":"设置变量","act_sound":"播放声音",
    "act_score":"加分","act_lives":"设置生命","act_next":"下一帧",
    "act_restart":"重启帧","act_jump":"跳转到帧",
    "bp_add":"+ 添加节点","bp_connect":"连接","bp_clear":"全部清除",
    "bp_event":"事件","bp_flow":"流程控制","bp_math":"数学",
    "bp_physics":"物理","bp_audio":"音频",
    "bp_on_start":"开始时","bp_on_tick":"每帧更新","bp_on_collide":"碰撞时",
    "bp_branch":"分支","bp_sequence":"シーケンス","bp_for_each":"遍历",
    "bp_delay":"延迟","bp_move":"移动到","bp_force":"施加力",
    "bp_velocity":"设置速度","bp_gravity":"设置重力",
    "bp_play_sfx":"播放音效","bp_play_bgm":"播放背景音乐",
    "bp_add_num":"加法","bp_multiply":"乘法","bp_clamp":"限制范围",
    "bp_random":"随机","bp_lerp":"线性插值",
    "vibe_prompt":"描述你的游戏创意，我会为你生成...",
    "vibe_go":"✦ 生成","vibe_apply":"应用到场景","vibe_clear":"清除",
    "vibe_templates":"模板","vibe_platformer":"平台跳跃",
    "vibe_shooter":"俯视射击","vibe_puzzle":"益智游戏","vibe_rpg":"RPG入门",
    "p_name":"名称","p_x":"X坐标","p_y":"Y坐标","p_w":"宽度","p_h":"高度",
    "p_rot":"旋转","p_color":"颜色","p_visible":"可见","p_solid":"实体",
    "p_layer":"图层","p_tag":"标签","p_speed":"速度","p_dir":"方向",
    "ready":"就绪","saved":"已保存","running":"运行中...",
    "obj_count":"对象: {}","frame":"帧 1","fps_target":"60 FPS","res":"640×480",
  },
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CLICKTEAM FUSION 3 DARK THEME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
T = {
    "menu_bg":"#2B2B3D","menu_fg":"#4488FF", # Dark Blue text
    "toolbar_bg":"#333348",
    "toolbar_fg":"#4488FF", # Dark Blue button labels
    "toolbar_active":"#5A5AFF","panel_bg":"#1E1E2E",
    "panel_fg":"#4488FF", # Dark Blue panel text
    "panel_header":"#2A2A40","panel_border":"#404060",
    "scene_bg":"#151530", # UPDATED: Dark Blue background
    "scene_grid":"#252550", # UPDATED: Lighter Blue grid
    "tab_bg":"#252540",
    "tab_active":"#3A3A60","tab_fg":"#4488FF", # Dark Blue tab text
    "tab_active_fg":"#FFFFFF",
    "event_row1":"#1E1E30","event_row2":"#252540","event_cond":"#3366AA",
    "event_action":"#44AA44","event_header":"#1A1A2E",
    "bp_bg":"#1A1A2E","bp_grid":"#222240",
    "bp_node_event":"#CC6633","bp_node_flow":"#3366CC",
    "bp_node_math":"#33AA66","bp_node_phys":"#9944CC","bp_node_audio":"#CC9933",
    "bp_wire":"#66AAFF","bp_wire_exec":"#FF4444",
    "bp_node_title":"#FFFFFF","bp_node_body":"#2A2A44",
    "vibe_bg":"#1A1A2E","vibe_input":"#252540",
    "accent":"#5A5AFF","accent2":"#FF6644",
    "status_bg":"#1A1A28","status_fg":"#4488FF", # Dark Blue status text
    "prop_entry":"#2A2A44","selection":"#FFAA33",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DATA MODELS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class GameObject:
    _id = 0
    def __init__(self, name="Obj", obj_type="active", x=100, y=100,
                 w=32, h=32, color="#44CC44", layer=0):
        GameObject._id += 1
        self.id = GameObject._id
        self.name = name; self.obj_type = obj_type
        self.x = x; self.y = y; self.w = w; self.h = h
        self.color = color; self.rotation = 0; self.visible = True
        self.solid = True; self.layer = layer; self.tag = ""
        self.speed = 0; self.direction = 0; self.canvas_id = None

    def to_dict(self):
        return {k:v for k,v in self.__dict__.items() if k != "canvas_id"}

    @staticmethod
    def from_dict(d):
        o = GameObject(); [setattr(o, k, v) for k, v in d.items() if k != "canvas_id"]; return o

class GameEvent:
    _id = 0
    def __init__(self, conditions=None, actions=None, comment=""):
        GameEvent._id += 1
        self.id = GameEvent._id
        self.conditions = conditions or []; self.actions = actions or []
        self.comment = comment

class BPNode:
    _id = 0
    def __init__(self, title="Node", category="event", x=100, y=100,
                 inputs=None, outputs=None):
        BPNode._id += 1
        self.id = BPNode._id; self.title = title; self.category = category
        self.x = x; self.y = y; self.w = 160
        self.inputs = inputs or []; self.outputs = outputs or []
        self.h = max(80, 32 + max(len(self.inputs), len(self.outputs)) * 18)

class BPConnection:
    def __init__(self, from_id, to_id):
        self.from_id = from_id; self.to_id = to_id

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  AC ENGINE — MAIN APPLICATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class ACEngine:
    def __init__(self, root):
        self.root = root
        self.lang = "English"
        self.L = LANG[self.lang]
        self.root.title(self.L["title"])
        self.root.geometry("600x400")
        self.root.minsize(600, 400)
        self.root.configure(bg=T["menu_bg"])

        # State
        self.project_name = "Untitled"
        self.project_path = None
        self.modified = False
        self.objects = []
        self.events = []
        self.bp_nodes = []
        self.bp_conns = []
        self.scenes = ["Frame 1"]
        self.layers = ["Layer 0", "Layer 1", "Layer 2"]
        self.selected = None
        self.tool = "select"
        self.grid_on = True
        self.snap_on = True
        self.grid_sz = 16
        self.zoom = 1.0
        self.offset = [0, 0]
        self.dragging = False
        self.drag_d = {}
        self.bp_sel = None
        self.bp_drag = False
        self.vibe_result = None

        self._build_ui()
        self._defaults()
        self._log("AC Engine v1.2 initialized — Team Flames / Samsoft")

    def t(self, k): return self.L.get(k, k)

    # ─── FULL UI BUILD ───
    def _build_ui(self):
        self._menubar()
        self._toolbar()
        self._main()
        self._statusbar()
        self._shortcuts()

    # ─── MENUBAR ───
    def _menubar(self):
        self.mb = tk.Menu(self.root, bg=T["menu_bg"], fg=T["menu_fg"],
                          activebackground=T["accent"], activeforeground="#FFF", bd=0)
        self.root.config(menu=self.mb)
        self._build_menus()

    def _build_menus(self):
        self.mb.delete(0, "end")
        def M(): return tk.Menu(self.mb, tearoff=0, bg=T["menu_bg"], fg=T["menu_fg"],
                                activebackground=T["accent"])
        # File
        m = M()
        m.add_command(label=self.t("new"), command=self.new_proj, accelerator="Ctrl+N")
        m.add_command(label=self.t("open"), command=self.open_proj, accelerator="Ctrl+O")
        m.add_separator()
        m.add_command(label=self.t("save"), command=self.save_proj, accelerator="Ctrl+S")
        m.add_command(label=self.t("save_as"), command=self.save_as)
        m.add_separator()
        m.add_command(label=self.t("export"), command=self.export_game)
        m.add_separator()
        m.add_command(label=self.t("exit"), command=self.on_exit)
        self.mb.add_cascade(label=self.t("file"), menu=m)
        # Edit
        m = M()
        for k in ["undo","redo"]: m.add_command(label=self.t(k))
        m.add_separator()
        for k in ["cut","copy","paste"]: m.add_command(label=self.t(k))
        m.add_command(label=self.t("delete"), command=self.del_sel)
        self.mb.add_cascade(label=self.t("edit"), menu=m)
        # View
        m = M()
        m.add_command(label=self.t("zoom_in"), command=lambda: self._do_zoom(1.2))
        m.add_command(label=self.t("zoom_out"), command=lambda: self._do_zoom(0.8))
        m.add_separator()
        m.add_command(label=self.t("grid"), command=self.tog_grid)
        m.add_command(label=self.t("snap"), command=self.tog_snap)
        self.mb.add_cascade(label=self.t("view"), menu=m)
        # Insert (Clickteam style)
        m = M()
        objs = [("obj_active","active","#44CC44"),("obj_backdrop","backdrop","#444466"),
                ("obj_quick_bg","quick_bg","#336"),("obj_counter","counter","#CCCC44"),
                ("obj_string","string","#FFF"),("obj_lives","lives","#FF6666"),
                ("obj_score","score","#FFCC00"),("obj_player","player","#44CC44"),
                ("obj_timer","timer","#66CCFF")]
        for lk, ot, co in objs:
            m.add_command(label=self.t(lk), command=lambda t=ot,c=co,n=lk: self._ins_obj(t,c,n))
        self.mb.add_cascade(label=self.t("insert"), menu=m)
        # Run
        m = M()
        m.add_command(label=self.t("play"), command=self.run_play)
        m.add_command(label=self.t("pause"), command=self.run_pause)
        m.add_command(label=self.t("stop"), command=self.run_stop)
        m.add_separator()
        m.add_command(label=self.t("build"), command=self.build_game)
        self.mb.add_cascade(label=self.t("run"), menu=m)
        # Project
        m = M()
        m.add_command(label=self.t("settings"), command=self.proj_settings)
        self.mb.add_cascade(label=self.t("project"), menu=m)
        # Language
        m = M()
        for lang in LANG: m.add_command(label=lang, command=lambda l=lang: self.set_lang(l))
        self.mb.add_cascade(label=self.t("language"), menu=m)
        # Help
        m = M()
        m.add_command(label=self.t("about"), command=self.about)
        self.mb.add_cascade(label=self.t("help"), menu=m)

    # ─── TOOLBAR ───
    def _toolbar(self):
        self.tb = tk.Frame(self.root, bg=T["toolbar_bg"], height=36)
        self.tb.pack(fill="x"); self.tb.pack_propagate(False)
        self._build_tb()

    def _build_tb(self):
        for w in self.tb.winfo_children(): w.destroy()
        tools = [("t_select","select"),("t_move","move"),("t_rect","rect"),
                 ("t_circle","circle"),("t_text","text"),("t_active","active"),
                 ("t_backdrop","backdrop"),("t_counter","counter")]
        for lk, tid in tools:
            tk.Button(self.tb, text=self.t(lk), font=("Segoe UI",8),
                      bg=T["toolbar_bg"], fg=T["toolbar_fg"], activebackground=T["toolbar_active"],
                      relief="flat", bd=0, padx=5, command=lambda t=tid: self._set_tool(t)
                      ).pack(side="left", padx=1, pady=2)
        tk.Frame(self.tb, width=2, bg=T["panel_border"]).pack(side="left", fill="y", padx=6, pady=4)
        for lk, cmd, fg in [("play",self.run_play,"#44FF44"),("pause",self.run_pause,T["toolbar_fg"]),
                             ("stop",self.run_stop,T["toolbar_fg"])]:
            tk.Button(self.tb, text=self.t(lk), font=("Segoe UI",9,"bold"),
                      bg=T["toolbar_bg"], fg=fg, activebackground=T["accent"],
                      relief="flat", bd=0, padx=6, command=cmd).pack(side="left", padx=2, pady=2)
        self.zoom_lbl = tk.Label(self.tb, text=f"🔍 {int(self.zoom*100)}%",
                                  font=("Segoe UI",8), bg=T["toolbar_bg"], fg=T["toolbar_fg"])
        self.zoom_lbl.pack(side="right", padx=8)

    # ─── MAIN AREA ───
    def _main(self):
        self.mf = tk.Frame(self.root, bg=T["panel_bg"])
        self.mf.pack(fill="both", expand=True)
        # Left panel
        self.lp = tk.Frame(self.mf, bg=T["panel_bg"], width=190)
        self.lp.pack(side="left", fill="y"); self.lp.pack_propagate(False)
        self._left_panel()
        tk.Frame(self.mf, width=1, bg=T["panel_border"]).pack(side="left", fill="y")
        # Right panel
        self.rp = tk.Frame(self.mf, bg=T["panel_bg"], width=210)
        self.rp.pack(side="right", fill="y"); self.rp.pack_propagate(False)
        self._right_panel()
        tk.Frame(self.mf, width=1, bg=T["panel_border"]).pack(side="right", fill="y")
        # Center
        self.cf = tk.Frame(self.mf, bg=T["scene_bg"])
        self.cf.pack(side="left", fill="both", expand=True)
        self._tabs()

    # ─── LEFT PANEL ───
    def _left_panel(self):
        for w in self.lp.winfo_children(): w.destroy()
        nb = ttk.Notebook(self.lp); nb.pack(fill="both", expand=True)
        # Objects
        of = tk.Frame(nb, bg=T["panel_bg"]); nb.add(of, text=f" {self.t('objects')} ")
        self.obj_lb = tk.Listbox(of, bg=T["panel_bg"], fg=T["panel_fg"],
                                  selectbackground=T["accent"], selectforeground="#FFF",
                                  relief="flat", font=("Consolas",9), activestyle="none")
        self.obj_lb.pack(fill="both", expand=True, padx=2, pady=2)
        self.obj_lb.bind("<<ListboxSelect>>", self._on_sel)
        bf = tk.Frame(of, bg=T["panel_bg"]); bf.pack(fill="x")
        # UPDATED: Blue Text + and - Buttons (Flat style) as requested
        tk.Button(bf, text="+", bg=T["panel_bg"], fg="#4488FF", relief="flat", width=3, font=("Segoe UI",9,"bold"),
                  activebackground=T["accent"], activeforeground="#FFF",
                  command=lambda: self._ins_obj("active","#44CC44","obj_active")).pack(side="left", padx=2, pady=2)
        tk.Button(bf, text="−", bg=T["panel_bg"], fg="#4488FF", relief="flat", width=3, font=("Segoe UI",9,"bold"),
                  activebackground="#663333", activeforeground="#FFF",
                  command=self.del_sel).pack(side="left", padx=2, pady=2)
        # Layers
        lf = tk.Frame(nb, bg=T["panel_bg"]); nb.add(lf, text=f" {self.t('layers')} ")
        lb = tk.Listbox(lf, bg=T["panel_bg"], fg=T["panel_fg"], selectbackground=T["accent"],
                        font=("Consolas",9), relief="flat", activestyle="none")
        lb.pack(fill="both", expand=True, padx=2, pady=2)
        for l in self.layers: lb.insert("end", f"  {l}")
        # Scenes (Frames)
        sf = tk.Frame(nb, bg=T["panel_bg"]); nb.add(sf, text=f" {self.t('scenes_panel')} ")
        sb = tk.Listbox(sf, bg=T["panel_bg"], fg=T["panel_fg"], selectbackground=T["accent"],
                        font=("Consolas",9), relief="flat", activestyle="none")
        sb.pack(fill="both", expand=True, padx=2, pady=2)
        for s in self.scenes: sb.insert("end", f"  🎬 {s}")

    # ─── RIGHT PANEL (Properties) ───
    def _right_panel(self):
        for w in self.rp.winfo_children(): w.destroy()
        # UPDATED: Label color to Dark Blue
        tk.Label(self.rp, text=f"  {self.t('properties')}", font=("Segoe UI",10,"bold"),
                 bg=T["panel_header"], fg="#4488FF", anchor="w").pack(fill="x", ipady=4)
        pc = tk.Canvas(self.rp, bg=T["panel_bg"], highlightthickness=0)
        sb = tk.Scrollbar(self.rp, orient="vertical", command=pc.yview)
        self.pi = tk.Frame(pc, bg=T["panel_bg"])
        self.pi.bind("<Configure>", lambda e: pc.configure(scrollregion=pc.bbox("all")))
        pc.create_window((0,0), window=self.pi, anchor="nw")
        pc.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y"); pc.pack(fill="both", expand=True)
        self._upd_props()

    def _upd_props(self):
        for w in self.pi.winfo_children(): w.destroy()
        o = self.selected
        if not o:
            tk.Label(self.pi, text="No selection", bg=T["panel_bg"], fg="#666688",
                     font=("Segoe UI",9,"italic")).pack(pady=20)
            return
        props = [("p_name","name","s"),("p_x","x","i"),("p_y","y","i"),("p_w","w","i"),
                 ("p_h","h","i"),("p_rot","rotation","i"),("p_color","color","c"),
                 ("p_visible","visible","b"),("p_solid","solid","b"),("p_layer","layer","i"),
                 ("p_tag","tag","s"),("p_speed","speed","i"),("p_dir","direction","i")]
        for lk, attr, dt in props:
            r = tk.Frame(self.pi, bg=T["panel_bg"]); r.pack(fill="x", padx=4, pady=1)
            tk.Label(r, text=self.t(lk), font=("Segoe UI",8), bg=T["panel_bg"],
                     fg=T["panel_fg"], width=10, anchor="w").pack(side="left")
            v = getattr(o, attr)
            if dt == "b":
                var = tk.BooleanVar(value=v)
                tk.Checkbutton(r, variable=var, bg=T["panel_bg"], fg=T["panel_fg"],
                               selectcolor=T["prop_entry"], activebackground=T["panel_bg"],
                               command=lambda a=attr, vr=var: self._sp(a, vr.get())).pack(side="left")
            elif dt == "c":
                tk.Button(r, text=f" {v} ", bg=v, fg="#FFF", font=("Consolas",8), relief="flat",
                          command=lambda a=attr: self._pick_col(a)).pack(side="left", fill="x", expand=True)
            else:
                e = tk.Entry(r, bg=T["prop_entry"], fg=T["panel_fg"], insertbackground=T["panel_fg"],
                             relief="flat", font=("Consolas",9))
                e.insert(0, str(v)); e.pack(side="left", fill="x", expand=True)
                e.bind("<Return>", lambda ev,a=attr,en=e,d=dt: self._ap(a,en,d))
                e.bind("<FocusOut>", lambda ev,a=attr,en=e,d=dt: self._ap(a,en,d))

    def _sp(self, a, v):
        if self.selected: setattr(self.selected, a, v); self._redraw(); self.modified = True

    def _ap(self, a, e, d):
        if not self.selected: return
        try:
            v = e.get(); v = int(float(v)) if d == "i" else v
            setattr(self.selected, a, v); self._redraw(); self._ref_list(); self.modified = True
        except: pass

    def _pick_col(self, a):
        if not self.selected: return
        c = colorchooser.askcolor(initialcolor=getattr(self.selected, a))
        if c[1]: setattr(self.selected, a, c[1]); self._upd_props(); self._redraw()

    # ─── CENTER TABS ───
    def _tabs(self):
        for w in self.cf.winfo_children(): w.destroy()
        self.tbar = tk.Frame(self.cf, bg=T["tab_bg"], height=28)
        self.tbar.pack(fill="x"); self.tbar.pack_propagate(False)
        self.tframes = {}; self.tbtns = {}; self.ctab = "scene"
        for tid, lk in [("scene","tab_scene"),("events","tab_events"),
                        ("blueprints","tab_blueprints"),("vibe","tab_vibe")]:
            b = tk.Button(self.tbar, text=f" {self.t(lk)} ", font=("Segoe UI",9),
                          bg=T["tab_bg"], fg=T["tab_fg"], relief="flat", bd=0,
                          activebackground=T["tab_active"],
                          command=lambda t=tid: self._stab(t))
            b.pack(side="left", padx=1, pady=2); self.tbtns[tid] = b
        self.tc = tk.Frame(self.cf, bg=T["scene_bg"]); self.tc.pack(fill="both", expand=True)
        self._scene_tab(); self._events_tab(); self._bp_tab(); self._vibe_tab()
        self._stab("scene")

    def _stab(self, tid):
        self.ctab = tid
        for k, b in self.tbtns.items():
            b.config(bg=T["tab_active"] if k==tid else T["tab_bg"],
                     fg=T["tab_active_fg"] if k==tid else T["tab_fg"])
        for k, f in self.tframes.items():
            f.pack(fill="both", expand=True) if k==tid else f.pack_forget()

    # ─── SCENE TAB ───
    def _scene_tab(self):
        f = tk.Frame(self.tc, bg=T["scene_bg"]); self.tframes["scene"] = f
        pw = tk.PanedWindow(f, orient="vertical", bg=T["panel_border"], sashwidth=3)
        pw.pack(fill="both", expand=True)
        cf = tk.Frame(pw, bg=T["scene_bg"])
        self.sc = tk.Canvas(cf, bg=T["scene_bg"], highlightthickness=0, cursor="crosshair")
        self.sc.pack(fill="both", expand=True); pw.add(cf, minsize=200)
        self.sc.bind("<Button-1>", self._sc_click)
        self.sc.bind("<B1-Motion>", self._sc_drag)
        self.sc.bind("<ButtonRelease-1>", self._sc_rel)
        self.sc.bind("<Button-3>", self._sc_rclick)
        self.sc.bind("<MouseWheel>", self._sc_scroll)
        self.sc.bind("<Configure>", lambda e: self._redraw())
        # Console
        cof = tk.Frame(pw, bg=T["panel_bg"])
        # UPDATED: Label color to Dark Blue
        tk.Label(cof, text=f"  {self.t('console')}", font=("Segoe UI",8,"bold"),
                 bg=T["panel_header"], fg="#4488FF", anchor="w").pack(fill="x")
        self.con = tk.Text(cof, bg=T["panel_bg"], fg="#88AA88", font=("Consolas",8),
                           height=4, relief="flat", insertbackground="#88AA88", state="disabled")
        self.con.pack(fill="both", expand=True); pw.add(cof, minsize=50)

    def _log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        if hasattr(self, "con"):
            self.con.config(state="normal")
            self.con.insert("end", f"[{ts}] {msg}\n")
            self.con.see("end"); self.con.config(state="disabled")

    def _redraw(self):
        c = self.sc
        # Enforce background color on the widget itself
        c.configure(bg=T["scene_bg"])
        c.delete("all")
        
        cw, ch = c.winfo_width() or 640, c.winfo_height() or 480
        
        # Draw a massive background rectangle to ensure coverage even during resize
        # Using -10 to cw+10 prevents any white borders
        c.create_rectangle(-10, -10, cw+20, ch+20, fill=T["scene_bg"], outline="")
        
        # Grid
        if self.grid_on:
            gs = int(self.grid_sz * self.zoom)
            if gs > 2:
                for x in range(0, cw, gs): c.create_line(x,0,x,ch, fill=T["scene_grid"])
                for y in range(0, ch, gs): c.create_line(0,y,cw,y, fill=T["scene_grid"])
        # Playfield
        pw, ph = int(640*self.zoom), int(480*self.zoom)
        ox, oy = self.offset
        c.create_rectangle(ox,oy,ox+pw,oy+ph, outline=T["accent"], width=2, dash=(4,4))
        # UPDATED: Changed label text color to match #4488FF
        c.create_text(ox+pw//2, oy-10, text="640 × 480", fill="#4488FF", font=("Consolas",8))
        # Objects
        icons = {"player":"P","active":"★","backdrop":"▦","counter":"#","string":"A",
                 "lives":"♥","score":"$","timer":"⏱","quick_bg":"▤","circle":"◯","rect":"▢"}
        for obj in sorted(self.objects, key=lambda o: o.layer):
            if not obj.visible: continue
            x = int(obj.x*self.zoom)+ox; y = int(obj.y*self.zoom)+oy
            w = int(obj.w*self.zoom); h = int(obj.h*self.zoom)
            if obj.obj_type == "circle":
                obj.canvas_id = c.create_oval(x,y,x+w,y+h, fill=obj.color, outline="#FFF")
            else:
                obj.canvas_id = c.create_rectangle(x,y,x+w,y+h, fill=obj.color, outline="#FFF")
            c.create_text(x+w//2, y+h//2, text=obj.name[:8], fill="#FFF",
                          font=("Consolas",max(7,int(8*self.zoom))))
            c.create_text(x+3, y+3, text=icons.get(obj.obj_type,"•"), fill="#FFF",
                          font=("Consolas",7), anchor="nw")
            if obj == self.selected:
                c.create_rectangle(x-2,y-2,x+w+2,y+h+2, outline=T["selection"], width=2, dash=(3,3))
                for hx,hy in [(x-3,y-3),(x+w,y-3),(x-3,y+h),(x+w,y+h)]:
                    c.create_rectangle(hx,hy,hx+6,hy+6, fill=T["selection"], outline="#FFF")

    def _sc_click(self, e):
        if self.tool == "select": self._sel_at(e.x, e.y)
        elif self.tool in ("rect","active","backdrop","counter","circle"):
            self._place(e.x, e.y)

    def _sel_at(self, mx, my):
        ox, oy = self.offset; found = None
        for obj in reversed(self.objects):
            x = int(obj.x*self.zoom)+ox; y = int(obj.y*self.zoom)+oy
            w = int(obj.w*self.zoom); h = int(obj.h*self.zoom)
            if x<=mx<=x+w and y<=my<=y+h: found = obj; break
        self.selected = found; self._upd_props(); self._hl_list(); self._redraw()
        if found:
            self.dragging = True
            self.drag_d = {"ox":found.x,"oy":found.y,"mx":mx,"my":my}

    def _sc_drag(self, e):
        if self.dragging and self.selected:
            dx = (e.x-self.drag_d["mx"])/self.zoom; dy = (e.y-self.drag_d["my"])/self.zoom
            nx, ny = self.drag_d["ox"]+dx, self.drag_d["oy"]+dy
            if self.snap_on:
                nx = round(nx/self.grid_sz)*self.grid_sz
                ny = round(ny/self.grid_sz)*self.grid_sz
            self.selected.x, self.selected.y = int(nx), int(ny)
            self._redraw(); self._upd_props(); self.modified = True

    def _sc_rel(self, e): self.dragging = False

    def _sc_rclick(self, e):
        m = tk.Menu(self.root, tearoff=0, bg=T["menu_bg"], fg=T["menu_fg"],
                    activebackground=T["accent"])
        for lk, ot, co in [("obj_active","active","#44CC44"),("obj_player","player","#44CC44"),
                            ("obj_backdrop","backdrop","#444466"),("obj_counter","counter","#CCCC44")]:
            m.add_command(label=f"Insert {self.t(lk)}",
                          command=lambda t=ot,c=co,n=lk,x=e.x,y=e.y: self._place_at(t,c,n,x,y))
        if self.selected:
            m.add_separator()
            m.add_command(label=self.t("delete"), command=self.del_sel)
            m.add_command(label=self.t("copy"), command=self._copy)
        m.tk_popup(e.x_root, e.y_root)

    def _sc_scroll(self, e): self._do_zoom(1.1 if e.delta > 0 else 0.9)

    def _place(self, mx, my):
        ox, oy = self.offset
        x, y = (mx-ox)/self.zoom, (my-oy)/self.zoom
        if self.snap_on: x = round(x/self.grid_sz)*self.grid_sz; y = round(y/self.grid_sz)*self.grid_sz
        ot = self.tool if self.tool in ("active","backdrop","counter") else self.tool
        colors = {"active":"#44CC44","backdrop":"#444466","counter":"#CCCC44","circle":"#CC44CC","rect":"#4488CC"}
        name = f"{ot.title()}_{len(self.objects)+1}"
        obj = GameObject(name, ot, int(x), int(y), 32, 32, colors.get(ot,"#4488CC"))
        self.objects.append(obj); self.selected = obj
        self._ref_list(); self._upd_props(); self._redraw()
        self._log(f"Created {name} at ({int(x)},{int(y)})"); self.modified = True

    def _place_at(self, ot, co, lk, mx, my):
        ox, oy = self.offset
        x, y = (mx-ox)/self.zoom, (my-oy)/self.zoom
        name = f"{self.t(lk)}_{len(self.objects)+1}"
        obj = GameObject(name, ot, int(x), int(y), 32, 32, co)
        self.objects.append(obj); self.selected = obj
        self._ref_list(); self._upd_props(); self._redraw()
        self._log(f"Inserted {name}"); self.modified = True

    def _ins_obj(self, ot, co, lk):
        name = f"{self.t(lk)}_{len(self.objects)+1}"
        obj = GameObject(name, ot, random.randint(50,400), random.randint(50,300), 32, 32, co)
        self.objects.append(obj); self.selected = obj
        self._ref_list(); self._upd_props(); self._redraw()
        self._log(f"Inserted {name}"); self.modified = True

    # ─── EVENT EDITOR TAB ───
    def _events_tab(self):
        f = tk.Frame(self.tc, bg=T["event_header"]); self.tframes["events"] = f
        tb = tk.Frame(f, bg=T["toolbar_bg"], height=32); tb.pack(fill="x"); tb.pack_propagate(False)
        for lk, cmd in [("add_event",self._add_evt),("add_cond",self._add_cond),
                        ("add_action",self._add_act),("event_grp",self._add_grp)]:
            tk.Button(tb, text=self.t(lk), font=("Segoe UI",8), bg=T["toolbar_bg"],
                      fg=T["toolbar_fg"], activebackground=T["accent"], relief="flat", padx=6,
                      command=cmd).pack(side="left", padx=2, pady=4)
        # Headers
        hf = tk.Frame(f, bg=T["event_header"], height=24); hf.pack(fill="x"); hf.pack_propagate(False)
        tk.Label(hf, text="  #", width=4, bg=T["event_header"], fg="#888", font=("Consolas",8)).pack(side="left")
        tk.Label(hf, text="Conditions", width=28, bg=T["event_cond"], fg="#FFF",
                 font=("Segoe UI",8,"bold")).pack(side="left", padx=1)
        tk.Label(hf, text="Actions", bg=T["event_action"], fg="#FFF",
                 font=("Segoe UI",8,"bold")).pack(side="left", fill="x", expand=True, padx=1)
        # Event rows
        ef = tk.Frame(f, bg=T["event_row1"]); ef.pack(fill="both", expand=True)
        ec = tk.Canvas(ef, bg=T["event_row1"], highlightthickness=0)
        esb = tk.Scrollbar(ef, orient="vertical", command=ec.yview)
        self.ei = tk.Frame(ec, bg=T["event_row1"])
        self.ei.bind("<Configure>", lambda e: ec.configure(scrollregion=ec.bbox("all")))
        ec.create_window((0,0), window=self.ei, anchor="nw")
        ec.configure(yscrollcommand=esb.set)
        esb.pack(side="right", fill="y"); ec.pack(fill="both", expand=True)
        self._ref_evts()

    def _ref_evts(self):
        for w in self.ei.winfo_children(): w.destroy()
        if not self.events:
            tk.Label(self.ei, text="  No events — click '+ New Event'", bg=T["event_row1"],
                     fg="#666688", font=("Segoe UI",9,"italic")).pack(pady=20)
            return
        for i, evt in enumerate(self.events):
            bg = T["event_row1"] if i%2==0 else T["event_row2"]
            r = tk.Frame(self.ei, bg=bg); r.pack(fill="x", pady=1)
            tk.Label(r, text=f"  {i+1}", width=4, bg=bg, fg="#888", font=("Consolas",8)).pack(side="left")
            ct = " + ".join(evt.conditions) if evt.conditions else "(empty)"
            tk.Label(r, text=f" {ct}", width=28, bg=bg, fg="#88AAFF", font=("Consolas",8),
                     anchor="w").pack(side="left", padx=1)
            at = " → ".join(evt.actions) if evt.actions else "(none)"
            tk.Label(r, text=f" {at}", bg=bg, fg="#88FF88", font=("Consolas",8),
                     anchor="w").pack(side="left", fill="x", expand=True, padx=1)
            tk.Button(r, text="✕", font=("Segoe UI",7), bg=bg, fg="#CC4444", relief="flat",
                      command=lambda idx=i: self._del_evt(idx)).pack(side="right", padx=4)

    def _add_evt(self):
        self.events.append(GameEvent([self.t("evt_always")],[self.t("act_move")]))
        self._ref_evts(); self._log("Added event")

    def _add_cond(self):
        w = tk.Toplevel(self.root); w.title("Condition"); w.geometry("240x280"); w.configure(bg=T["panel_bg"])
        for c in ["evt_always","evt_start","evt_end","evt_timer","evt_collision",
                   "evt_keyboard","evt_mouse","evt_animation"]:
            tk.Button(w, text=self.t(c), bg=T["event_cond"], fg="#FFF", font=("Segoe UI",9),
                      relief="flat", anchor="w",
                      command=lambda cd=c, win=w: self._pick_cond(cd,win)).pack(fill="x", padx=4, pady=1)

    def _pick_cond(self, c, w):
        if self.events: self.events[-1].conditions.append(self.t(c))
        else: self.events.append(GameEvent([self.t(c)]))
        self._ref_evts(); w.destroy()

    def _add_act(self):
        w = tk.Toplevel(self.root); w.title("Action"); w.geometry("240x320"); w.configure(bg=T["panel_bg"])
        for a in ["act_move","act_speed","act_dir","act_destroy","act_create","act_anim",
                   "act_visible","act_var","act_sound","act_score","act_lives","act_next",
                   "act_restart","act_jump"]:
            tk.Button(w, text=self.t(a), bg=T["event_action"], fg="#FFF", font=("Segoe UI",9),
                      relief="flat", anchor="w",
                      command=lambda ac=a, win=w: self._pick_act(ac,win)).pack(fill="x", padx=4, pady=1)

    def _pick_act(self, a, w):
        if self.events: self.events[-1].actions.append(self.t(a))
        else: self.events.append(GameEvent(actions=[self.t(a)]))
        self._ref_evts(); w.destroy()

    def _add_grp(self):
        self.events.append(GameEvent(comment="── Group ──")); self._ref_evts()

    def _del_evt(self, i):
        if 0 <= i < len(self.events): self.events.pop(i); self._ref_evts()

    # ─── BLUEPRINT TAB (Cocos/Unreal style) ───
    def _bp_tab(self):
        f = tk.Frame(self.tc, bg=T["bp_bg"]); self.tframes["blueprints"] = f
        tb = tk.Frame(f, bg=T["toolbar_bg"], height=32); tb.pack(fill="x"); tb.pack_propagate(False)
        cats = [("bp_event","event",T["bp_node_event"]),("bp_flow","flow",T["bp_node_flow"]),
                ("bp_math","math",T["bp_node_math"]),("bp_physics","physics",T["bp_node_phys"]),
                ("bp_audio","audio",T["bp_node_audio"])]
        for lk, cat, co in cats:
            tk.Button(tb, text=self.t(lk), font=("Segoe UI",8), bg=co, fg="#FFF",
                      relief="flat", padx=6, command=lambda c=cat: self._bp_menu(c)
                      ).pack(side="left", padx=2, pady=4)
        tk.Frame(tb, width=2, bg=T["panel_border"]).pack(side="left", fill="y", padx=4, pady=4)
        tk.Button(tb, text=self.t("bp_clear"), font=("Segoe UI",8), bg="#663333", fg="#FFF",
                  relief="flat", padx=6, command=self._bp_clr).pack(side="left", padx=2, pady=4)
        self.bpc = tk.Canvas(f, bg=T["bp_bg"], highlightthickness=0)
        self.bpc.pack(fill="both", expand=True)
        self.bpc.bind("<Button-1>", self._bp_click)
        self.bpc.bind("<B1-Motion>", self._bp_dmove)
        self.bpc.bind("<ButtonRelease-1>", self._bp_rel)
        self.bpc.bind("<Button-3>", self._bp_rclick)
        self.bpc.bind("<Configure>", lambda e: self._bp_draw())

    def _bp_draw(self):
        c = self.bpc; c.delete("all")
        cw, ch = c.winfo_width() or 600, c.winfo_height() or 400
        for x in range(0,cw,20): c.create_line(x,0,x,ch, fill=T["bp_grid"])
        for y in range(0,ch,20): c.create_line(0,y,cw,y, fill=T["bp_grid"])
        # Connections
        for cn in self.bp_conns:
            fn = next((n for n in self.bp_nodes if n.id==cn.from_id), None)
            tn = next((n for n in self.bp_nodes if n.id==cn.to_id), None)
            if fn and tn:
                x1,y1 = fn.x+fn.w, fn.y+40; x2,y2 = tn.x, tn.y+40
                mx = (x1+x2)/2; co = T["bp_wire_exec"] if fn.category=="exec" else T["bp_wire"]
                c.create_line(x1,y1,mx,y1,mx,y2,x2,y2, fill=co, width=2, smooth=True)
        # Nodes
        cc = {"event":T["bp_node_event"],"flow":T["bp_node_flow"],"math":T["bp_node_math"],
              "physics":T["bp_node_phys"],"audio":T["bp_node_audio"]}
        for n in self.bp_nodes:
            co = cc.get(n.category, "#666")
            c.create_rectangle(n.x,n.y,n.x+n.w,n.y+n.h, fill=T["bp_node_body"], outline=co, width=2)
            c.create_rectangle(n.x,n.y,n.x+n.w,n.y+22, fill=co, outline=co)
            c.create_text(n.x+8,n.y+11, text=n.title, fill="#FFF", font=("Segoe UI",8,"bold"), anchor="w")
            c.create_text(n.x+n.w-6,n.y+11, text=n.category[:3].upper(), fill="#FFF8",
                          font=("Consolas",6), anchor="e")
            for i, inp in enumerate(n.inputs):
                py = n.y+32+i*18
                c.create_oval(n.x-5,py-5,n.x+5,py+5, fill="#FFF", outline=co)
                c.create_text(n.x+12,py, text=inp, fill="#AAC", font=("Consolas",7), anchor="w")
            for i, out in enumerate(n.outputs):
                py = n.y+32+i*18
                c.create_oval(n.x+n.w-5,py-5,n.x+n.w+5,py+5, fill="#FFF", outline=co)
                c.create_text(n.x+n.w-12,py, text=out, fill="#AAC", font=("Consolas",7), anchor="e")
            if n == self.bp_sel:
                c.create_rectangle(n.x-3,n.y-3,n.x+n.w+3,n.y+n.h+3,
                                   outline=T["selection"], width=2, dash=(4,4))

    def _bp_menu(self, cat):
        w = tk.Toplevel(self.root); w.title(f"Add {cat.title()} Node")
        w.geometry("220x280"); w.configure(bg=T["panel_bg"])
        defs = {
            "event":[("bp_on_start",[""],["Exec"]),("bp_on_tick",[""],["Exec","Delta"]),
                     ("bp_on_collide",[""],["Exec","Other"])],
            "flow":[("bp_branch",["Exec","Cond"],["True","False"]),("bp_sequence",["Exec"],["Then0","Then1"]),
                    ("bp_for_each",["Exec","Array"],["Body","Elem"]),("bp_delay",["Exec","Sec"],["Done"])],
            "math":[("bp_add_num",["A","B"],["Sum"]),("bp_multiply",["A","B"],["Product"]),
                    ("bp_clamp",["Val","Min","Max"],["Result"]),("bp_random",["Min","Max"],["Result"]),
                    ("bp_lerp",["A","B","Alpha"],["Result"])],
            "physics":[("bp_move",["Exec","Target","Pos"],["Done"]),("bp_force",["Exec","Obj","F"],["Done"]),
                       ("bp_velocity",["Exec","X","Y"],["Done"]),("bp_gravity",["Exec","Val"],["Done"])],
            "audio":[("bp_play_sfx",["Exec","Sound"],["Done"]),("bp_play_bgm",["Exec","Track"],["Done"])],
        }
        for lk, ins, outs in defs.get(cat, []):
            tk.Button(w, text=self.t(lk), bg=T["panel_header"], fg=T["panel_fg"],
                      font=("Segoe UI",9), relief="flat", anchor="w",
                      command=lambda t=lk,i=ins,o=outs,c=cat,win=w: self._bp_add(t,c,i,o,win)
                      ).pack(fill="x", padx=4, pady=1)

    def _bp_add(self, lk, cat, ins, outs, w):
        n = BPNode(self.t(lk), cat, random.randint(50,400), random.randint(50,300), ins, outs)
        self.bp_nodes.append(n); self._bp_draw(); w.destroy()
        self._log(f"Blueprint: Added '{self.t(lk)}'")

    def _bp_click(self, e):
        found = None
        for n in reversed(self.bp_nodes):
            if n.x<=e.x<=n.x+n.w and n.y<=e.y<=n.y+n.h: found = n; break
        self.bp_sel = found; self._bp_draw()
        if found:
            self.bp_drag = True
            self.drag_d = {"ox":found.x,"oy":found.y,"mx":e.x,"my":e.y}

    def _bp_dmove(self, e):
        if self.bp_drag and self.bp_sel:
            self.bp_sel.x = self.drag_d["ox"]+(e.x-self.drag_d["mx"])
            self.bp_sel.y = self.drag_d["oy"]+(e.y-self.drag_d["my"])
            self._bp_draw()

    def _bp_rel(self, e): self.bp_drag = False

    def _bp_rclick(self, e):
        if len(self.bp_nodes) >= 2:
            n1, n2 = self.bp_nodes[-2], self.bp_nodes[-1]
            self.bp_conns.append(BPConnection(n1.id, n2.id))
            self._bp_draw(); self._log(f"Connected {n1.title} → {n2.title}")

    def _bp_clr(self):
        self.bp_nodes.clear(); self.bp_conns.clear(); self.bp_sel = None
        self._bp_draw(); self._log("Blueprints cleared")

    # ─── VIBE CODER AI TAB ───
    def _vibe_tab(self):
        f = tk.Frame(self.tc, bg=T["vibe_bg"]); self.tframes["vibe"] = f
        tk.Label(f, text="✦ Vibe Coder AI — Agentic Game Generator",
                 font=("Segoe UI",12,"bold"), bg=T["vibe_bg"], fg=T["accent"]).pack(pady=(12,2))
        tk.Label(f, text="Describe your game → AC Engine generates objects, events & blueprints",
                 font=("Segoe UI",8), bg=T["vibe_bg"], fg="#666688").pack()
        # Templates
        tf = tk.Frame(f, bg=T["vibe_bg"]); tf.pack(fill="x", padx=20, pady=8)
        tk.Label(tf, text=self.t("vibe_templates")+":", font=("Segoe UI",8,"bold"),
                 bg=T["vibe_bg"], fg=T["panel_fg"]).pack(side="left")
        tmpls = {
            "vibe_platformer": "Side-scrolling platformer with player, platforms, coins, enemies. Arrow keys + space to jump.",
            "vibe_shooter": "Top-down shooter with player ship, enemy waves, bullets, power-ups. WASD + click.",
            "vibe_puzzle": "Match-3 puzzle with colored gems grid, swap mechanics, score counter, combos.",
            "vibe_rpg": "RPG with player character, NPC dialog, inventory, health bar, turn-based combat.",
        }
        for lk, pt in tmpls.items():
            tk.Button(tf, text=self.t(lk), font=("Segoe UI",8), bg=T["panel_header"],
                      fg=T["panel_fg"], relief="flat", padx=6,
                      command=lambda p=pt: self._vibe_set(p)).pack(side="left", padx=3)
        # Input
        self.vi = tk.Text(f, height=4, bg=T["vibe_input"], fg=T["panel_fg"],
                          font=("Consolas",9), insertbackground=T["panel_fg"],
                          relief="flat", wrap="word")
        self.vi.pack(fill="x", padx=20, pady=4)
        self.vi.insert("1.0", self.t("vibe_prompt"))
        self.vi.bind("<FocusIn>", lambda e: self.vi.delete("1.0","end")
                     if self.vi.get("1.0","end").strip()==self.t("vibe_prompt") else None)
        # Buttons
        bf = tk.Frame(f, bg=T["vibe_bg"]); bf.pack(fill="x", padx=20, pady=4)
        tk.Button(bf, text=self.t("vibe_go"), font=("Segoe UI",10,"bold"), bg=T["accent"],
                  fg="#FFF", relief="flat", padx=16, command=self._vibe_gen).pack(side="left", padx=4)
        tk.Button(bf, text=self.t("vibe_apply"), font=("Segoe UI",9), bg=T["event_action"],
                  fg="#FFF", relief="flat", padx=10, command=self._vibe_apply).pack(side="left", padx=4)
        tk.Button(bf, text=self.t("vibe_clear"), font=("Segoe UI",9), bg=T["panel_header"],
                  fg=T["panel_fg"], relief="flat", padx=10,
                  command=lambda: [self.vi.delete("1.0","end"),
                                   self.vo.config(state="normal"),self.vo.delete("1.0","end"),
                                   self.vo.config(state="disabled")]).pack(side="left", padx=4)
        # Output
        tk.Label(f, text="Generated Scene Blueprint:", font=("Segoe UI",8,"bold"),
                 bg=T["vibe_bg"], fg=T["panel_fg"], anchor="w").pack(fill="x", padx=20, pady=(8,2))
        self.vo = tk.Text(f, bg=T["vibe_input"], fg="#88FF88", font=("Consolas",8),
                          relief="flat", state="disabled", wrap="word")
        self.vo.pack(fill="both", expand=True, padx=20, pady=(0,12))

    def _vibe_set(self, t):
        self.vi.delete("1.0","end"); self.vi.insert("1.0", t)

    def _vibe_gen(self):
        p = self.vi.get("1.0","end").strip()
        if not p or p == self.t("vibe_prompt"): return
        self._log("Vibe Coder: Generating...")
        self.vibe_result = self._gen_scene(p)
        self.vo.config(state="normal"); self.vo.delete("1.0","end")
        self.vo.insert("1.0", json.dumps(self.vibe_result, indent=2))
        self.vo.config(state="disabled")
        self._log(f"Generated {len(self.vibe_result.get('objects',[]))} objects, "
                  f"{len(self.vibe_result.get('events',[]))} events")

    def _gen_scene(self, prompt):
        p = prompt.lower(); objs = []; evts = []; bps = []
        if any(w in p for w in ["player","character","hero","ship"]):
            objs.append({"n":"Player","t":"player","x":200,"y":300,"w":32,"h":32,"c":"#44CC44"})
            evts.append({"c":["Keyboard: Arrow Keys"],"a":["Move Player"]})
            bps.append({"t":"On Start","cat":"event"})
        if any(w in p for w in ["platform","ground","floor","jump"]):
            for i in range(5):
                objs.append({"n":f"Platform_{i+1}","t":"backdrop","x":i*120,
                             "y":380+random.randint(-40,0),"w":100,"h":16,"c":"#666688"})
            evts.append({"c":["Collision: Player ↔ Platform"],"a":["Stop falling"]})
        if any(w in p for w in ["enemy","monster","boss","wave"]):
            for i in range(3):
                objs.append({"n":f"Enemy_{i+1}","t":"active","x":300+i*100,"y":200,
                             "w":24,"h":24,"c":"#CC4444"})
            evts.append({"c":["Timer: Every 2s"],"a":["Move Enemy → Player"]})
            evts.append({"c":["Collision: Player ↔ Enemy"],"a":["−1 Life","Restart"]})
        if any(w in p for w in ["coin","collect","item","gem","power"]):
            for i in range(5):
                objs.append({"n":f"Coin_{i+1}","t":"counter","x":random.randint(50,550),
                             "y":random.randint(50,350),"w":16,"h":16,"c":"#FFCC00"})
            evts.append({"c":["Collision: Player ↔ Coin"],"a":["+100 Score","Destroy Coin"]})
        if any(w in p for w in ["shoot","bullet","fire","gun"]):
            objs.append({"n":"Bullet","t":"active","x":0,"y":0,"w":8,"h":4,"c":"#FFFF44"})
            evts.append({"c":["Mouse Click"],"a":["Spawn Bullet at Player"]})
            evts.append({"c":["Bullet ↔ Enemy"],"a":["Destroy Both","+50 Score"]})
        if any(w in p for w in ["score","hud","lives","health","ui"]):
            objs.append({"n":"Score_HUD","t":"score","x":10,"y":10,"w":80,"h":20,"c":"#FFCC00"})
            objs.append({"n":"Lives_HUD","t":"lives","x":550,"y":10,"w":80,"h":20,"c":"#FF6666"})
        if any(w in p for w in ["grid","gem","match","puzzle","swap"]):
            for r in range(6):
                for col in range(6):
                    colors = ["#FF4444","#44FF44","#4444FF","#FFFF44","#FF44FF"]
                    objs.append({"n":f"Gem_{r}_{col}","t":"active",
                                "x":180+col*40,"y":100+r*40,"w":32,"h":32,
                                "c":random.choice(colors)})
            evts.append({"c":["Mouse Click on Gem"],"a":["Select Gem"]})
            evts.append({"c":["Two Gems Selected + Adjacent"],"a":["Swap Gems","Check Matches"]})
        if any(w in p for w in ["npc","dialog","talk","quest"]):
            objs.append({"n":"NPC","t":"string","x":350,"y":250,"w":32,"h":48,"c":"#66AAFF"})
            evts.append({"c":["Player near NPC + Press E"],"a":["Show Dialog Box"]})
        if any(w in p for w in ["inventory","item","equip","bag"]):
            objs.append({"n":"Inventory_UI","t":"backdrop","x":400,"y":50,"w":200,"h":300,"c":"#2A2A44"})
            evts.append({"c":["Press I"],"a":["Toggle Inventory"]})
        objs.append({"n":"Background","t":"backdrop","x":0,"y":0,"w":640,"h":480,"c":"#1A1A2E"})
        if len(objs) <= 1:
            objs.insert(0, {"n":"Player","t":"player","x":200,"y":200,"w":32,"h":32,"c":"#44CC44"})
        return {"objects": objs, "events": evts, "blueprints": bps}

    def _vibe_apply(self):
        if not self.vibe_result: return
        self.objects.clear(); self.events.clear()
        for od in self.vibe_result.get("objects",[]):
            self.objects.append(GameObject(od["n"],od["t"],od["x"],od["y"],od["w"],od["h"],od["c"]))
        for ed in self.vibe_result.get("events",[]):
            self.events.append(GameEvent(ed["c"],ed["a"]))
        xo = 50
        for bd in self.vibe_result.get("blueprints",[]):
            self.bp_nodes.append(BPNode(bd["t"],bd.get("cat","event"),xo,100,[""],["Exec"]))
            xo += 200
        self._ref_list(); self._ref_evts(); self._redraw(); self._bp_draw()
        self._log(f"Applied {len(self.objects)} objects to scene")
        self.modified = True; self._stab("scene")

    # ─── STATUS BAR ───
    def _statusbar(self):
        self.sb = tk.Frame(self.root, bg=T["status_bg"], height=22)
        self.sb.pack(fill="x", side="bottom"); self.sb.pack_propagate(False)
        self._build_sb()

    def _build_sb(self):
        for w in self.sb.winfo_children(): w.destroy()
        self.slbl = tk.Label(self.sb, text=f"  {self.t('ready')}", font=("Segoe UI",8),
                              bg=T["status_bg"], fg=T["status_fg"])
        self.slbl.pack(side="left", padx=4)
        for txt in reversed([self.t("frame"), self.t("obj_count").format(len(self.objects)),
                             self.t("fps_target"), self.t("res"), f"🔍 {int(self.zoom*100)}%"]):
            tk.Label(self.sb, text=f" {txt} ", font=("Consolas",7),
                     bg=T["status_bg"], fg=T["status_fg"]).pack(side="right")
            tk.Frame(self.sb, width=1, bg=T["panel_border"]).pack(side="right", fill="y", pady=3)

    # ─── HELPERS ───
    def _set_tool(self, t):
        self.tool = t
        cm = {"select":"arrow","move":"fleur","rect":"crosshair","circle":"crosshair",
              "text":"xterm","active":"crosshair","backdrop":"crosshair","counter":"crosshair"}
        self.sc.config(cursor=cm.get(t,"arrow")); self._log(f"Tool: {t}")

    def _do_zoom(self, f):
        self.zoom = max(0.25, min(4.0, self.zoom*f)); self._redraw()
        if hasattr(self,"zoom_lbl"): self.zoom_lbl.config(text=f"🔍 {int(self.zoom*100)}%")
        self._build_sb()

    def tog_grid(self): self.grid_on = not self.grid_on; self._redraw()
    def tog_snap(self): self.snap_on = not self.snap_on

    def _ref_list(self):
        self.obj_lb.delete(0,"end")
        icons = {"player":"P","active":"★","backdrop":"▦","counter":"#","string":"A",
                 "lives":"♥","score":"$","timer":"⏱","quick_bg":"▤","circle":"◯","rect":"▢"}
        for o in self.objects:
            self.obj_lb.insert("end", f"  {icons.get(o.obj_type,'•')} {o.name}")
        self._build_sb()

    def _hl_list(self):
        self.obj_lb.selection_clear(0,"end")
        if self.selected and self.selected in self.objects:
            i = self.objects.index(self.selected)
            self.obj_lb.selection_set(i); self.obj_lb.see(i)

    def _on_sel(self, e):
        s = self.obj_lb.curselection()
        if s and 0<=s[0]<len(self.objects):
            self.selected = self.objects[s[0]]; self._upd_props(); self._redraw()

    def del_sel(self):
        if self.selected and self.selected in self.objects:
            n = self.selected.name; self.objects.remove(self.selected); self.selected = None
            self._ref_list(); self._upd_props(); self._redraw(); self._log(f"Deleted {n}")

    def _copy(self):
        if self.selected:
            o = self.selected
            c = GameObject(f"{o.name}_copy",o.obj_type,o.x+20,o.y+20,o.w,o.h,o.color)
            self.objects.append(c); self.selected = c
            self._ref_list(); self._upd_props(); self._redraw()

    def _defaults(self):
        self.objects = []
        self.events = []
        self.bp_nodes = []
        self.bp_conns = []
        self._ref_list()

    # ─── FILE OPS ───
    def new_proj(self):
        if self.modified and not messagebox.askyesno("AC Engine","Unsaved changes. New project?"): return
        self.objects.clear(); self.events.clear(); self.bp_nodes.clear(); self.bp_conns.clear()
        self.selected = None; self.project_name = "Untitled"; self.project_path = None
        self._defaults(); self._ref_evts(); self._redraw(); self._bp_draw()
        self._upd_props(); self._log("New project"); self.modified = False

    def save_proj(self):
        if not self.project_path: self.save_as(); return
        self._do_save()

    def save_as(self):
        p = filedialog.asksaveasfilename(defaultextension=".acproj",
            filetypes=[("AC Engine Project","*.acproj"),("JSON","*.json")])
        if p: self.project_path = p; self.project_name = os.path.basename(p).replace(".acproj",""); self._do_save()

    def _do_save(self):
        d = {"engine":"AC Engine v1.0","project":self.project_name,
             "objects":[o.to_dict() for o in self.objects],
             "events":[{"c":e.conditions,"a":e.actions} for e in self.events],
             "nodes":[{"id":n.id,"t":n.title,"cat":n.category,"x":n.x,"y":n.y,
                       "in":n.inputs,"out":n.outputs} for n in self.bp_nodes],
             "conns":[{"f":c.from_id,"t":c.to_id} for c in self.bp_conns]}
        with open(self.project_path,"w") as f: json.dump(d, f, indent=2)
        self.modified = False; self._log(f"Saved: {self.project_path}")
        self.slbl.config(text=f"  {self.t('saved')}: {self.project_name}")

    def open_proj(self):
        p = filedialog.askopenfilename(filetypes=[("AC Engine Project","*.acproj"),("JSON","*.json")])
        if not p: return
        try:
            with open(p) as f: d = json.load(f)
            self.objects = [GameObject.from_dict(x) for x in d.get("objects",[])]
            self.events = [GameEvent(e.get("c",[]),e.get("a",[])) for e in d.get("events",[])]
            self.bp_nodes = [BPNode(n["t"],n.get("cat","event"),n["x"],n["y"],
                                    n.get("in",[]),n.get("out",[])) for n in d.get("nodes",[])]
            self.bp_conns = [BPConnection(c["f"],c["t"]) for c in d.get("conns",[])]
            self.project_name = d.get("project","Untitled"); self.project_path = p
            self.selected = None; self.modified = False
            self._ref_list(); self._ref_evts(); self._upd_props(); self._redraw(); self._bp_draw()
            self._log(f"Opened: {self.project_name}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def export_game(self):
        self._log("Exporting game...")
        messagebox.showinfo("AC Engine", f"Game exported!\nObjects: {len(self.objects)}\n"
                           f"Events: {len(self.events)}\nNodes: {len(self.bp_nodes)}")

    def run_play(self): self._log("▶ Running..."); self.slbl.config(text=f"  {self.t('running')}", fg="#44FF44")
    def run_pause(self): self._log("⏸ Paused"); self.slbl.config(text="  ⏸ Paused", fg="#FFAA44")
    def run_stop(self): self._log("⏹ Stopped"); self.slbl.config(text=f"  {self.t('ready')}", fg=T["status_fg"])
    def build_game(self):
        self._log(f"Building... {len(self.objects)} objects, {len(self.events)} events")
        self._log("Build complete!")

    def proj_settings(self):
        w = tk.Toplevel(self.root); w.title("Settings"); w.geometry("300x200"); w.configure(bg=T["panel_bg"])
        tk.Label(w, text="Project Name:", bg=T["panel_bg"], fg=T["panel_fg"]).pack(pady=(12,2))
        e = tk.Entry(w, bg=T["prop_entry"], fg=T["panel_fg"], relief="flat", font=("Consolas",10))
        e.insert(0, self.project_name); e.pack(padx=20, fill="x")
        tk.Label(w, text="Resolution: 640×480", bg=T["panel_bg"], fg="#888").pack(pady=8)
        tk.Button(w, text="OK", bg=T["accent"], fg="#FFF", relief="flat", padx=20,
                  command=lambda: [setattr(self,'project_name',e.get()),w.destroy(),
                                   self._log(f"Renamed: {self.project_name}")]).pack(pady=12)

    def about(self):
        messagebox.showinfo("About AC Engine",
            "AC Engine v1.2\nby Team Flames / Samsoft / Flames Co.\n\n"
            "Clickteam Fusion 3 + Cocos2d inspired\nUnreal-style Visual Blueprints\n"
            "Vibe Coding AI Engine\n\nTrilingual: English / 日本語 / 中文\n\n© 2025 Team Flames")

    def set_lang(self, lang):
        self.lang = lang; self.L = LANG[lang]
        self._build_menus(); self._build_tb(); self._build_sb()
        self._left_panel(); self._right_panel(); self._ref_list()
        self._tabs(); self._defaults() if not self.objects else self._ref_list()
        self._redraw(); self._bp_draw()
        self.root.title(self.L["title"]); self._log(f"Language: {lang}")

    def _shortcuts(self):
        self.root.bind("<Control-n>", lambda e: self.new_proj())
        self.root.bind("<Control-o>", lambda e: self.open_proj())
        self.root.bind("<Control-s>", lambda e: self.save_proj())
        self.root.bind("<Delete>", lambda e: self.del_sel())
        self.root.bind("<F5>", lambda e: self.run_play())
        self.root.bind("<Escape>", lambda e: self.run_stop())
        self.root.bind("<Control-g>", lambda e: self.tog_grid())

    def on_exit(self):
        if self.modified and not messagebox.askyesno("AC Engine","Unsaved changes. Exit?"): return
        self.root.destroy()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(); style.theme_use("clam")
    style.configure("TNotebook", background="#1E1E2E", borderwidth=0)
    style.configure("TNotebook.Tab", background="#252540", foreground="#AAAACC",
                    padding=[8,4], font=("Segoe UI",8))
    style.map("TNotebook.Tab", background=[("selected","#3A3A60")], foreground=[("selected","#FFF")])
    app = ACEngine(root)
    root.protocol("WM_DELETE_WINDOW", app.on_exit)
    root.mainloop()
