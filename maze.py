from random import randint
from termcolor import cprint

space = "\u2588"

class Cell:
  def __init__(self, row, col, height, width):
    self.isWall = [
      row != 0, # Above
      row != height - 1, # Below
      col != 0, # Left
      col != width - 1 # Right
    ]
    self.isVisited = False
    self.isStart = False
    self.isEnd = False
    self.whoami = [row, col]
    self.endNoShow = [
      True,
      True,
      True,
      True
    ]

  def Showing(self, height, width):
    return [
      self.whoami[0] != 0 and not self.isWall[0] and self.endNoShow[0],
      self.whoami[0] != height - 1 and not self.isWall[1] and self.endNoShow[1],
      self.whoami[1] != 0 and not self.isWall[2] and self.endNoShow[2],
      self.whoami[1] != width - 1 and not self.isWall[3] and self.endNoShow[3]
    ]

class Display:
  def __init__(self, value=" ", color="white"):
    self.value = value
    self.color = color

class Maze:
  def __init__(self, height, width, useColor):
    self.height = height
    self.width = width
    self.maze = []
    for i in range(self.height):
      ar = []
      for j in range(self.width):
        ar.append(Cell(i, j, self.height, self.width))
      self.maze.append(ar)
    self.max = self.height * self.width
    self.count = 0
    self.useColor = useColor

  def __Show(self):
    display = [[Display() for _ in range(self.width * 2 - 1)] for _ in range(self.height * 2 - 1)]
    for x in range(self.height):
      for y in range(self.width):
        if self.maze[x][y].isVisited:
          i = 2 * x
          j = 2 * y
          display[i][j].value = space
          directions = self.maze[x][y].Showing(self.height, self.width)
          if self.maze[x][y].isStart:
            display[i][j].color = "green"
          elif self.maze[x][y].isEnd:
            display[i][j].color="red"
          if directions[0]:
            display[i - 1][j].value = space
          if directions[1]:
            display[i + 1][j].value = space
          if directions[2]:
            display[i][j - 1].value = space
          if directions[3]:
            display[i][j + 1].value = space
    
    if self.useColor == "Y" or self.useColor == "y":
      for row in display:
        for item in row:
          cprint(item.value, item.color, end="")
        print()
    else:
      for row in display:
        for item in row:
          print(item.value, end="")
        print()

  def __GetDirections(self, row, col):
    new = []
    directions = self.maze[row][col].isWall
    for i in range(len(directions)):
      if directions[i]:
        if i == 0:
          if not self.maze[row - 1][col].isVisited:
            new.append(0)
        elif i == 1:
          if not self.maze[row + 1][col].isVisited:
            new.append(1)
        elif i == 2:
          if not self.maze[row][col - 1].isVisited:
            new.append(2)
        else:
          if not self.maze[row][col + 1].isVisited:
            new.append(3)
    return new

  def __Initialize(self, start, end):
    self.maze[start[0]][start[1]].isStart = True
    
    if not type(end) == list:
      end = [self.height - 1, self.width - 1]
    self.maze[end[0]][end[1]].isEnd = True
    self.maze[end[0]][end[1]].isVisited = True

    directions = self.__GetDirections(end[0], end[1])
    direction = directions[randint(0, len(directions) - 1)]
    for i in range(4):
      if not i == direction:
        self.maze[end[0]][end[1]].isWall[i] = False
        self.maze[end[0]][end[1]].endNoShow[i] = False

    return end

  def __RemoveWallIn(self, row, col, fro):
      if fro == 0:
        self.maze[row][col].isWall[1] = False
      elif fro == 1:
        self.maze[row][col].isWall[0] = False
      elif fro == 2:
        self.maze[row][col].isWall[3] = False
      else:
        self.maze[row][col].isWall[2] = False

  def __RemoveWallOut(self, row, col, go):
    self.maze[row][col].isWall[go] = False

  def __Create(self, row, col, fro=0):
    self.maze[row][col].isVisited = True
    self.count += 1
    if self.count < self.max:
      if fro:
        self.__RemoveWallIn(row, col, fro)
      directions = self.__GetDirections(row, col)
      while directions:
        direction = directions[randint(0, len(directions) - 1)]
        self.__RemoveWallOut(row, col, direction)
        if direction == 0:
          self.__Create(row - 1, col, direction)
        elif direction == 1:
          self.__Create(row + 1, col, direction)
        elif direction == 2:
          self.__Create(row, col - 1, direction)
        elif direction == 3:
          self.__Create(row, col + 1, direction)
        directions = self.__GetDirections(row, col)
      return
    self.__Show()
  
  def Generate(self, start=[0, 0], end=0):
    end = self.__Initialize(start, end)
    self.__Create(end[0], end[1])

if __name__ == '__main__':
  c = input("Does your terminal support colors? (Y/n): ")
  a = int(input("Number of rows: "))
  b = int(input("Number of columns: "))
  maze = Maze(a, b, c)
  maze.Generate()
