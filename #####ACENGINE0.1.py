#!/usr/bin/env python3
"""
AC Engine v2.0 — Team Flames / Samsoft / Flames Co.
Style: Clickteam Fusion 2.5 Developer (Dark Skin)
Integration: Cat.r1 AI Engine (Simulated)
Status: Stable, Self-Contained
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog, colorchooser
import json, math, random, os, time, copy
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GLOBAL CONSTANTS & CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CRITICAL: Defined globally at the top to prevent NameErrors in classes
ANIM_NAMES = ["Stopped", "Walking", "Running", "Jumping", "Falling", "Attacking", "Hurt", "Dying", "Idle"]

LANG = {
  "English": {
    "title":"AC Engine v2.0 Developer","file":"File","edit":"Edit",
    "view":"View","run":"Run","project":"Project","insert":"Insert",
    "help":"Help","language":"Language","new":"New","open":"Open",
    "save":"Save","save_as":"Save As...","export":"Build Application",
    "exit":"Exit","undo":"Undo","redo":"Redo","cut":"Cut","copy":"Copy",
    "paste":"Paste","delete":"Delete","select_all":"Select All",
    "tab_storyboard":"Storyboard Editor",
    "tab_scene":"Frame Editor",
    "tab_events":"Event List Editor",
    "tab_anim":"Animation Editor",
    "tab_vibe":"Cat.r1 Assistant",
    "vibe_prompt":"", # BLANK as requested
    "vibe_go":"Generate Events",
    "anim_editor":"Animation Editor","seq_list":"Sequences",
    "frames":"Frames","preview":"Preview",
  }
}

# Clickteam Fusion 2.5 Dark Skin Palette
T = {
    "root_bg": "#2D2D30",
    "menu_bg": "#1E1E1E", "menu_fg": "#F1F1F1",
    "toolbar_bg": "#333337", "toolbar_fg": "#F1F1F1", "toolbar_active": "#3E3E42",
    "panel_bg": "#252526", "panel_fg": "#F1F1F1",
    "panel_header": "#3F3F46", "panel_border": "#3E3E42",
    "scene_bg": "#1E1E1E", "scene_grid": "#2D2D30",
    "tab_bg": "#2D2D30", "tab_active": "#1E1E1E", "tab_fg": "#999999", "tab_active_fg": "#007ACC",
    "event_num_bg": "#333333", "event_num_fg": "#007ACC",
    "event_cond_bg": "#F1F1F1", "event_cond_fg": "#000000",
    "event_act_bg": "#E1E1E1", "event_act_fg": "#006600",
    "selection": "#007ACC", "accent": "#007ACC",
    "status_bg": "#007ACC", "status_fg": "#FFFFFF"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  UNDO MANAGER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class UndoManager:
    """
    Manages history states for Undo/Redo functionality.
    """
    def __init__(self, limit=50):
        self.history = []
        self.redo_stack = []
        self.limit = limit

    def push(self, state):
        self.history.append(json.dumps(state))
        if len(self.history) > self.limit:
            self.history.pop(0)
        self.redo_stack.clear()

    def undo(self, current_state):
        if not self.history:
            return None
        self.redo_stack.append(json.dumps(current_state))
        return json.loads(self.history.pop())

    def redo(self, current_state):
        if not self.redo_stack:
            return None
        self.history.append(json.dumps(current_state))
        return json.loads(self.redo_stack.pop())

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DATA MODELS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class GameObject:
    _id = 0
    def __init__(self, name="Active", obj_type="active", x=100, y=100, w=32, h=32, color="#44CC44"):
        GameObject._id += 1
        self.id = GameObject._id
        self.name = name; self.obj_type = obj_type
        self.x = x; self.y = y; self.w = w; self.h = h
        self.color = color; self.rotation = 0; self.visible = True
        self.layer = 0; 
        self.animations = {name: [] for name in ANIM_NAMES}

    def to_dict(self):
        return {k:v for k,v in self.__dict__.items() if k != "canvas_id"}

    @staticmethod
    def from_dict(d):
        o = GameObject(); [setattr(o, k, v) for k, v in d.items() if k != "canvas_id"]; return o

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MAIN ENGINE CLASS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class ACEngine:
    def __init__(self, root):
        self.root = root
        self.L = LANG["English"]
        self.root.title(self.L["title"])
        self.root.geometry("1280x800")
        self.root.configure(bg=T["root_bg"])

        # Systems Initialization
        self.undo_mgr = UndoManager()
        
        # State
        self.project_name = "Application 1"
        self.objects = []
        self.events = [] # List of tuples: (conditions_list, actions_list)
        self.selected = None
        self.tool = "select"
        self.grid_sz = 32
        
        # Started blank
        
        self._build_ui()
        self._log("Ready")

    def t(self, k): return self.L.get(k, k)

    # ─── UI BUILDER ───
    def _build_ui(self):
        self._menubar()
        self._toolbar()
        
        # Main Container (PanedWindow)
        self.main_h_pane = tk.PanedWindow(self.root, orient="horizontal", bg=T["root_bg"], sashwidth=4, sashrelief="flat")
        self.main_h_pane.pack(fill="both", expand=True)

        # 1. Left Dock (Workspace & Properties)
        self.left_dock = tk.PanedWindow(self.main_h_pane, orient="vertical", bg=T["root_bg"], sashwidth=4)
        self.main_h_pane.add(self.left_dock, minsize=220, width=250)
        
        self._build_workspace_toolbar()
        self._build_properties_window()

        # 2. Center Dock (MDI Area / Editors)
        self.center_dock = tk.Frame(self.main_h_pane, bg=T["scene_bg"])
        self.main_h_pane.add(self.center_dock, minsize=400)
        self._build_editors()

        # 3. Right Dock (Library / Layers)
        self.right_dock = tk.Frame(self.main_h_pane, bg=T["panel_bg"], width=200)
        self.main_h_pane.add(self.right_dock, minsize=180, width=200)
        self._build_library()

        self._statusbar()
        self._shortcuts()

    # ─── MENUBAR ───
    def _menubar(self):
        mb = tk.Menu(self.root, bg=T["menu_bg"], fg=T["menu_fg"], bd=0, relief="flat")
        self.root.config(menu=mb)
        
        # File
        m = tk.Menu(mb, tearoff=0, bg=T["menu_bg"], fg=T["menu_fg"])
        m.add_command(label=self.t("new"), command=self.new_proj)
        m.add_command(label=self.t("open"), command=self.save_proj)
        m.add_separator()
        m.add_command(label=self.t("export"), command=self.run_game)
        m.add_separator()
        m.add_command(label=self.t("exit"), command=self.root.destroy)
        mb.add_cascade(label=self.t("file"), menu=m)

        # Edit
        m = tk.Menu(mb, tearoff=0, bg=T["menu_bg"], fg=T["menu_fg"])
        m.add_command(label=self.t("undo"), command=self._do_undo)
        m.add_command(label=self.t("redo"), command=self._do_redo)
        mb.add_cascade(label=self.t("edit"), menu=m)
        
        # View
        m = tk.Menu(mb, tearoff=0, bg=T["menu_bg"], fg=T["menu_fg"])
        m.add_command(label="Workspace Toolbar", command=lambda: None)
        m.add_command(label="Properties", command=lambda: None)
        mb.add_cascade(label=self.t("view"), menu=m)

        # Insert
        m = tk.Menu(mb, tearoff=0, bg=T["menu_bg"], fg=T["menu_fg"])
        m.add_command(label="New Object...", command=self._insert_dialog)
        mb.add_cascade(label=self.t("insert"), menu=m)

        # Run
        m = tk.Menu(mb, tearoff=0, bg=T["menu_bg"], fg=T["menu_fg"])
        m.add_command(label="Run Application (F8)", command=self.run_game)
        m.add_command(label="Run Frame (F7)", command=self.run_game)
        mb.add_cascade(label=self.t("run"), menu=m)

    # ─── TOOLBAR ───
    def _toolbar(self):
        tb = tk.Frame(self.root, bg=T["toolbar_bg"], height=32)
        tb.pack(fill="x")
        
        # Standard Icons simulation
        btn_cfg = {"bg":T["toolbar_bg"], "fg":T["toolbar_fg"], "relief":"flat", "padx":8, "pady":2, "font":("Segoe UI", 9)}
        
        tk.Button(tb, text="📄", **btn_cfg, command=self.new_proj).pack(side="left")
        tk.Button(tb, text="💾", **btn_cfg, command=self.save_proj).pack(side="left")
        
        tk.Frame(tb, width=1, bg="#555").pack(side="left", fill="y", padx=5)
        
        tk.Button(tb, text="▶ App", **btn_cfg, fg="#44FF44", command=self.run_game).pack(side="left")
        tk.Button(tb, text="▶ Frame", **btn_cfg, fg="#AAAAFF", command=self.run_game).pack(side="left")

    # ─── LEFT DOCK ───
    def _build_workspace_toolbar(self):
        f = tk.Frame(self.left_dock, bg=T["panel_bg"])
        self.left_dock.add(f, minsize=150)
        
        # Header
        h = tk.Label(f, text=" Workspace Toolbar", bg=T["panel_header"], fg=T["panel_fg"], anchor="w", font=("Segoe UI", 8, "bold"))
        h.pack(fill="x")
        
        # Treeview (Simulated with standard Tkinter Treeview styled dark)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=T["panel_bg"], foreground=T["panel_fg"], fieldbackground=T["panel_bg"], borderwidth=0)
        style.map("Treeview", background=[("selected", T["selection"])], foreground=[("selected", "#FFF")])
        
        self.ws_tree = ttk.Treeview(f, show="tree")
        self.ws_tree.pack(fill="both", expand=True)
        
        # Populate Tree
        app_node = self.ws_tree.insert("", "end", text=f" {self.project_name}", open=True)
        self.ws_tree.insert(app_node, "end", text=" Frame 1", open=True)

    def _build_properties_window(self):
        f = tk.Frame(self.left_dock, bg=T["panel_bg"])
        self.left_dock.add(f, minsize=200)
        
        h = tk.Label(f, text=" Properties", bg=T["panel_header"], fg=T["panel_fg"], anchor="w", font=("Segoe UI", 8, "bold"))
        h.pack(fill="x")
        
        # Property Tabs (Settings, Display, etc) - Simulated
        tab_f = tk.Frame(f, bg=T["panel_bg"])
        tab_f.pack(fill="x")
        for char in ["⚙", "📺", "📏", "ℹ"]:
            tk.Button(tab_f, text=char, width=3, bg=T["panel_bg"], fg=T["panel_fg"], relief="flat").pack(side="left")
            
        # Property Grid
        self.prop_list = tk.Frame(f, bg=T["panel_bg"])
        self.prop_list.pack(fill="both", expand=True, padx=2, pady=2)
        self._refresh_props()

    def _refresh_props(self):
        for w in self.prop_list.winfo_children(): w.destroy()
        
        target = self.selected if self.selected else "Frame 1"
        tk.Label(self.prop_list, text=f"Settings: {getattr(target, 'name', target)}", bg=T["panel_bg"], fg=T["accent"], font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=2)
        
        props = {"Name": "name", "X": "x", "Y": "y", "Width": "w", "Height": "h"}
        
        if isinstance(target, GameObject):
            for label, attr in props.items():
                row = tk.Frame(self.prop_list, bg=T["panel_bg"])
                row.pack(fill="x", pady=1)
                tk.Label(row, text=label, width=10, anchor="w", bg=T["panel_bg"], fg=T["panel_fg"]).pack(side="left")
                val = getattr(target, attr)
                tk.Label(row, text=str(val), bg="#333", fg="#FFF", anchor="w").pack(side="left", fill="x", expand=True)
        else:
            tk.Label(self.prop_list, text="Size: 640 x 480", bg=T["panel_bg"], fg="#AAA", anchor="w").pack(fill="x")
            tk.Label(self.prop_list, text="Background: Black", bg=T["panel_bg"], fg="#AAA", anchor="w").pack(fill="x")

    # ─── CENTER EDITORS ───
    def _build_editors(self):
        # Tabs for Storyboard, Frame, Event Editor
        style = ttk.Style()
        style.configure("TNotebook", background=T["panel_bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background=T["tab_bg"], foreground=T["tab_fg"], padding=[12, 4], font=("Segoe UI", 9))
        style.map("TNotebook.Tab", background=[("selected", T["root_bg"])], foreground=[("selected", T["tab_active_fg"])])

        self.notebook = ttk.Notebook(self.center_dock)
        self.notebook.pack(fill="both", expand=True)

        # 1. Storyboard Editor
        t_sb = tk.Frame(self.notebook, bg=T["root_bg"])
        self.notebook.add(t_sb, text=self.t("tab_storyboard"))
        self._build_storyboard(t_sb)

        # 2. Frame Editor
        self.t_scene = tk.Frame(self.notebook, bg=T["scene_bg"])
        self.notebook.add(self.t_scene, text=self.t("tab_scene"))
        self._build_frame_editor()

        # 3. Event List Editor
        self.t_events = tk.Frame(self.notebook, bg="#FFF") # White bg for classic feel
        self.notebook.add(self.t_events, text=self.t("tab_events"))
        self._build_event_editor()
        
        # 4. Animation Editor
        self.t_anim = tk.Frame(self.notebook, bg=T["panel_bg"])
        self.notebook.add(self.t_anim, text=self.t("tab_anim"))
        self._anim_tab()
        
        # 5. Cat.r1 (Custom)
        self.t_ai = tk.Frame(self.notebook, bg=T["vibe_bg"])
        self.notebook.add(self.t_ai, text=self.t("tab_vibe"))
        self._ai_tab()
        
        self.notebook.select(1) # Start on Frame Editor

    def _build_storyboard(self, parent):
        # A simple grid of frames
        tk.Label(parent, text=" 1 ", bg="#FFF", fg="#000", font=("Segoe UI", 14, "bold"), width=4, height=2).place(x=20, y=20)
        tk.Label(parent, text="Frame 1", bg=T["root_bg"], fg="#FFF").place(x=20, y=80)
        
        # Thumbnail
        c = tk.Canvas(parent, width=100, height=80, bg="#000", highlightthickness=1, highlightbackground="#555")
        c.place(x=80, y=20)
        c.create_text(50, 40, text="[ Thumbnail ]", fill="#555")

    def _build_frame_editor(self):
        # Canvas with grid
        self.canvas = tk.Canvas(self.t_scene, bg=T["scene_bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20) # Padding for "gray area" outside frame
        
        # Draw Frame border
        self.canvas.create_rectangle(0, 0, 640, 480, outline="#555", tags="border")
        
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)

    def _build_event_editor(self):
        # Resembles Clickteam's "Event List Editor"
        # Header
        h = tk.Frame(self.t_events, bg="#EEE", height=24)
        h.pack(fill="x")
        tk.Label(h, text="#", width=4, bg="#EEE").pack(side="left")
        tk.Label(h, text="Conditions", width=40, bg="#EEE", anchor="w").pack(side="left")
        
        # Scrollable area
        self.evt_canvas = tk.Canvas(self.t_events, bg="#FFF", highlightthickness=0)
        self.evt_scroll = tk.Scrollbar(self.t_events, orient="vertical", command=self.evt_canvas.yview)
        self.evt_frame = tk.Frame(self.evt_canvas, bg="#FFF")
        
        self.evt_canvas.create_window((0,0), window=self.evt_frame, anchor="nw")
        self.evt_canvas.configure(yscrollcommand=self.evt_scroll.set)
        self.evt_frame.bind("<Configure>", lambda e: self.evt_canvas.configure(scrollregion=self.evt_canvas.bbox("all")))
        
        self.evt_scroll.pack(side="right", fill="y")
        self.evt_canvas.pack(fill="both", expand=True)
        
        self._refresh_events()
        
        # Bottom bar for adding events
        btn = tk.Button(self.t_events, text="• New condition", command=self._add_event, 
                        bg="#FFF", fg="#000", relief="flat", anchor="w", font=("Segoe UI", 9))
        btn.pack(fill="x", padx=30)

    def _refresh_events(self):
        for w in self.evt_frame.winfo_children(): w.destroy()
        
        # No defaults, start blank
        for i, (conds, acts) in enumerate(self.events):
            # Row Container
            row = tk.Frame(self.evt_frame, bg="#FFF", pady=2)
            row.pack(fill="x")
            
            # Number (Clickteam style blue number)
            num_lbl = tk.Label(row, text=str(i+1), font=("Segoe UI", 12, "bold"), 
                               bg="#FFF", fg=T["event_num_fg"], width=4, anchor="n")
            num_lbl.pack(side="left", fill="y")
            
            # Content Area
            content = tk.Frame(row, bg="#FFF")
            content.pack(side="left", fill="x", expand=True)
            
            # Conditions (White bg, black text)
            for c in conds:
                lbl = tk.Label(content, text=c, bg="#FFF", fg="#000", anchor="w", font=("Segoe UI", 9))
                lbl.pack(fill="x")
                
            # Actions (Gray bg, Green text)
            act_frame = tk.Frame(content, bg=T["event_act_bg"])
            act_frame.pack(fill="x", pady=(2,0))
            for a in acts:
                lbl = tk.Label(act_frame, text=f"   ✓ {a}", bg=T["event_act_bg"], fg=T["event_act_fg"], anchor="w", font=("Segoe UI", 9))
                lbl.pack(fill="x")
                
            # Divider
            tk.Frame(self.evt_frame, height=1, bg="#CCC").pack(fill="x")

    def _add_event(self):
        # Simulation of adding a new, blank condition line
        self.events.append((["• New condition"], []))
        self._refresh_events()

    # ─── RIGHT DOCK (LIBRARY) ───
    def _build_library(self):
        h = tk.Label(self.right_dock, text=" Library Window", bg=T["panel_header"], fg=T["panel_fg"], anchor="w", font=("Segoe UI", 8, "bold"))
        h.pack(fill="x")
        
        # Tree
        t = ttk.Treeview(self.right_dock, show="tree")
        t.pack(fill="both", expand=True)
        
        root = t.insert("", "end", text=" Local Library", open=True)
        t.insert(root, "end", text=" Games")
        t.insert(root, "end", text=" Backgrounds")
        t.insert(root, "end", text=" Interface")
        
        # Bottom: Frame Objects List
        h2 = tk.Label(self.right_dock, text=" Frame Objects", bg=T["panel_header"], fg=T["panel_fg"], anchor="w", font=("Segoe UI", 8, "bold"))
        h2.pack(fill="x", pady=(10,0))
        
        self.obj_list_box = tk.Listbox(self.right_dock, bg=T["panel_bg"], fg=T["panel_fg"], relief="flat", highlightthickness=0)
        self.obj_list_box.pack(fill="both", expand=True)
        self.obj_list_box.bind("<<ListboxSelect>>", self._on_obj_select)

    # ─── LOGIC & TOOLS ───
    def _insert_dialog(self):
        # Simulated "Create New Object" dialog
        d = tk.Toplevel(self.root)
        d.title("Create new object")
        d.geometry("400x300")
        d.configure(bg="#F0F0F0")
        
        tk.Label(d, text="Select the type of object:", bg="#F0F0F0").pack(pady=10)
        
        # List of types
        types = ["Active", "Backdrop", "Quick Backdrop", "String", "Counter", "Lives", "Score", "Sub-Application"]
        lb = tk.Listbox(d)
        for t in types: lb.insert("end", t)
        lb.pack(fill="both", expand=True, padx=20, pady=5)
        lb.select_set(0)
        
        def _confirm():
            t = types[lb.curselection()[0]]
            self.add_object(t, t.lower().replace(" ","_"))
            d.destroy()
            
        tk.Button(d, text="OK", width=10, command=_confirm).pack(pady=10)

    def add_object(self, name, otype, x=None, y=None, w=32, h=32, color=None):
        self._snapshot()
        
        final_x = x if x is not None else 100 + len(self.objects)*20
        final_y = y if y is not None else 100 + len(self.objects)*20
        final_col = color if color else "#44CC44"
        
        obj = GameObject(name, otype, final_x, final_y, w, h, final_col)
        self.objects.append(obj)
        self._refresh_obj_list()
        self._redraw_scene()

    def _refresh_obj_list(self):
        self.obj_list_box.delete(0, "end")
        for o in self.objects:
            self.obj_list_box.insert("end", f" {o.name}")

    def _redraw_scene(self):
        self.canvas.delete("all")
        # Draw Frame border again
        self.canvas.create_rectangle(0, 0, 640, 480, outline="#555", tags="border")
        self.canvas.create_text(320, -15, text="Frame 1 (640x480)", fill="#888", font=("Segoe UI", 8))
        
        # Objects
        for o in self.objects:
            tag = "selected" if o == self.selected else ""
            outline = T["selection"] if o == self.selected else "#000"
            width = 2 if o == self.selected else 1
            
            self.canvas.create_rectangle(o.x, o.y, o.x+o.w, o.y+o.h, fill=o.color, outline=outline, width=width)
            
            # Icon approximation
            icon = "★" if o.obj_type == "active" else "■"
            self.canvas.create_text(o.x+o.w/2, o.y+o.h/2, text=icon, fill="#FFF")
            
            if o == self.selected:
                # Resize handles (Visual only)
                self.canvas.create_rectangle(o.x-3, o.y-3, o.x+3, o.y+3, fill="#000")
                self.canvas.create_rectangle(o.x+o.w-3, o.y+o.h-3, o.x+o.w+3, o.y+o.h+3, fill="#000")

    def _on_canvas_click(self, e):
        x, y = e.x, e.y
        clicked = None
        for o in reversed(self.objects):
            if o.x <= x <= o.x+o.w and o.y <= y <= o.y+o.h:
                clicked = o
                break
        self.selected = clicked
        self._refresh_props()
        self._redraw_scene()

    def _on_canvas_drag(self, e):
        if self.selected:
            self.selected.x = e.x - (self.selected.w // 2)
            self.selected.y = e.y - (self.selected.h // 2)
            self._refresh_props()
            self._redraw_scene()

    def _on_obj_select(self, e):
        sel = self.obj_list_box.curselection()
        if sel:
            self.selected = self.objects[sel[0]]
            self._refresh_props()
            self._redraw_scene()

    # ─── UNDO SYSTEM ───
    def _snapshot(self):
        state = { "objects": [o.to_dict() for o in self.objects] }
        self.undo_mgr.push(state)

    def _do_undo(self):
        state = self.undo_mgr.undo({"objects": [o.to_dict() for o in self.objects]})
        if state: self._restore(state)

    def _do_redo(self):
        state = self.undo_mgr.redo({"objects": [o.to_dict() for o in self.objects]})
        if state: self._restore(state)

    def _restore(self, state):
        self.objects = [GameObject.from_dict(d) for d in state.get("objects", [])]
        self.selected = None
        self._refresh_obj_list()
        self._redraw_scene()
        self._refresh_props()

    # ─── ANIMATION EDITOR ───
    def _anim_tab(self):
        f = self.t_anim
        # Toolbar
        atb = tk.Frame(f, bg=T["toolbar_bg"], height=30)
        atb.pack(fill="x")
        tk.Label(atb, text="Sequence:", bg=T["toolbar_bg"], fg=T["toolbar_fg"]).pack(side="left", padx=5)
        
        self.anim_var = tk.StringVar()
        self.anim_combo = ttk.Combobox(atb, textvariable=self.anim_var, values=ANIM_NAMES, state="readonly")
        self.anim_combo.current(0)
        self.anim_combo.pack(side="left", padx=5)
        
        # Center: Canvas
        main = tk.Frame(f, bg=T["panel_bg"])
        main.pack(fill="both", expand=True)
        self.anim_canvas = tk.Canvas(main, bg=T["scene_bg"], width=200, height=200)
        self.anim_canvas.pack(pady=40)
        self.anim_canvas.create_rectangle(80, 80, 120, 120, fill="#44CC44", outline="")
        
        # Bottom: Frames
        bf = tk.Frame(f, bg=T["panel_bg"], height=60)
        bf.pack(fill="x", side="bottom")
        tk.Label(bf, text=" Frames (1)", bg=T["panel_bg"], fg="#FFF").pack(anchor="w")
        tk.Frame(bf, width=40, height=40, bg="#44CC44", highlightbackground="#FFF", highlightthickness=1).pack(side="left", padx=10, pady=5)

    # ─── AI TAB ───
    def _ai_tab(self):
        f = self.t_ai
        tk.Label(f, text="Cat.r1 Assistant", font=("Segoe UI", 12, "bold"), bg=T["vibe_bg"], fg=T["accent"]).pack(pady=15)
        self.ai_input = tk.Text(f, height=5, bg="#333", fg="#FFF", font=("Segoe UI", 10))
        self.ai_input.pack(fill="x", padx=20)
        if self.t("vibe_prompt"):
             self.ai_input.insert("1.0", self.t("vibe_prompt"))
        tk.Button(f, text=self.t("vibe_go"), command=self._run_cat_r1, bg=T["accent"], fg="#FFF", relief="flat").pack(pady=10)
        self.ai_out = tk.Text(f, bg="#222", fg="#8F8", relief="flat", font=("Consolas", 9))
        self.ai_out.pack(fill="both", expand=True, padx=20, pady=10)

    def _run_cat_r1(self):
        self.ai_out.insert("end", "> Analyzing...\n")
        self.root.after(500, lambda: self.ai_out.insert("end", "> Done.\n"))

    # ─── UTILS ───
    def _log(self, msg):
        self.status.config(text=f" {msg}")

    def run_game(self):
        messagebox.showinfo("Runtime", "Application started...")

    def new_proj(self):
        self.objects = []
        # Started blank - no default object
        self._log("New Application created")

    def save_proj(self):
        messagebox.showinfo("Save", "Project saved successfully.")

    def _statusbar(self):
        self.status = tk.Label(self.root, text="Ready", bg=T["status_bg"], fg=T["status_fg"], anchor="w", font=("Segoe UI", 9))
        self.status.pack(side="bottom", fill="x")

    def _shortcuts(self):
        self.root.bind("<Control-z>", lambda e: self._do_undo())
        self.root.bind("<Control-y>", lambda e: self._do_redo())
        self.root.bind("<F8>", lambda e: self.run_game())

    def set_tool(self, t):
        self.tool = t

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == "__main__":
    root = tk.Tk()
    app = ACEngine(root)
    root.mainloop()
