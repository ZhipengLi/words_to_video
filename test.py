from typing import List
class BIT:
    def __init__(self, matrix):
        m,n = len(matrix), len(matrix[0])
        self.BIT_tree = [[0]*(n+1)]*(m+1)
        self.m = m
        self.n = n
        for i in range(m):
            for j in range(n):
                self.update(matrix[i][j], i,j)
        for i in range(m+1):
            print(self.BIT_tree[i])
    def update(self, val, x, y)->None:
        print("x,y,val", x, y,val)
        x+=1
        y+=1
        origin_y = y
        while x<=self.m:
            y = origin_y
            while y<=self.n:
                self.BIT_tree[x][y] += val
                y+=self.get_low(y)
            x+=self.get_low(x)            
    def get_sum(self, x, y)->int:
        x+=1
        y+=1
        origin_y = y
        res = 0
        while x>0:
            y = origin_y
            while y>0:
                res+=self.BIT_tree[x][y]
                y-=self.get_low(y)
            x-=self.get_low(x)
        return res
    def get_low(self, num)-> int:
        return num & -num
class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        self.BIT_tree =  BIT(matrix)
        self.matrix = matrix
    def update(self, row: int, col: int, val: int) -> None:
        self.BIT_tree.update(val-self.matrix[row][col], row, col)
        self.matrix[row][col] = val
    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return self.BIT_tree.get_sum(row2, col2) \
                    -self.BIT_tree.get_sum(row1-1, col2) \
                    -self.BIT_tree.get_sum(row2, col1-1) \
                    +self.BIT_tree.get_sum(row1-1, col1-1)

matrix = NumMatrix([[3,0,1,4,2],[5,6,3,2,1],[1,2,0,1,5],[4,1,0,1,7],[1,0,3,0,5]])