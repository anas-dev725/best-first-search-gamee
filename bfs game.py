import pygame
import time
import heapq

# Initialize
pygame.init()

ROWS, COLS = 10, 10
TILE_SIZE = 60
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE + 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Best First Search - Dot Path")

# Colors
BG = (30, 30, 30)
WALL = (70, 70, 70)
DOT_VISITED = (150, 100, 255)
DOT_PATH = (50, 220, 50)
DOT_CURRENT = (255, 255, 0)
START_COLOR = (0, 170, 255)
GOAL_COLOR = (255, 80, 80)
TEXT = (255, 255, 255)

font = pygame.font.SysFont("consolas", 24)

maze = [
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
]

start = (0, 0)
goal = (9, 9)

def draw_dots(visited, path, current=None, status="", steps=0, visited_count=0):
    screen.fill(BG)

    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == 1:
                pygame.draw.rect(screen, WALL, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw visited
    for node in visited:
        x = node[1] * TILE_SIZE + TILE_SIZE // 2
        y = node[0] * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, DOT_VISITED, (x, y), 5)

    # Draw final path
    for node in path:
        x = node[1] * TILE_SIZE + TILE_SIZE // 2
        y = node[0] * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, DOT_PATH, (x, y), 6)

    # Current moving dot
    if current:
        x = current[1] * TILE_SIZE + TILE_SIZE // 2
        y = current[0] * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, DOT_CURRENT, (x, y), 7)

    # Start and goal
    sx = start[1] * TILE_SIZE + TILE_SIZE // 2
    sy = start[0] * TILE_SIZE + TILE_SIZE // 2
    gx = goal[1] * TILE_SIZE + TILE_SIZE // 2
    gy = goal[0] * TILE_SIZE + TILE_SIZE // 2
    pygame.draw.circle(screen, START_COLOR, (sx, sy), 9)
    pygame.draw.circle(screen, GOAL_COLOR, (gx, gy), 9)

    # Bottom info bar
    pygame.draw.rect(screen, BG, (0, HEIGHT - 100, WIDTH, 100))
    screen.blit(font.render(f"Status: {status}", True, TEXT), (10, HEIGHT - 90))
    screen.blit(font.render(f"Steps: {steps}", True, TEXT), (10, HEIGHT - 60))
    screen.blit(font.render(f"Visited: {visited_count}", True, TEXT), (10, HEIGHT - 30))

    pygame.display.update()

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def best_first_search_with_dots():
    visited = set()
    queue = []
    came_from = {}
    heapq.heappush(queue, (heuristic(start, goal), start))
    steps = 0

    draw_dots(visited, [], None, "Starting...", steps, 0)
    time.sleep(1)

    while queue:
        _, current = heapq.heappop(queue)
        if current == goal:
            break

        visited.add(current)
        steps += 1
        row, col = current

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            r, c = row + dr, col + dc
            neighbor = (r, c)
            if 0 <= r < ROWS and 0 <= c < COLS and maze[r][c] == 0 and neighbor not in visited:
                if neighbor not in [item[1] for item in queue]:
                    heapq.heappush(queue, (heuristic(neighbor, goal), neighbor))
                    came_from[neighbor] = current

        draw_dots(visited, [], current, "Exploring...", steps, len(visited))
        time.sleep(0.05)

    # Reconstruct path
    path = []
    curr = goal
    while curr != start:
        path.append(curr)
        curr = came_from.get(curr)
        if curr is None:
            draw_dots(visited, [], None, "No Path Found", steps, len(visited))
            return
    path.append(start)
    path.reverse()

    # Animate moving dot on path
    for node in path:
        draw_dots(visited, path, node, "Path Found!", steps, len(visited))
        time.sleep(0.08)

    draw_dots(visited, path, None, "Path Complete!", steps, len(visited))
    time.sleep(3)

def main():
    running = True
    best_first_search_with_dots()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

main()
