import tkinter as tk

from tkinter import messagebox, ttk, filedialog
from collections import deque
import math
import heapq

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bài tập lớn - Nhóm 1")
        self.root.geometry("1350x880")
        self.root.configure(bg="#f8f9fa")

        # Dữ liệu hệ thống
        self.nodes = []
        self.edges = []
        self.adj_list = {}
        self.node_pos = {}
        self.highlighted_edges = []
        self.highlight_color = "#dc3545"

        self.setup_ui()

    def setup_ui(self):
        # --- THANH MENU BÊN TRÁI ---
        sidebar = tk.Frame(self.root, width=400, bg="#ffffff", relief=tk.RIDGE, borderwidth=1, padx=15, pady=10)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(sidebar, text="CẤU HÌNH ĐỒ THỊ", font=("Arial", 12, "bold"), bg="#ffffff", fg="#333").pack(pady=(0, 5))
        
        self.graph_type = tk.StringVar(value="undirected")
        type_frame = tk.Frame(sidebar, bg="#ffffff")
        type_frame.pack(fill=tk.X, pady=2)
        tk.Radiobutton(type_frame, text="Vô hướng", variable=self.graph_type, value="undirected", bg="#ffffff", command=self.build_graph).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(type_frame, text="Có hướng", variable=self.graph_type, value="directed", bg="#ffffff", command=self.build_graph).pack(side=tk.LEFT, padx=10)

        tk.Label(sidebar, text="Số lượng đỉnh:", bg="#ffffff", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5,0))
        self.entry_nodes = tk.Entry(sidebar, font=("Arial", 10))
        self.entry_nodes.insert(0, "6")
        self.entry_nodes.pack(fill=tk.X, pady=2)

        tk.Label(sidebar, text="Danh sách cạnh (u v):", bg="#ffffff", font=("Arial", 9, "bold")).pack(anchor="w")
        self.text_edges = tk.Text(sidebar, height=8, font=("Consolas", 10))
        self.text_edges.insert("1.0", "1 2\n1 3\n2 3\n2 4\n3 4\n3 5\n4 5\n4 6\n5 6")
        self.text_edges.pack(fill=tk.X, pady=2)

        tk.Label(sidebar, text="PHẦN CƠ BẢN", font=("Arial", 11, "bold"), bg="#ffffff", fg="#007bff").pack(pady=(8, 3))
        
        btn_frame1 = tk.Frame(sidebar, bg="#ffffff")
        btn_frame1.pack(fill=tk.X, pady=2)
        tk.Button(btn_frame1, text="Vẽ Đồ Thị", command=self.build_graph, bg="#007bff", fg="white", font=("Arial", 9, "bold")).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        tk.Button(btn_frame1, text="Lưu Đồ Thị", command=self.save_graph, bg="#17a2b8", fg="white", font=("Arial", 9, "bold")).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        path_frame = tk.Frame(sidebar, bg="#ffffff")
        path_frame.pack(fill=tk.X, pady=4)
        tk.Label(path_frame, text="Tìm từ:", bg="#ffffff").pack(side=tk.LEFT)
        self.ent_s = tk.Entry(path_frame, width=4); self.ent_s.insert(0, "1"); self.ent_s.pack(side=tk.LEFT, padx=2)
        tk.Label(path_frame, text="đến:", bg="#ffffff").pack(side=tk.LEFT)
        self.ent_e = tk.Entry(path_frame, width=4); self.ent_e.insert(0, "6"); self.ent_e.pack(side=tk.LEFT, padx=2)
        tk.Button(path_frame, text="Dijkstra", command=self.run_dijkstra, bg="#fd7e14", fg="white", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        tk.Label(sidebar, text="PHẦN NÂNG CAO", font=("Arial", 11, "bold"), bg="#ffffff", fg="#28a745").pack(pady=(10, 3))
        
        grid_f = tk.Frame(sidebar, bg="#ffffff")
        grid_f.pack(fill=tk.X, pady=2)
        tk.Button(grid_f, text="Prim", command=self.run_prim, bg="#28a745", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        tk.Button(grid_f, text="Kruskal", command=self.run_kruskal, bg="#218838", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        tk.Button(grid_f, text="Ford-Fulkerson", command=self.run_ford_fulkerson, bg="#e83e8c", fg="white", font=("Arial", 9, "bold")).grid(row=1, column=0, columnspan=2, sticky="ew", padx=2, pady=2)
        tk.Button(grid_f, text="Fleury", command=self.run_fleury, bg="#6f42c1", fg="white", font=("Arial", 9, "bold")).grid(row=2, column=0, sticky="ew", padx=2, pady=2)
        tk.Button(grid_f, text="Hierholzer", command=self.run_hierholzer, bg="#6610f2", fg="white", font=("Arial", 9, "bold")).grid(row=2, column=1, sticky="ew", padx=2, pady=2)
        grid_f.columnconfigure(0, weight=1); grid_f.columnconfigure(1, weight=1)

        tk.Button(sidebar, text="LÀM MỚI", command=self.reset_ui, bg="#6c757d", fg="white", font=("Arial", 10, "bold")).pack(fill=tk.X, pady=(15, 0))

        # --- HIỂN THỊ ---
        main_area = tk.Frame(self.root, bg="#f8f9fa")
        main_area.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10)

        self.canvas = tk.Canvas(main_area, bg="white", highlightthickness=1)
        self.canvas.pack(expand=True, fill=tk.BOTH, pady=10)

        self.tabs = ttk.Notebook(main_area)
        self.tabs.pack(fill=tk.X, pady=(0, 10))

        self.res_txt = tk.Text(self.tabs, height=10, font=("Consolas", 10))
        self.matrix_txt = tk.Text(self.tabs, height=10, font=("Consolas", 10))
        self.adj_list_txt = tk.Text(self.tabs, height=10, font=("Consolas", 10))
        self.edges_txt = tk.Text(self.tabs, height=10, font=("Consolas", 10))

        self.tabs.add(self.res_txt, text=" Kết quả ")
        self.tabs.add(self.matrix_txt, text=" Ma trận kề ")
        self.tabs.add(self.adj_list_txt, text=" Danh sách kề ")
        self.tabs.add(self.edges_txt, text=" Danh sách cạnh ")

    def build_graph(self):
        try:
            n_str = self.entry_nodes.get().strip()
            if not n_str: return
            n = int(n_str)
            self.nodes = [str(i) for i in range(1, n + 1)]
            self.adj_list = {node: [] for node in self.nodes}
            self.edges = []
            self.highlighted_edges = []

            cx, cy, r = 400, 200, 150
            for i, node in enumerate(self.nodes):
                angle = 2 * math.pi * i / n
                self.node_pos[node] = (cx + r * math.cos(angle), cy + r * math.sin(angle))

            lines = self.text_edges.get("1.0", tk.END).strip().split('\n')
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    u, v = parts[0], parts[1]
                    w = 1  # Trọng số mặc định bằng 1 vì đã lược bỏ nhập liệu trọng số
                    if u in self.node_pos and v in self.node_pos:
                        self.edges.append((u, v, w))
                        self.adj_list[u].append((v, w))
                        if self.graph_type.get() == "undirected":
                            self.adj_list[v].append((u, w))

            self.draw_graph()
            self.run_basic_analysis()
            self.update_representations_tab()
        except Exception as e:
            messagebox.showerror("Lỗi", "Vui lòng kiểm tra lại định dạng nhập liệu")

    def draw_graph(self):
        self.canvas.delete("all")
        is_directed = (self.graph_type.get() == "directed")
        for u, v, w in self.edges:
            x1, y1 = self.node_pos[u]
            x2, y2 = self.node_pos[v]
            is_hl = (u, v) in self.highlighted_edges or (not is_directed and (v, u) in self.highlighted_edges)
            color = self.highlight_color if is_hl else "#adb5bd"
            width = 3 if is_hl else 1
            
            if is_directed:
                dx, dy = x2 - x1, y2 - y1
                l = math.sqrt(dx*dx + dy*dy)
                self.canvas.create_line(x1, y1, x2-(dx/l)*20, y2-(dy/l)*20, fill=color, width=width, arrow=tk.LAST)
            else:
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
            # Đã xóa dòng tạo text trọng số đè lên cạnh vẽ trên Canvas

        for node, (x, y) in self.node_pos.items():
            self.canvas.create_oval(x-18, y-18, x+18, y+18, fill="#ffc107", outline="#333")
            self.canvas.create_text(x, y, text=node, font=("Arial", 9, "bold"))

    def run_dijkstra(self):
        s, e = self.ent_s.get(), self.ent_e.get()
        if s not in self.nodes or e not in self.nodes: return
        pq = [(0, s, [])]
        visited = {}
        while pq:
            (cost, u, path) = heapq.heappop(pq)
            if u in visited: continue
            path = path + [u]
            visited[u] = cost
            if u == e:
                self.highlight_color = "#dc3545"
                self.highlighted_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
                self.draw_graph()
                self.res_txt.insert(tk.END, f"\n[Dijkstra] {s}->{e}: {'->'.join(path)} (Số cạnh đi qua: {cost})\n")
                return
            for v, w in self.adj_list[u]:
                if v not in visited: heapq.heappush(pq, (cost + w, v, path))

    def run_basic_analysis(self):
        self.res_txt.delete("1.0", tk.END)
        if not self.nodes: return
        start = self.nodes[0]
        v_bfs, q, seen = [], deque([start]), {start}
        while q:
            u = q.popleft(); v_bfs.append(u)
            for v, w in self.adj_list[u]:
                if v not in seen: seen.add(v); q.append(v)
        is_bi, colors = True, {}
        for n in self.nodes:
            if n not in colors:
                colors[n] = 0; q = deque([n])
                while q:
                    u = q.popleft()
                    for v, w in self.adj_list[u]:
                        if v not in colors: colors[v] = 1-colors[u]; q.append(v)
                        elif colors[v] == colors[u]: is_bi = False
        self.res_txt.insert(tk.END, f"BFS: {'->'.join(v_bfs)}\nHai phía: {'Có' if is_bi else 'Không'}\n")

    def update_representations_tab(self):
        self.matrix_txt.delete("1.0", tk.END)
        self.adj_list_txt.delete("1.0", tk.END)
        self.edges_txt.delete("1.0", tk.END)
        n = len(self.nodes)
        idx = {node: i for i, node in enumerate(self.nodes)}
        mat = [[0]*n for _ in range(n)]
        for u, v, w in self.edges:
            mat[idx[u]][idx[v]] = w
            if self.graph_type.get() == "undirected": mat[idx[v]][idx[u]] = w
        for row in mat: self.matrix_txt.insert(tk.END, str(row) + "\n")
        for u in self.nodes: self.adj_list_txt.insert(tk.END, f"{u}: {[v for v,w in self.adj_list[u]]}\n")
        for u, v, w in self.edges: self.edges_txt.insert(tk.END, f"{u}-{v}\n") # Đã xóa phần hiển thị trọng số ở đây

    def run_prim(self):
        if not self.nodes: return
        self.highlight_color = "#28a745"
        visited, self.highlighted_edges, total = {self.nodes[0]}, [], 0
        while len(visited) < len(self.nodes):
            best = None
            for u, v, w in self.edges:
                if (u in visited) != (v in visited):
                    if not best or w < best[2]: best = (u, v, w)
            if not best: break
            self.highlighted_edges.append((best[0], best[1]))
            visited.update([best[0], best[1]]); total += best[2]
        self.draw_graph()
        self.res_txt.insert(tk.END, f"[Prim] MST Edges Count: {total}\n")

    def run_kruskal(self):
        self.highlight_color = "#218838"
        parent = {n: n for n in self.nodes}
        def find(i): return i if parent[i] == i else find(parent[i])
        self.highlighted_edges, total = [], 0
        for u, v, w in sorted(self.edges, key=lambda x: x[2]):
            r1, r2 = find(u), find(v)
            if r1 != r2:
                parent[r1] = r2; self.highlighted_edges.append((u, v)); total += w
        self.draw_graph()
        self.res_txt.insert(tk.END, f"[Kruskal] MST Edges Count: {total}\n")

    def run_ford_fulkerson(self):
        if len(self.nodes) < 2: return
        s, t = self.nodes[0], self.nodes[-1]
        cap = {(u, v): w for u, v, w in self.edges}
        def bfs():
            p = {s: None}
            q = deque([s])
            while q:
                u = q.popleft()
                for (u_e, v_e), c in cap.items():
                    if u_e == u and v_e not in p and c > 0:
                        p[v_e] = u
                        if v_e == t: return p
                        q.append(v_e)
            return None
        max_f = 0
        while True:
            p = bfs()
            if not p: break
            f = float('inf')
            curr = t
            while curr != s:
                f = min(f, cap[(p[curr], curr)])
                curr = p[curr]
            max_f += f
            curr = t
            while curr != s:
                cap[(p[curr], curr)] -= f
                cap[(curr, p[curr])] = cap.get((curr, p[curr]), 0) + f
                curr = p[curr]
        self.res_txt.insert(tk.END, f"[Ford-Fulkerson] Luồng cực đại: {max_f}\n")

    def run_fleury(self):
        degs = [len(self.adj_list[u]) for u in self.nodes]
        odds = sum(1 for d in degs if d % 2 != 0)
        res = "Có chu trình" if odds == 0 else "Có đường đi" if odds == 2 else "Không có"
        self.res_txt.insert(tk.END, f"[Fleury] {res} Euler\n")

    def run_hierholzer(self):
        adj = {u: [v for v, w in self.adj_list[u]] for u in self.nodes}
        stack, path = [self.nodes[0]], []
        while stack:
            u = stack[-1]
            if adj[u]:
                v = adj[u].pop()
                if u in adj[v]: adj[v].remove(u)
                stack.append(v)
            else: path.append(stack.pop())
        self.res_txt.insert(tk.END, f"[Hierholzer] Path: {'->'.join(path[::-1])}\n")

    def save_graph(self):
        f = filedialog.asksaveasfilename(defaultextension=".txt")
        if f:
            with open(f, "w") as file:
                file.write(f"Type: {self.graph_type.get()}\nNodes: {len(self.nodes)}\n")
                for u, v, w in self.edges: file.write(f"{u} {v}\n") # Lưu dưới dạng chỉ có u v

    def reset_ui(self):
        self.canvas.delete("all")
        self.res_txt.delete("1.0", tk.END)
        self.nodes, self.edges, self.highlighted_edges = [], [], []

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()