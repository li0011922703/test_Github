import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import socket
import os

class SCPDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SCP基金会机密数据库")
        self.root.geometry("1200x800")
        
        # 初始化数据库文件
        self.db_file = "scp_database.json"
        self.log_file = "access_log.txt"
        self.initialize_files()
        
        # 记录访问IP
        self.log_access()
        
        # 创建Canvas主界面
        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绘制SCP风格界面
        self.draw_scp_interface()
        
        # 创建数据库操作控件
        self.create_widgets()

    def initialize_files(self):
        """初始化数据库和日志文件"""
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump({"scps": []}, f)
        
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write("SCP数据库访问日志\n")

    def log_access(self):
        """记录访问者IPv4地址和时间"""
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.log_file, 'a') as f:
                f.write(f"[{timestamp}] 访问IP: {ip}\n")
        except Exception as e:
            print(f"日志记录失败: {e}")

    def draw_scp_interface(self):
        """绘制SCP风格界面"""
        # 黑色背景
        self.canvas.create_rectangle(0, 0, 1200, 800, fill="black", outline="")
        
        # 红色边框
        self.canvas.create_rectangle(10, 10, 1190, 790, outline="#ff0000", width=5)
        
        # 标题
        self.canvas.create_text(600, 50, text="☣ SCP 机密数据库 ☣", 
                              fill="#ff0000", font=("Arial", 24, "bold"))
        
        # 装饰元素
        self.canvas.create_line(100, 100, 1100, 100, fill="#ff0000", width=2)
        self.canvas.create_line(100, 700, 1100, 700, fill="#ff0000", width=2)

    def create_widgets(self):
        """创建数据库操作控件"""
        # 主框架
        main_frame = tk.Frame(self.canvas, bg="black")
        self.canvas.create_window(600, 400, window=main_frame, width=1000, height=600)
        
        # SCP列表树状图
        self.tree = ttk.Treeview(main_frame, columns=('id', 'class', 'name'), show='headings')
        self.tree.heading('id', text='SCP编号')
        self.tree.heading('class', text='等级')
        self.tree.heading('name', text='名称')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 控制面板
        control_frame = tk.Frame(main_frame, bg="black")
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 按钮
        ttk.Button(control_frame, text="添加SCP", command=self.add_scp).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="查看详情", command=self.view_scp).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="删除SCP", command=self.delete_scp).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="刷新列表", command=self.load_data).pack(side=tk.LEFT, padx=5)
        
        # 搜索框
        search_frame = tk.Frame(control_frame, bg="black")
        search_frame.pack(side=tk.RIGHT, padx=5)
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="搜索", command=self.search_scp).pack(side=tk.LEFT)
        
        # 加载数据
        self.load_data()

    def load_data(self):
        """加载SCP数据"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            with open(self.db_file, 'r') as f:
                data = json.load(f)
                for scp in data['scps']:
                    self.tree.insert('', tk.END, values=(scp['scp_id'], scp['object_class'], scp['name']))
        except Exception as e:
            messagebox.showerror("错误", f"加载数据库失败: {e}")

    def add_scp(self):
        """添加新SCP"""
        add_window = tk.Toplevel(self.root)
        add_window.title("添加SCP条目")
        add_window.geometry("500x600")
        
        # 表单字段
        tk.Label(add_window, text="SCP编号 (如SCP-XXX):").pack(pady=5)
        scp_id_entry = ttk.Entry(add_window)
        scp_id_entry.pack(pady=5)
        
        tk.Label(add_window, text="等级:").pack(pady=5)
        class_entry = ttk.Combobox(add_window, values=["Safe", "Euclid", "Keter", "Thaumiel", "Neutralized"])
        class_entry.pack(pady=5)
        
        tk.Label(add_window, text="名称:").pack(pady=5)
        name_entry = ttk.Entry(add_window)
        name_entry.pack(pady=5)
        
        tk.Label(add_window, text="描述:").pack(pady=5)
        desc_text = tk.Text(add_window, height=10)
        desc_text.pack(pady=5)
        
        tk.Label(add_window, text="收容措施:").pack(pady=5)
        contain_text = tk.Text(add_window, height=10)
        contain_text.pack(pady=5)
        
        def submit():
            new_scp = {
                "scp_id": scp_id_entry.get(),
                "object_class": class_entry.get(),
                "name": name_entry.get(),
                "description": desc_text.get("1.0", tk.END).strip(),
                "containment_procedure": contain_text.get("1.0", tk.END).strip(),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            try:
                with open(self.db_file, 'r+') as f:
                    data = json.load(f)
                    data['scps'].append(new_scp)
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                
                messagebox.showinfo("成功", "SCP条目已添加")
                self.load_data()
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {e}")
        
        ttk.Button(add_window, text="提交", command=submit).pack(pady=10)

    def view_scp(self):
        """查看SCP详情"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("警告", "请先选择一个SCP条目")
            return
            
        scp_id = self.tree.item(selected)['values'][0]
        
        try:
            with open(self.db_file, 'r') as f:
                data = json.load(f)
                scp = next((s for s in data['scps'] if s['scp_id'] == scp_id), None)
                
                if scp:
                    detail_window = tk.Toplevel(self.root)
                    detail_window.title(f"SCP-{scp_id} 详情")
                    detail_window.geometry("800x600")
                    
                    notebook = ttk.Notebook(detail_window)
                    
                    # 基本信息标签页
                    info_frame = ttk.Frame(notebook)
                    notebook.add(info_frame, text="基本信息")
                    
                    ttk.Label(info_frame, text=f"SCP编号: {scp['scp_id']}", font=('Arial', 14, 'bold')).pack(pady=10)
                    ttk.Label(info_frame, text=f"等级: {scp['object_class']}").pack(pady=5)
                    ttk.Label(info_frame, text=f"名称: {scp['name']}").pack(pady=5)
                    ttk.Label(info_frame, text=f"创建时间: {scp['created_at']}").pack(pady=5)
                    
                    # 描述标签页
                    desc_frame = ttk.Frame(notebook)
                    notebook.add(desc_frame, text="描述")
                    
                    desc_text = tk.Text(desc_frame, wrap=tk.WORD)
                    desc_text.insert(tk.END, scp['description'])
                    desc_text.config(state=tk.DISABLED)
                    desc_scroll = ttk.Scrollbar(desc_frame, command=desc_text.yview)
                    desc_text['yscrollcommand'] = desc_scroll.set
                    desc_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    desc_scroll.pack(side=tk.RIGHT, fill=tk.Y)
                    
                    # 收容措施标签页
                    contain_frame = ttk.Frame(notebook)
                    notebook.add(contain_frame, text="收容措施")
                    
                    contain_text = tk.Text(contain_frame, wrap=tk.WORD)
                    contain_text.insert(tk.END, scp['containment_procedure'])
                    contain_text.config(state=tk.DISABLED)
                    contain_scroll = ttk.Scrollbar(contain_frame, command=contain_text.yview)
                    contain_text['yscrollcommand'] = contain_scroll.set
                    contain_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    contain_scroll.pack(side=tk.RIGHT, fill=tk.Y)
                    
                    notebook.pack(fill=tk.BOTH, expand=True)
                else:
                    messagebox.showerror("错误", "找不到指定的SCP条目")
        except Exception as e:
            messagebox.showerror("错误", f"读取数据失败: {e}")

    def delete_scp(self):
        """删除SCP条目"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("警告", "请先选择一个SCP条目")
            return
            
        scp_id = self.tree.item(selected)['values'][0]
        
        if messagebox.askyesno("确认", f"确定要删除SCP-{scp_id}吗？此操作不可恢复！"):
            try:
                with open(self.db_file, 'r+') as f:
                    data = json.load(f)
                    data['scps'] = [s for s in data['scps'] if s['scp_id'] != scp_id]
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                
                messagebox.showinfo("成功", "SCP条目已删除")
                self.load_data()
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {e}")

    def search_scp(self):
        """搜索SCP条目"""
        query = self.search_entry.get().lower()
        if not query:
            self.load_data()
            return
            
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            if any(query in str(v).lower() for v in values):
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
            else:
                self.tree.detach(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = SCPDatabaseApp(root)
    root.mainloop()