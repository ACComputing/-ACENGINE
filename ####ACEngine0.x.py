#!/usr/bin/env python3
"""
AC Engine v2.0 — Team Flames / Samsoft / Flames Co.
Integration: Cat.r1 AI Engine (Simulated)
Fixes: Added UndoManager, ANIM_NAMES, and Animation Editor Tab
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
    "title":"AC Engine v2.0 + Cat.r1 AI","file":"File","edit":"Edit",
    "view":"View","run":"Run","project":"Project","insert":"Insert",
    "help":"Help","language":"Language","new":"New Project","open":"Open Project",
    "save":"Save Project","save_as":"Save As...","export":"Export Game",
    "exit":"Exit","undo":"Undo","redo":"Redo","cut":"Cut","copy":"Copy",
    "paste":"Paste","delete":"Delete","select_all":"Select All",
    "tab_scene":"Frame Editor","tab_events":"Event Editor",
    "tab_blueprints":"Blueprints","tab_anim":"Animation","tab_vibe":"Cat.r1 AI",
    "vibe_prompt":"[Cat.r1] Describe your game logic or mechanics...",
    "vibe_go":"✦ Cat.r1 Generate",
    "anim_editor":"Animation Editor","seq_list":"Sequences",
    "frames":"Frames","preview":"Preview",
  }
}

# Dark Theme Palette
T = {
    "menu_bg":"#2B2B3D","menu_fg":"#4488FF",
    "toolbar_bg":"#333348","toolbar_fg":"#4488FF","toolbar_active":"#5A5AFF",
    "panel_bg":"#1E1E2E","panel_fg":"#4488FF","panel_header":"#2A2A40","panel_border":"#404060",
    "scene_bg":"#151530","scene_grid":"#252550",
    "tab_bg":"#252540","tab_active":"#3A3A60","tab_fg":"#4488FF","tab_active_fg":"#FFFFFF",
    "event_row1":"#1E1E30","event_row2":"#252540","event_cond":"#3366AA","event_action":"#44AA44",
    "bp_bg":"#1A1A2E","bp_grid":"#222240",
    "bp_node_body":"#2A2A44","bp_node_header":"#444466",
    "vibe_bg":"#1A1A2E","vibe_input":"#252540",
    "accent":"#5A5AFF","selection":"#FFAA33",
    "status_bg":"#1A1A28","status_fg":"#4488FF"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  UNDO MANAGER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class UndoManager:
    """
    Manages history states for Undo/Redo functionality.
    Defined before ACEngine to avoid NameError during initialization.
    """
    def __init__(self, limit=50):
        self.history = []
        self.redo_stack = []
        self.limit = limit

    def push(self, state):
        # Deep copy the state using JSON serialization to ensure total isolation
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
    def __init__(self, name="Obj", obj_type="active", x=100, y=100, w=32, h=32, color="#44CC44"):
        GameObject._id += 1
        self.id = GameObject._id
        self.name = name; self.obj_type = obj_type
        self.x = x; self.y = y; self.w = w; self.h = h
        self.color = color; self.rotation = 0; self.visible = True
        self.layer = 0; 
        # Initialize empty animation lists for each defined sequence
        self.animations = {name: [] for name in ANIM_NAMES}

    def to_dict(self):
        return {k:v for k,v in self.__dict__.items() if k != "canvas_id"}

    @staticmethod
    def from_dict(d):
        o = GameObject(); [setattr(o, k, v) for k, v in d.items() if k != "canvas_id"]; return o

class GameEvent:
    def __init__(self, c=None, a=None):
        self.conditions = c or []; self.actions = a or []

class BPNode:
    _id = 0
    def __init__(self, title="Node", category="event", x=0, y=0, ins=None, outs=None):
        BPNode._id += 1
        self.id = BPNode._id; self.title = title; self.category = category
        self.x = x; self.y = y; self.w = 160; self.h = 100
        self.inputs = ins or []; self.outputs = outs or []

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MAIN ENGINE CLASS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class ACEngine:
    def __init__(self, root):
        self.root = root
        self.L = LANG["English"]
        self.root.title(self.L["title"])
        self.root.geometry("1024x768")
        self.root.configure(bg=T["menu_bg"])

        # Systems Initialization
        self.undo_mgr = UndoManager()
        
        # State
        self.project_name = "Untitled"
        self.objects = []
        self.events = []
        self.bp_nodes = []
        self.bp_conns = []
        self.selected = None
        self.tool = "select"
        self.zoom = 1.0
        self.grid_sz = 16
        self.offset = [0, 0]
        self.dragging = False
        
        self._build_ui()
        self._log("AC Engine v2.0 initialized. Cat.r1 AI Ready.")

    def t(self, k): return self.L.get(k, k)

    # ─── UI BUILDER ───
    def _build_ui(self):
        self._menubar()
        self._toolbar()
        self._main_layout()
        self._statusbar()
        self._shortcuts()

    def _menubar(self):
        mb = tk.Menu(self.root, bg=T["menu_bg"], fg=T["menu_fg"])
        self.root.config(menu=mb)
        
        # File Menu
        fm = tk.Menu(mb, tearoff=0, bg=T["menu_bg"], fg=T["menu_fg"])
        fm.add_command(label=self.t("new"), command=self.new_proj)
        fm.add_command(label=self.t("save"), command=self.save_proj)
        fm.add_separator()
        fm.add_command(label=self.t("exit"), command=self.root.destroy)
        mb.add_cascade(label=self.t("file"), menu=fm)

        # Edit Menu (Undo/Redo)
        em = tk.Menu(mb, tearoff=0, bg=T["menu_bg"], fg=T["menu_fg"])
        em.add_command(label=self.t("undo"), command=self._do_undo, accelerator="Ctrl+Z")
        em.add_command(label=self.t("redo"), command=self._do_redo, accelerator="Ctrl+Y")
        mb.add_cascade(label=self.t("edit"), menu=em)

    def _toolbar(self):
        tb = tk.Frame(self.root, bg=T["toolbar_bg"], height=40)
        tb.pack(fill="x")
        
        tools = [("Select", "select"), ("Move", "move"), ("Active", "active"), ("Backdrop", "backdrop")]
        for txt, mode in tools:
            tk.Button(tb, text=txt, command=lambda m=mode: self.set_tool(m),
                      bg=T["toolbar_bg"], fg=T["toolbar_fg"], relief="flat", padx=10).pack(side="left", pady=2)
        
        tk.Button(tb, text="▶ Run", command=self.run_game, bg=T["toolbar_bg"], fg="#44FF44", 
                  font=("Segoe UI", 9, "bold"), relief="flat").pack(side="left", padx=20)

    def _main_layout(self):
        self.panes = tk.PanedWindow(self.root, orient="horizontal", bg=T["panel_border"])
        self.panes.pack(fill="both", expand=True)

        # Left: Project Tree
        self.lp = tk.Frame(self.panes, bg=T["panel_bg"], width=200)
        self.panes.add(self.lp, minsize=150)
        self._build_object_list()

        # Center: Tabs (Scene, Events, Anim, AI)
        self.cp = tk.Frame(self.panes, bg=T["scene_bg"])
        self.panes.add(self.cp, minsize=400)
        self._build_tabs()

        # Right: Properties
        self.rp = tk.Frame(self.panes, bg=T["panel_bg"], width=250)
        self.panes.add(self.rp, minsize=200)
        self._build_props()

    def _build_object_list(self):
        tk.Label(self.lp, text="Objects", bg=T["panel_header"], fg=T["panel_fg"]).pack(fill="x")
        self.obj_list = tk.Listbox(self.lp, bg=T["panel_bg"], fg="#FFF", selectbackground=T["accent"], relief="flat")
        self.obj_list.pack(fill="both", expand=True)
        self.obj_list.bind("<<ListboxSelect>>", self._on_obj_select)
        
        btn_f = tk.Frame(self.lp, bg=T["panel_bg"])
        btn_f.pack(fill="x")
        tk.Button(btn_f, text="+", command=lambda: self.add_object("active"), bg=T["panel_bg"], fg=T["panel_fg"], relief="flat").pack(side="left", expand=True, fill="x")
        tk.Button(btn_f, text="-", command=self.del_object, bg=T["panel_bg"], fg=T["panel_fg"], relief="flat").pack(side="left", expand=True, fill="x")

    def _build_tabs(self):
        self.notebook = ttk.Notebook(self.cp)
        self.notebook.pack(fill="both", expand=True)

        # Tab 1: Scene Editor
        self.t_scene = tk.Frame(self.notebook, bg=T["scene_bg"])
        self.notebook.add(self.t_scene, text=self.t("tab_scene"))
        self.canvas = tk.Canvas(self.t_scene, bg=T["scene_bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)

        # Tab 2: Events
        self.t_events = tk.Frame(self.notebook, bg=T["event_row1"])
        self.notebook.add(self.t_events, text=self.t("tab_events"))
        self._build_event_editor()

        # Tab 3: Blueprints
        self.t_bp = tk.Frame(self.notebook, bg=T["bp_bg"])
        self.notebook.add(self.t_bp, text=self.t("tab_blueprints"))
        
        # Tab 4: Animation
        self.t_anim = tk.Frame(self.notebook, bg=T["panel_bg"])
        self.notebook.add(self.t_anim, text=self.t("tab_anim"))
        self._anim_tab()

        # Tab 5: Cat.r1 AI
        self.t_ai = tk.Frame(self.notebook, bg=T["vibe_bg"])
        self.notebook.add(self.t_ai, text=self.t("tab_vibe"))
        self._ai_tab()

    def _build_props(self):
        tk.Label(self.rp, text="Properties", bg=T["panel_header"], fg=T["panel_fg"]).pack(fill="x")
        self.prop_frame = tk.Frame(self.rp, bg=T["panel_bg"])
        self.prop_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def _statusbar(self):
        self.status = tk.Label(self.root, text="Ready", bg=T["status_bg"], fg=T["status_fg"], anchor="w")
        self.status.pack(side="bottom", fill="x")

    # ─── ANIMATION EDITOR ───
    def _anim_tab(self):
        # Layout: Left list (animations), Center (Canvas/Preview), Bottom (Timeline)
        f = self.t_anim
        
        # Toolbar
        atb = tk.Frame(f, bg=T["toolbar_bg"], height=30)
        atb.pack(fill="x")
        tk.Label(atb, text="Animation Sequence:", bg=T["toolbar_bg"], fg=T["toolbar_fg"]).pack(side="left", padx=5)
        
        self.anim_var = tk.StringVar()
        # FIX: Uses global ANIM_NAMES, which must be defined at top of file
        self.anim_combo = ttk.Combobox(atb, textvariable=self.anim_var, values=ANIM_NAMES, state="readonly")
        self.anim_combo.current(0)
        self.anim_combo.pack(side="left", padx=5)
        
        # Main Area
        main = tk.Frame(f, bg=T["panel_bg"])
        main.pack(fill="both", expand=True)
        
        # Preview Canvas
        self.anim_canvas = tk.Canvas(main, bg=T["scene_bg"], width=300, height=300)
        self.anim_canvas.pack(pady=20)
        
        # Controls
        ctrl = tk.Frame(main, bg=T["panel_bg"])
        ctrl.pack(fill="x", pady=10)
        tk.Button(ctrl, text="⏪", bg=T["panel_bg"], fg="#FFF", relief="flat").pack(side="left", padx=2)
        tk.Button(ctrl, text="▶ Play", bg=T["accent"], fg="#FFF", relief="flat").pack(side="left", padx=5)
        tk.Button(ctrl, text="Import Frames...", bg=T["panel_header"], fg=T["panel_fg"], relief="flat").pack(side="right", padx=10)

    # ─── AI TAB (Cat.r1) ───
    def _ai_tab(self):
        f = self.t_ai
        tk.Label(f, text="Cat.r1 AI Engine — Neural Game Generation", font=("Segoe UI", 12, "bold"), bg=T["vibe_bg"], fg=T["accent"]).pack(pady=15)
        
        self.ai_input = tk.Text(f, height=5, bg=T["vibe_input"], fg="#FFF", insertbackground="#FFF", relief="flat", font=("Consolas", 10))
        self.ai_input.pack(fill="x", padx=20)
        self.ai_input.insert("1.0", self.t("vibe_prompt"))
        
        btn = tk.Button(f, text=self.t("vibe_go"), command=self._run_cat_r1, bg=T["accent"], fg="#FFF", font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=5)
        btn.pack(pady=10)
        
        tk.Label(f, text="Reasoning Output:", bg=T["vibe_bg"], fg="#888").pack(anchor="w", padx=20)
        self.ai_out = tk.Text(f, bg=T["vibe_input"], fg="#8F8", relief="flat", font=("Consolas", 9))
        self.ai_out.pack(fill="both", expand=True, padx=20, pady=10)

    def _run_cat_r1(self):
        prompt = self.ai_input.get("1.0", "end").strip()
        self.ai_out.delete("1.0", "end")
        self.ai_out.insert("end", "> Initializing Cat.r1-14B model...\n")
        self.ai_out.update()
        
        # Use root.after to prevent UI freezing (Simulated Async)
        self.root.after(500, lambda: self._cat_r1_step1(prompt))

    def _cat_r1_step1(self, prompt):
        self.ai_out.insert("end", "> Analyzing prompt tokens...\n")
        self.ai_out.update()
        self.root.after(500, lambda: self._cat_r1_step2(prompt))

    def _cat_r1_step2(self, prompt):
        self.ai_out.insert("end", f"> Generative Task: '{prompt}'\n> Creating objects and events...\n> DONE.")
        self.add_object("generated_obj")

    # ─── LOGIC ───
    def set_tool(self, t):
        self.tool = t
        self._log(f"Tool selected: {t}")

    def add_object(self, otype):
        self._snapshot() # Undo
        name = f"{otype}_{len(self.objects)}"
        obj = GameObject(name, otype, 200, 200)
        self.objects.append(obj)
        self._refresh_obj_list()
        self._redraw_scene()

    def del_object(self):
        if self.selected:
            self._snapshot()
            self.objects.remove(self.selected)
            self.selected = None
            self._refresh_obj_list()
            self._redraw_scene()

    def _refresh_obj_list(self):
        self.obj_list.delete(0, "end")
        for o in self.objects:
            self.obj_list.insert("end", f" {o.name} ({o.obj_type})")

    def _redraw_scene(self):
        self.canvas.delete("all")
        # Grid
        w, h = 2000, 2000
        for x in range(0, w, self.grid_sz):
            self.canvas.create_line(x, 0, x, h, fill=T["scene_grid"])
        for y in range(0, h, self.grid_sz):
            self.canvas.create_line(0, y, w, y, fill=T["scene_grid"])
        
        # Objects
        for o in self.objects:
            color = o.color
            if o == self.selected:
                self.canvas.create_rectangle(o.x-2, o.y-2, o.x+o.w+2, o.y+o.h+2, outline=T["selection"], width=2)
            self.canvas.create_rectangle(o.x, o.y, o.x+o.w, o.y+o.h, fill=color, outline="#FFF")
            self.canvas.create_text(o.x, o.y-10, text=o.name, fill="#FFF", anchor="sw", font=("Consolas", 8))

    def _on_canvas_click(self, e):
        x, y = e.x, e.y
        # Simple selection
        clicked = None
        for o in reversed(self.objects):
            if o.x <= x <= o.x+o.w and o.y <= y <= o.y+o.h:
                clicked = o
                break
        self.selected = clicked
        self._redraw_scene()
        if not clicked and self.tool == "active":
            self.add_object("active")

    def _on_canvas_drag(self, e):
        if self.selected:
            self.selected.x = e.x - (self.selected.w // 2)
            self.selected.y = e.y - (self.selected.h // 2)
            self._redraw_scene()

    def _on_obj_select(self, e):
        sel = self.obj_list.curselection()
        if sel:
            idx = sel[0]
            self.selected = self.objects[idx]
            self._redraw_scene()

    def _build_event_editor(self):
        # Simple placeholder for event editor
        tk.Label(self.t_events, text="Condition", bg=T["event_row1"], fg=T["event_cond"], font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.t_events, text="Action", bg=T["event_row1"], fg=T["event_action"], font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self.t_events, text="Always", bg=T["event_row2"], fg="#FFF").grid(row=1, column=0, sticky="w", padx=10)
        tk.Label(self.t_events, text="Set Speed to 50", bg=T["event_row2"], fg="#FFF").grid(row=1, column=1, sticky="w", padx=10)

    # ─── UNDO SYSTEM WRAPPERS ───
    def _snapshot(self):
        state = {
            "objects": [o.to_dict() for o in self.objects],
            "events": [] # Add events serialization
        }
        self.undo_mgr.push(state)

    def _do_undo(self):
        current = {"objects": [o.to_dict() for o in self.objects]}
        state = self.undo_mgr.undo(current)
        if state:
            self._restore_state(state)
            self._log("Undo performed")

    def _do_redo(self):
        current = {"objects": [o.to_dict() for o in self.objects]}
        state = self.undo_mgr.redo(current)
        if state:
            self._restore_state(state)
            self._log("Redo performed")

    def _restore_state(self, state):
        self.objects = [GameObject.from_dict(d) for d in state.get("objects", [])]
        self.selected = None
        self._refresh_obj_list()
        self._redraw_scene()

    # ─── UTILS ───
    def _log(self, msg):
        self.status.config(text=f" {msg}")
        print(f"[LOG] {msg}")

    def run_game(self):
        messagebox.showinfo("Run", "Building and launching game runtime...")

    def new_proj(self):
        self.objects = []
        self._refresh_obj_list()
        self._redraw_scene()

    def save_proj(self):
        file = filedialog.asksaveasfilename(defaultextension=".json")
        if file:
            data = {"objects": [o.to_dict() for o in self.objects]}
            with open(file, "w") as f:
                json.dump(data, f)
            self._log(f"Saved to {os.path.basename(file)}")

    def _shortcuts(self):
        self.root.bind("<Control-z>", lambda e: self._do_undo())
        self.root.bind("<Control-y>", lambda e: self._do_redo())

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook", background=T["panel_bg"], borderwidth=0)
    style.configure("TNotebook.Tab", background=T["tab_bg"], foreground=T["tab_fg"], padding=[10, 5])
    style.map("TNotebook.Tab", background=[("selected", T["tab_active"])], foreground=[("selected", "#FFF")])
    
    app = ACEngine(root)
    root.mainloop()
