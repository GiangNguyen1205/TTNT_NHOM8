import turtle  # Thư viện dùng để tạo đồ họa 2D cơ bản, vẽ các đối tượng trong chương trình.
import time    # Dùng để điều chỉnh tốc độ và tạo độ trễ (delay).
import sys     # Thư viện hệ thống, dùng để thoát chương trình.
from collections import deque  # Dùng deque để quản lý hàng đợi trong thuật toán BFS.

# Cài đặt cửa sổ đồ họa
wn = turtle.Screen()  # Tạo cửa sổ đồ họa.
wn.bgcolor("black")  # Đặt màu nền cửa sổ là đen.
wn.title("A BFS Maze Solving Program")  # Đặt tiêu đề cửa sổ.
wn.setup(1300, 700)  # Đặt kích thước cửa sổ đồ họa.

# Định nghĩa lớp Mê cung (Maze)
class Maze(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")  # Định dạng con trỏ hình vuông.
        self.color("white")   # Màu sắc của con trỏ là trắng.
        self.penup()          # Nhấc bút lên để không vẽ đường.
        self.speed(0)         # Tốc độ cao nhất.

# Định nghĩa lớp cho điểm kết thúc
class Green(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("green")  # Màu xanh lá cho điểm kết thúc.
        self.penup()
        self.speed(0)

# Định nghĩa lớp cho điểm bắt đầu
class Red(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")  # Màu đỏ cho điểm bắt đầu.
        self.penup()
        self.speed(0)

# Định nghĩa lớp cho đường đi cuối cùng
class Yellow(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("yellow")  # Màu vàng cho đường đi kết quả.
        self.penup()
        self.speed(0)

# Mê cung được thiết kế dưới dạng danh sách các chuỗi.
grid = [
    "+++++++++++++++++++++++++++++++++++++++++++++++++++",
    "+                       s                         +",
    "+  ++++++++++  +++++++++++++  +++++++  ++++++++++++",
    "+           +                 +               ++  +",
    "+  +++++++  +++++++++++++  ++++++++++  +++++++++  +",
    "+  +     +  +           +  +                 +++  +",
    "+  +  +  +  +  +  ++++  +  +  +++++++++++++  +++  +",
    "+  +  +  +  +  +  +        +  +  +        +       +",
    "+  +  ++++  +  ++++++++++  +  +  ++++  +  +  ++   +",
    "+  +     +  +          +   +           +  +  ++  ++",
    "+  ++++  +  +++++++ +++++ ++  +++++++++++++  ++  ++",
    "+     +  +     +              +              ++   +",
    "++++  +  ++++++++++ +++++++++++  ++++++++++  +++  +",
    "+  +  +                    +     +     +  +  +++  +",
    "+  +  ++++  +++++++++++++  +  ++++  +  +  +  ++   +",
    "+  +  +     +     +     +  +  +     +     +  ++  ++",
    "+  +  +  +++++++  ++++  +  +  +  ++++++++++  ++  ++",
    "+                       +  +  +              ++  ++",
    "+ ++++++             +  +  +  +  +++        +++  ++",
    "+ ++++++ ++++++ +++++++++    ++ ++   ++++++++++  ++",
    "+ +    +    +++ +     +++++++++ ++  +++++++    + ++",
    "+ ++++ ++++ +++ + +++ +++    ++    ++    ++ ++ + ++",
    "+ ++++    +     + +++ +++ ++ ++++++++ ++ ++ ++   ++",
    "+      ++ +++++++e+++     ++          ++    +++++++",
    "+++++++++++++++++++++++++++++++++++++++++++++++++++",
]

# Hàm thiết lập mê cung
def setup_maze(grid):
    global start_x, start_y, end_x, end_y  # Biến toàn cục để lưu tọa độ điểm bắt đầu và kết thúc.
    for y in range(len(grid)):  # Duyệt từng dòng của mê cung.
        for x in range(len(grid[y])):  # Duyệt từng ký tự trong dòng.
            character = grid[y][x]  # Lấy ký tự tại vị trí (x, y).
            screen_x = -588 + (x * 24)  # Tính tọa độ x trên màn hình.
            screen_y = 288 - (y * 24)  # Tính tọa độ y trên màn hình.

            if character == "+":  # Nếu là tường:
                maze.goto(screen_x, screen_y)  # Di chuyển con trỏ đến vị trí tương ứng.
                maze.stamp()  # Đóng dấu tường.
                walls.append((screen_x, screen_y))  # Lưu tọa độ vào danh sách walls.

            if character == " " or character == "e":  # Nếu là đường đi hoặc điểm kết thúc:
                path.append((screen_x, screen_y))  # Lưu vào danh sách path.

            if character == "e":  # Nếu là điểm kết thúc:
                green.color("purple")
                green.goto(screen_x, screen_y)  # Di chuyển đến điểm kết thúc.
                end_x, end_y = screen_x, screen_y  # Lưu tọa độ vào biến toàn cục.
                green.stamp()
                green.color("green")

            if character == "s":  # Nếu là điểm bắt đầu:
                start_x, start_y = screen_x, screen_y  # Lưu tọa độ vào biến toàn cục.
                red.goto(screen_x, screen_y)  # Đặt con trỏ đỏ tại điểm bắt đầu.

# Hàm tìm kiếm BFS
def search(x, y):
    frontier.append((x, y))  # Thêm điểm bắt đầu vào hàng đợi.
    solution[x, y] = x, y  # Ghi nhận điểm đầu tiên.

    while len(frontier) > 0:  # Lặp cho đến khi hàng đợi rỗng.
        x, y = frontier.popleft()  # Lấy phần tử đầu hàng đợi.

        # Kiểm tra các ô kề:
        for dx, dy in [(-24, 0), (0, -24), (24, 0), (0, 24)]:
            neighbor = (x + dx, y + dy)  # Tạo tọa độ ô liền kề từ vị trí hiện tại.
            if neighbor in path and neighbor not in visited:
                # Kiểm tra xem ô này có thuộc đường đi hợp lệ và chưa được thăm hay không.
                frontier.append(neighbor)  # Thêm ô liền kề vào hàng đợi để duyệt tiếp.
                solution[neighbor] = (x, y)  # Lưu lại đường đi theo cơ chế backtracking.
                visited.add(neighbor)  # Đánh dấu ô này đã được thăm.
                green.goto(neighbor)  # Di chuyển con trỏ xanh lá đến ô này.
                green.stamp()  # Đóng dấu để đánh dấu ô vừa duyệt.


# Hàm hiển thị đường đi cuối cùng
def backRoute(x, y):
    yellow.goto(x, y)  # Di chuyển con trỏ vàng đến tọa độ đích (kết thúc).
    yellow.stamp()  # Đánh dấu tọa độ đó bằng màu vàng.
    while (x, y) != (start_x, start_y):  # Lặp lại cho đến khi quay về điểm bắt đầu.
        yellow.goto(solution[x, y])  # Di chuyển đến tọa độ trước đó theo từ điển `solution`.
        yellow.stamp()  # Đánh dấu ô này bằng màu vàng.
        x, y = solution[x, y]  # Cập nhật vị trí hiện tại để quay ngược lại đường đi.
# Khởi tạo các lớp và danh sách:
maze = Maze()  # Tạo đối tượng mê cung.
red = Red()  # Tạo đối tượng biểu diễn điểm bắt đầu.
green = Green()  # Tạo đối tượng biểu diễn điểm kết thúc.
yellow = Yellow()  # Tạo đối tượng biểu diễn đường đi cuối cùng.

walls = []  # Danh sách lưu tọa độ của các bức tường trong mê cung.
path = []  # Danh sách lưu tọa độ của các ô đường đi hợp lệ.
visited = set()  # Tập hợp các ô đã được thăm.
frontier = deque()  # Hàng đợi dùng cho thuật toán BFS.
solution = {}  # Từ điển để lưu thông tin đường đi (backtracking).


# Chương trình chính:
setup_maze(grid)  # Thiết lập mê cung bằng cách đọc lưới (grid) và phân loại tường, đường đi.
search(start_x, start_y)  # Tìm kiếm đường đi từ điểm bắt đầu đến điểm kết thúc bằng BFS.
backRoute(end_x, end_y)  # Hiển thị đường đi cuối cùng từ điểm kết thúc quay về điểm bắt đầu.
wn.exitonclick()  # Chờ người dùng nhấp chuột để đóng cửa sổ đồ họa.

