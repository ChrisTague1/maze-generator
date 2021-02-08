from random import randint

space = "\u2588"

class Cell:
  def __init__(self, row, col, height, width):
    self.wallAbove = row != 0
    self.wallBelow = row != height - 1
    self.wallLeft = col != 0
    self.wallRight = col != width - 1
    self.visited = False
    self.whoami = [row, col]
  
  def directions(self):
    available = []
    if self.wallAbove:
      available.append("above")
    if self.wallBelow:
      available.append("below")
    if self.wallLeft:
      available.append("left")
    if self.wallRight:
      available.append("right")
    
    return available

class Maze:
  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.maze = []
    for i in range(self.height):
      arr = []
      for j in range(self.width):
        arr.append(Cell(i, j, self.height, self.width))
      self.maze.append(arr)
    self.dir = {
      "above": -1,
      "below": 1,
      "right": 1,
      "left": -1
    }
    self.max = self.height * self.width
    self.count = 0
    self.bandaid = []
  
  def Show(self, maze):
    display = []
    for i in range(self.height * 2 - 1):
      arr = []
      for j in range(self.width * 2 - 1):
        if i % 2 == 0 and j % 2 == 0:
          arr.append(space)
        else:
          arr.append(" ")
      display.append(arr)
    
    for i, row in enumerate(maze):
      for j, cell in enumerate(row):
        if not cell.wallAbove:
          if i != 0:
            display[i * 2 - 1][j * 2] = space
        if not cell.wallBelow:
          if i != self.height - 1:
            display[i * 2 + 1][j * 2] = space
        if not cell.wallLeft:
          if j != 0:
            display[i * 2][j * 2 - 1] = space
        if not cell.wallRight:
          if j != self.width - 1:
            display[i * 2][j * 2 + 1] = space
    
    for i in display:
      for j in i:
        print(j, end = "")
      print()

  def Remove_Wall_In(self, row, col, fro):
    if fro == "above":
      self.maze[row][col].wallBelow = False
    elif fro == "below":
      self.maze[row][col].wallAbove = False
    elif fro == "left":
      self.maze[row][col].wallRight = False
    elif fro == "right":
      self.maze[row][col].wallLeft = False
  
  def Remove_Wall_Out(self, row, col, go):
    if go == "above":
      self.maze[row][col].wallAbove = False
    elif go == "below":
      self.maze[row][col].wallBelow = False
    elif go == "left":
      self.maze[row][col].wallLeft = False
    elif go == "right":
      self.maze[row][col].wallRight = False

  def Get_Directions(self, row, col):
    directions = self.maze[row][col].directions()
    new_directions = []
    if directions:
      for direction in directions:
        if direction == "above" or direction == "below":
          if not self.maze[row + self.dir[direction]][col].visited:
            new_directions.append(direction)
        elif direction == "left" or direction == "right":
          if not self.maze[row][col + self.dir[direction]].visited:
            new_directions.append(direction)
    return new_directions
  
  def Create(self, row=0, col=0, fro=0):
    self.count += 1
    if not (self.count >= self.max):
      self.maze[row][col].visited = True
      if fro:
        self.Remove_Wall_In(row, col, fro)
      valid_directions = self.Get_Directions(row, col)
      while valid_directions:
        valid_directions = self.Get_Directions(row, col)
        if valid_directions:
          direction = valid_directions[randint(0, len(valid_directions) - 1)]
          self.Remove_Wall_Out(row, col, direction)
          if direction == "above" or direction == "below":
            self.Create(row + self.dir[direction], col, direction)
          elif direction == "left" or direction == "right":
            self.Create(row, col + self.dir[direction], direction)
      return
    self.bandaid.append(self.maze)
    return

  def Generate(self, row=0, col=0):
    self.Create(row, col)
    self.Show(self.bandaid[0])
  
if __name__ == '__main__':
    x = int(input("Rows: "))
    y = int(input("Columns: "))
    maze = Maze(x, y)
    maze.Generate()
  
