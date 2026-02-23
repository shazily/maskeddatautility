import pandas as pd
import hashlib
import hmac
import os
import glob
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import gc
import sys
import ctypes

# --- SYSTEM & DPI ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('shazily.securemasker.v3.2.4')
except: pass

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_secure_hash(val, salt="", method="HMAC-SHA256"):
    if pd.isna(val) or str(val).strip() == "": return "NULL"
    msg = str(val).strip().lower().encode()
    if method == "HMAC-SHA256":
        return hmac.new(salt.encode(), msg, hashlib.sha256).hexdigest()[:16]
    return hashlib.sha256(msg).hexdigest()[:16]

class MaskingWizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secure Data Masking Utility v3.2.4")
        self.geometry("850x900")
        self.configure(bg="#F3F4F6")
        
        try: self.iconbitmap(resource_path("securemasker.ico"))
        except: pass

        # App State
        self.source_folder = tk.StringVar()
        self.dest_folder = tk.StringVar()
        self.salt_key = tk.StringVar(value="SECURE_SALT_2026")
        self.mask_method = tk.StringVar(value="HMAC-SHA256")
        self.output_fmt = tk.StringVar(value="Keep Original")
        self.out_prefix = tk.StringVar(value="MASKED_")
        self.do_zip = tk.BooleanVar(value=False)
        self.vars = {}

        self.master_view = tk.Frame(self, bg="#F3F4F6")
        self.master_view.pack(expand=True, fill="both")
        
        self.frames = {}
        for F in (StartPage, PathPage, MethodPage, ColumnPage, FinalPage, SecurityPage, ManualPage):
            page_name = F.__name__
            frame = F(parent=self.master_view, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.master_view.grid_rowconfigure(0, weight=1)
        self.master_view.grid_columnconfigure(0, weight=1)
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"): frame.on_show()

# --- COMPONENTS ---
def draw_breadcrumb(parent, step):
    container = tk.Frame(parent, bg="#F3F4F6")
    container.pack(pady=(40, 20))
    steps = ["FOLDERS", "METHOD", "COLUMNS", "FINISH"]
    for i, name in enumerate(steps):
        color = "#1E3A8A" if i+1 == step else "#94A3B8"
        tk.Label(container, text=f"{i+1}. {name}", font=("Segoe UI", 10, "bold" if i+1==step else "normal"), fg=color, bg="#F3F4F6", padx=15).pack(side="left")
        if i < 3: tk.Label(container, text=">", fg="#CBD5E1", bg="#F3F4F6").pack(side="left")

# --- PAGES ---
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        content = tk.Frame(self, bg="white")
        content.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(content, text="SECURE MASKING UTILITY", font=("Segoe UI", 28, "bold"), fg="#1E293B", bg="white").pack(pady=20)
        tk.Button(content, text="LAUNCH WIZARD", command=lambda: controller.show_frame("PathPage"), bg="#2563EB", fg="white", font=("Segoe UI", 12, "bold"), width=30, height=2, relief="flat").pack()
        nav_f = tk.Frame(self, bg="white")
        nav_f.pack(side="bottom", pady=40)
        tk.Button(nav_f, text="User Manual", command=lambda: controller.show_frame("ManualPage"), bg="white", fg="#3B82F6", borderwidth=0, font=("Segoe UI", 9, "bold")).pack(side="left", padx=20)
        tk.Button(nav_f, text="IT Compliance", command=lambda: controller.show_frame("SecurityPage"), bg="white", fg="#3B82F6", borderwidth=0, font=("Segoe UI", 9, "bold")).pack(side="left", padx=20)

class PathPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F3F4F6")
        self.controller = controller

    def on_show(self):
        for w in self.winfo_children(): w.destroy()
        draw_breadcrumb(self, 1)
        card = tk.Frame(self, bg="white", padx=40, pady=40, highlightbackground="#E5E7EB", highlightthickness=1)
        card.place(relx=0.5, rely=0.45, anchor="center", width=650)
        tk.Label(card, text="1. Folder Configuration", font=("Segoe UI", 16, "bold"), bg="white", fg="#1E293B").pack(anchor="w", pady=(0, 20))
        self.add_field(card, "Source Folder:", self.controller.source_folder)
        self.add_field(card, "Output Folder:", self.controller.dest_folder)
        tk.Label(card, text="Output Prefix:", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(15,0))
        tk.Entry(card, textvariable=self.controller.out_prefix, font=("Segoe UI", 10), bg="#F9FAFB", relief="solid", borderwidth=1).pack(fill="x", pady=5, ipady=3)
        tk.Button(self, text="Next Step →", command=lambda: self.controller.show_frame("MethodPage"), bg="#1E3A8A", fg="white", font=("Segoe UI", 11, "bold"), width=20, height=2, relief="flat").pack(side="bottom", pady=60)

    def add_field(self, parent, label, var):
        tk.Label(parent, text=label, bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10,0))
        row = tk.Frame(parent, bg="white")
        row.pack(fill="x")
        tk.Entry(row, textvariable=var, font=("Segoe UI", 10), bg="#F9FAFB", relief="solid", borderwidth=1).pack(side="left", fill="x", expand=True, ipady=3)
        tk.Button(row, text="Browse", command=lambda: var.set(filedialog.askdirectory()), bg="#E5E7EB", relief="flat").pack(side="right", padx=5)

class MethodPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F3F4F6")
        self.controller = controller

    def on_show(self):
        for w in self.winfo_children(): w.destroy()
        draw_breadcrumb(self, 2)
        card = tk.Frame(self, bg="white", padx=50, pady=40, highlightbackground="#E5E7EB", highlightthickness=1)
        card.place(relx=0.5, rely=0.45, anchor="center", width=650)
        tk.Label(card, text="2. Masking Strategy", font=("Segoe UI", 16, "bold"), bg="white", fg="#1E293B").pack(anchor="w", pady=(0, 20))
        self.controller.mask_method.trace_add("write", self.toggle_salt)
        self.add_radio(card, "Standard Hashing (SHA-256)", "SHA-256", "Fast deterministic masking.")
        self.add_radio(card, "Salted HMAC (HMAC-SHA256)", "HMAC-SHA256", "Secure keyed hashing for PII.")
        self.salt_frame = tk.Frame(card, bg="white")
        self.salt_frame.pack(fill="x", pady=10)
        tk.Label(self.salt_frame, text="Secret Salt Key:", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Entry(self.salt_frame, textvariable=self.controller.salt_key, show="*", font=("Segoe UI", 10), bg="#F9FAFB", relief="solid", borderwidth=1).pack(fill="x", pady=5, ipady=3)
        tk.Label(card, text="Output Format Selection:", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(15,0))
        ttk.Combobox(card, textvariable=self.controller.output_fmt, values=["Keep Original", "Convert to CSV", "Convert to Excel"], state="readonly").pack(fill="x", pady=5)
        tk.Checkbutton(card, text="Compress output into a ZIP archive", variable=self.controller.do_zip, bg="white", font=("Segoe UI", 9)).pack(anchor="w", pady=15)
        self.toggle_salt()
        btn_f = tk.Frame(self, bg="#F3F4F6")
        btn_f.pack(side="bottom", fill="x", padx=100, pady=60)
        tk.Button(btn_f, text="← Back", command=lambda: self.controller.show_frame("PathPage"), bg="#94A3B8", fg="white", font=("Segoe UI", 10, "bold"), width=15, height=2, relief="flat").pack(side="left")
        tk.Button(btn_f, text="Select Columns →", command=lambda: self.controller.show_frame("ColumnPage"), bg="#1E3A8A", fg="white", font=("Segoe UI", 10, "bold"), width=20, height=2, relief="flat").pack(side="right")

    def toggle_salt(self, *args):
        if self.controller.mask_method.get() == "SHA-256": self.salt_frame.pack_forget()
        else: self.salt_frame.pack(fill="x", pady=10)

    def add_radio(self, parent, label, val, help_t):
        row = tk.Frame(parent, bg="white")
        row.pack(fill="x", pady=2)
        tk.Radiobutton(row, text=label, variable=self.controller.mask_method, value=val, bg="white").pack(side="left")
        tk.Button(row, text="ⓘ", command=lambda: messagebox.showinfo("Algorithm", help_t), bg="white", fg="#2563EB", borderwidth=0, font=("Arial", 9, "bold")).pack(side="left")

class ColumnPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F3F4F6")
        self.controller = controller

    def on_show(self):
        for w in self.winfo_children(): w.destroy()
        draw_breadcrumb(self, 3)
        card = tk.Frame(self, bg="white", padx=40, pady=30, highlightbackground="#E5E7EB", highlightthickness=1)
        card.place(relx=0.5, rely=0.45, anchor="center", width=650, height=500)
        tk.Label(card, text="3. Target Column Selection", font=("Segoe UI", 16, "bold"), bg="white", fg="#1E293B").pack(anchor="w")
        btn_f = tk.Frame(card, bg="white")
        btn_f.pack(fill="x", pady=10)
        tk.Button(btn_f, text="AUTO-DETECT PII", command=self.auto_pii, bg="#DBEAFE", fg="#1E40AF", font=("Segoe UI", 8, "bold"), relief="flat", padx=12).pack(side="left")
        tk.Button(btn_f, text="SELECT ALL", command=lambda: [v.set(True) for v in self.controller.vars.values()], bg="#F3F4F6", font=("Segoe UI", 8), relief="flat", padx=12).pack(side="left", padx=10)
        tk.Button(btn_f, text="RESET", command=lambda: [v.set(False) for v in self.controller.vars.values()], bg="#F3F4F6", font=("Segoe UI", 8), relief="flat", padx=12).pack(side="left")
        container = tk.Frame(card, bg="#F9FAFB", bd=1, relief="solid")
        container.pack(fill="both", expand=True)
        cv = tk.Canvas(container, bg="#F9FAFB", highlightthickness=0)
        sb = ttk.Scrollbar(container, orient="vertical", command=cv.yview)
        sf = tk.Frame(cv, bg="#F9FAFB")
        cv.configure(yscrollcommand=sb.set)
        cv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        cv.create_window((0, 0), window=sf, anchor="nw")
        src = self.controller.source_folder.get()
        files = glob.glob(os.path.join(src, "*.xlsx")) + glob.glob(os.path.join(src, "*.csv"))
        f = files[0]
        df = pd.read_csv(f, nrows=0) if f.lower().endswith('.csv') else pd.read_excel(f, nrows=0)
        for c in df.columns:
            if c not in self.controller.vars: self.controller.vars[c] = tk.BooleanVar()
            tk.Checkbutton(sf, text=c, variable=self.controller.vars[c], bg="#F9FAFB", font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        sf.update_idletasks()
        cv.config(scrollregion=cv.bbox("all"))
        nav = tk.Frame(self, bg="#F3F4F6")
        nav.pack(side="bottom", fill="x", padx=100, pady=60)
        tk.Button(nav, text="← Back", command=lambda: self.controller.show_frame("MethodPage"), bg="#94A3B8", fg="white", font=("Segoe UI", 10, "bold"), width=15, height=2, relief="flat").pack(side="left")
        tk.Button(nav, text="Review Strategy →", command=self.review, bg="#2563EB", fg="white", font=("Segoe UI", 10, "bold"), width=20, height=2, relief="flat").pack(side="right")

    def auto_pii(self):
        keys = ['id', 'name', 'passport', 'license', 'dob', 'nationality', 'sr', 'remarks', 'description', 'complainant']
        for c, v in self.controller.vars.items():
            if any(k in c.lower() for k in keys): v.set(True)

    def review(self):
        win = tk.Toplevel(self)
        win.title("Review Strategy")
        win.geometry("650x650")
        masked = [c for c, v in self.controller.vars.items() if v.get()]
        
        # FIXED: INCLUDED OUTPUT FOLDER IN THE REVIEW POPUP
        details = (
            f"DATA SOURCE  : {self.controller.source_folder.get()}\n"
            f"DESTINATION  : {self.controller.dest_folder.get()}\n"
            f"METHODOLOGY  : {self.controller.mask_method.get()}\n"
            f"ZIP ARCHIVE  : {'Yes' if self.controller.do_zip.get() else 'No'}\n"
            f"OUTPUT FORMAT: {self.controller.output_fmt.get()}\n"
            f"--------------------------------------------------\n"
            f"TARGET PII COLUMNS:\n" + "\n".join([f"• {x}" for x in masked])
        )
        
        tk.Label(win, text="Confirm Masking Strategy", font=("Segoe UI", 12, "bold")).pack(pady=20)
        tk.Label(win, text=details, justify="left", bg="#F8FAFC", padx=25, pady=25, font=("Consolas", 9)).pack(fill="both", padx=30, pady=10)
        tk.Button(win, text="CONFIRM & RUN", command=lambda: [win.destroy(), self.controller.show_frame("FinalPage")], bg="#DC2626", fg="white", font=("Segoe UI", 11, "bold"), height=2).pack(pady=20)

class FinalPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        
    def on_show(self):
        for w in self.winfo_children(): w.destroy()
        draw_breadcrumb(self, 4)
        self.card = tk.Frame(self, bg="white", padx=50, pady=40, highlightbackground="#E5E7EB", highlightthickness=1)
        self.card.place(relx=0.5, rely=0.45, anchor="center", width=700)
        tk.Label(self.card, text="4. Execution & Summary", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=(0, 20))
        self.prog = ttk.Progressbar(self.card, orient="horizontal", length=600, mode="determinate")
        self.prog.pack(pady=10)
        self.summary = tk.Listbox(self.card, height=12, width=80, font=("Consolas", 9), bg="#F9FAFB", borderwidth=0)
        self.summary.pack(pady=15)
        self.btn_run = tk.Button(self.card, text="START MASKING PROCESS", command=self.execute, bg="#1E3A8A", fg="white", font=("Segoe UI", 12, "bold"), width=35, height=2, relief="flat")
        self.btn_run.pack(pady=20)

    def execute(self):
        self.btn_run.config(state="disabled", text="PROCESSING...")
        src, dst = self.controller.source_folder.get(), self.controller.dest_folder.get()
        selected = [c for c, v in self.controller.vars.items() if v.get()]
        salt, method, pre = self.controller.salt_key.get(), self.controller.mask_method.get(), self.controller.out_prefix.get()
        fmt = self.controller.output_fmt.get()
        
        files = glob.glob(os.path.join(src, "*.xlsx")) + glob.glob(os.path.join(src, "*.csv"))
        self.prog["maximum"] = len(files)
        total_rows = 0
        masked_paths = []

        self.summary.insert(tk.END, f"DATA SOURCE: {src}")
        self.summary.insert(tk.END, f"SAVING TO  : {dst}")
        self.summary.insert(tk.END, "-"*65)

        for i, fpath in enumerate(files):
            df = pd.read_csv(fpath) if fpath.lower().endswith('.csv') else pd.read_excel(fpath)
            total_rows += len(df)
            for c in selected:
                if c in df.columns: df[c] = df[c].apply(lambda x: get_secure_hash(x, salt, method))
            ext = os.path.splitext(fpath)[1]
            if fmt == "Convert to CSV": ext = ".csv"
            elif fmt == "Convert to Excel": ext = ".xlsx"
            out_name = f"{pre}{os.path.splitext(os.path.basename(fpath))[0]}{ext}"
            out_p = os.path.join(dst, out_name)
            df.to_csv(out_p, index=False) if ext == ".csv" else df.to_excel(out_p, index=False)
            masked_paths.append(out_p)
            self.summary.insert(tk.END, f"CREATED: {out_name} | Rows: {len(df)}")
            self.prog["value"] = i + 1
            self.update_idletasks()

        if self.controller.do_zip.get():
            zip_p = os.path.join(dst, f"Masked_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
            with zipfile.ZipFile(zip_p, 'w') as z:
                for p in masked_paths: z.write(p, os.path.basename(p))
            self.summary.insert(tk.END, f"ZIP ARCHIVE: {os.path.basename(zip_p)}")

        audit_dir = os.path.join(dst, "Audit_Logs")
        if not os.path.exists(audit_dir): os.makedirs(audit_dir)
        master_log_path = os.path.join(audit_dir, "Masking_History.log")
        with open(master_log_path, "a") as f:
            f.write(f"\n[{datetime.now()}] MASKING EVENT\n")
            f.write(f"Method: {method} | Total Records: {total_rows}\n")
            f.write(f"Source: {src}\n")
            f.write(f"Columns: {selected}\n")
            f.write("-" * 50 + "\n")

        self.btn_run.pack_forget()
        btn_f = tk.Frame(self.card, bg="white")
        btn_f.pack(pady=20)
        tk.Button(btn_f, text="OPEN FOLDER", command=lambda: os.startfile(dst), bg="#107C10", fg="white", width=15, relief="flat").pack(side="left", padx=10)
        tk.Button(btn_f, text="MASK MORE", command=lambda: self.controller.show_frame("PathPage"), bg="#2563EB", fg="white", width=15, relief="flat").pack(side="left", padx=10)
        tk.Button(btn_f, text="EXIT APP", command=self.controller.destroy, bg="#333333", fg="white", width=15, relief="flat").pack(side="left", padx=10)
        
        self.summary.insert(tk.END, "-"*65)
        self.summary.insert(tk.END, f"TOTAL RECORDS SANITIZED: {total_rows}")
        self.summary.insert(tk.END, f"COMPLIANCE LOGS UPDATED IN: /Audit_Logs/")
        self.summary.see(tk.END)
        gc.collect()

class SecurityPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="IT Compliance Standard", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=50)
        tk.Label(self, text="• Air-Gapped\n• RAM-Only Processing\n• Persistent Audit History", justify="left", bg="#F3F4F6", padx=40, pady=40).pack()
        tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage")).pack(pady=50)

class ManualPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="User Manual", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=20)
        guide = "HMAC: Keyed hashing.\nSHA-256: Basic masking.\n\nAUDIT LOGS: /Audit_Logs/ stores a permanent history of every run."
        tk.Label(self, text=guide, justify="left", bg="#F3F4F6", padx=40, pady=40).pack()
        tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage")).pack(pady=20)

if __name__ == "__main__":
    app = MaskingWizard()
    app.mainloop()