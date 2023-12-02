import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x400")
        self.master.iconbitmap('icon/snakegame.ico')

        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack()

        self.score = 0
        self.score_display = self.canvas.create_text(380, 10, text=f"Score: {self.score}", fill="white", anchor="e")

        self.initial_message = self.canvas.create_text(200, 200, text="Press Space key to Start...", fill="white", font=("Helvetica", 16), tags="initial_message")

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.food = self.create_food()

        self.game_running = False
        self.paused = False
        self.master.bind("<Key>", self.handle_key)

    def create_food(self):
        x = random.randint(1, 39) * 10
        y = random.randint(1, 39) * 10
        food = self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="red")
        return food

    def handle_key(self, event):
        if event.keysym == "space":
            if not self.game_running:
                self.reset_game()
            else:
                self.toggle_pause()

        if self.game_running and not self.paused:
            self.change_direction(event)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.canvas.create_text(200, 200, text="Press Space to Continue...", fill="white", font=("Helvetica", 16), tags="paused_text")
        else:
            self.canvas.delete("paused_text")
            self.update()

    def reset_game(self):
        self.canvas.delete("initial_message")
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.score = 0
        self.canvas.itemconfig(self.score_display, text=f"Score: {self.score}")
        self.canvas.delete("game_over_text")
        self.game_running = True
        self.paused = False
        self.update()

    def change_direction(self, event):
        key = event.keysym
        if (key == "Up" and self.direction != "Down") or \
           (key == "Down" and self.direction != "Up") or \
           (key == "Left" and self.direction != "Right") or \
           (key == "Right" and self.direction != "Left"):
            self.direction = key

    def move_snake(self):
        head = self.snake[0]
        if self.direction == "Up":
            new_head = (head[0], head[1] - 10)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 10)
        elif self.direction == "Left":
            new_head = (head[0] - 10, head[1])
        elif self.direction == "Right":
            new_head = (head[0] + 10, head[1])

        self.snake = [new_head] + self.snake[:-1]

        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill="green", tags="snake")

    def check_collision(self):
        head = self.snake[0]
        if head[0] < 0 or head[0] >= 400 or head[1] < 0 or head[1] >= 400:
            return True  

        for segment in self.snake[1:]:
            if head == segment:
                return True  

        return False

    def check_food(self):
        head = self.snake[0]
        food_coords = self.canvas.coords(self.food)
        if head == (food_coords[0], food_coords[1]):
            self.snake.append((0, 0))  
            self.canvas.delete(self.food)
            self.food = self.create_food()
            self.score += 1
            self.canvas.itemconfig(self.score_display, text=f"Score: {self.score}")

    def update(self):
        if self.game_running and not self.paused:
            self.move_snake()
            if self.check_collision():
                self.show_game_over()
            else:
                self.check_food()
                self.master.after(100, self.update)

    def show_game_over(self):
        self.canvas.create_text(200, 200, text=f"Game Over\nScore: {self.score}", fill="white", font=("Helvetica", 16), tags="game_over_text")
        self.canvas.create_text(200, 280, text="Press Space bar to play again!", fill="white", font=("Helvetica", 12), tags="game_over_text")
        self.game_running = False

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()