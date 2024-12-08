import pygame
import random
import networkx as nx

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Graph with Movable Nodes")

# Tạo đồ thị vô hướng
G = nx.Graph()

# Số lượng đỉnh ngẫu nhiên từ 6 đến 7
num_nodes = random.randint(6, 7)

# Thêm các đỉnh vào đồ thị
G.add_nodes_from(range(1, num_nodes + 1))

# Tạo cây bằng cách đảm bảo liên thông
# Thêm các cạnh sao cho đồ thị là cây (có số lượng cạnh = num_nodes - 1)
for i in range(1, num_nodes):
    u = random.randint(1, i)
    v = i + 1
    G.add_edge(u, v)

# Tiếp tục thêm các cạnh ngẫu nhiên sao cho không tạo chu trình
edge_seen = set((u, v) if u < v else (v, u) for u, v in G.edges())
max_edges = ((num_nodes - 1) * (num_nodes - 2)) // 2  # Số cạnh tối đa theo công thức mới
while len(edge_seen) < max_edges:
    u = random.randint(1, num_nodes)
    v = random.randint(1, num_nodes)
    
    # Đảm bảo u != v và không tạo chu trình
    if u != v and (u, v) not in edge_seen and (v, u) not in edge_seen:
        G.add_edge(u, v)
        edge_seen.add((u, v))

# Thêm trọng số ngẫu nhiên cho các cạnh (từ 1 đến 9)
for u, v in G.edges():
    weight = random.randint(1, 9)  # Trọng số ngẫu nhiên từ 1 đến 9
    G[u][v]['weight'] = weight

# Vị trí ban đầu của các đỉnh
pos = {i: [random.randint(50, screen_width - 50), random.randint(50, screen_height - 50)] for i in G.nodes()}

# Kích thước đỉnh
node_radius = 20

# Màu sắc
node_color = (100, 200, 255)
edge_color = (200, 200, 200)
font = pygame.font.SysFont("Arial", 20)

# Hàm vẽ đồ thị
def draw_graph():
    # Vẽ các cạnh
    for u, v in G.edges():
        pygame.draw.line(screen, edge_color, pos[u], pos[v], 2)

    # Vẽ các đỉnh và nhãn
    for node in G.nodes():
        pygame.draw.circle(screen, node_color, pos[node], node_radius)
        label = font.render(str(node), True, (0, 0, 0))
        screen.blit(label, (pos[node][0] - label.get_width() // 2, pos[node][1] - label.get_height() // 2))

    # Hiển thị trọng số cạnh
    for u, v in G.edges():
        weight = G[u][v]['weight']
        mid_point = [(pos[u][0] + pos[v][0]) // 2, (pos[u][1] + pos[v][1]) // 2]
        weight_text = font.render(str(weight), True, (0, 0, 0))
        screen.blit(weight_text, (mid_point[0] - weight_text.get_width() // 2, mid_point[1] - weight_text.get_height() // 2))

# Xử lý sự kiện
dragging = None
drag_offset = [0, 0]

running = True
while running:
    screen.fill((255, 255, 255))  # Màu nền trắng

    # Vẽ đồ thị
    draw_graph()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra xem có nhấp vào một đỉnh không
            for node, (x, y) in pos.items():
                if (event.pos[0] - x) ** 2 + (event.pos[1] - y) ** 2 <= node_radius ** 2:
                    dragging = node
                    drag_offset = [x - event.pos[0], y - event.pos[1]]
                    break
        
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = None

        if event.type == pygame.MOUSEMOTION:
            if dragging is not None:
                pos[dragging] = [event.pos[0] + drag_offset[0], event.pos[1] + drag_offset[1]]

    pygame.display.flip()  # Cập nhật màn hình

pygame.quit()
