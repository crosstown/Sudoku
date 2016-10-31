'''
Created on Sep 30, 2014

@author: Fernando Simon
'''
import sys
import numpy as np
from _ast import Num
from scipy.stats.vonmises_cython import numpy

def SolveSudoku(M):
    row = 0
    col = 0
    
    if (not FindUnassignedLocation(M, row, col)):
        return True
    for num in range(1, num <= 9):
        if (isSafe(M, row, col, num)):
            M[row][col] = num
            if (SolveSudoku(M)):
                return True
            M[row][col] = 0
            
    return False
 
def FindUnassignedLocation(M, row, col):
    for row in range(0, row < 9):
        for col in range(0, col < 9):
            if M[row][col] == 0:
                return True
def isSafe(M, row, col, num):
    
    return not UsedInRow(M, row, num) and not UsedInCol(M, col, num) and not UsedInBox(M, row - row % 3, col - col % 3, num)

def UsedInRow(M, row, num):
    for col in range(0, col < 9):
        if M[row][col] == num:
            return True    
    return False

def UsedInBox(M, boxStartRow, boxStartCol, num):
    for row in range(0, row < 3):
        for col in range (0, col < 3):
            if M[row + boxStartRow][col + boxStartCol] == num:
               return True
    return False

def UsedInCol(M, col, num):
    for row in range(0, col < 9):
        if M[row][col] == num:
            return True
    return False

def next_coordinate(row, col):
    """
    Returns the next coordinate to explore in a sudoku puzzle, regardless of
    whether or not the cell is actually empty. The order is left to right,
    top to bottom.
    """
    if col == 8:
        return row + 1, 0
    else:
        return row, col + 1

def solve(M, row=0, col=0):
    """
    Recursively solves a Sudoku puzzle starting at the given row and column.
    Note that two assumptions are made:
    
    1. All positions to the left and above of the starting position are filled
    2. All filled in cells are valid (no duplicates as in the Sudoku rules)

    Note that the second assumption does NOT imply that the puzzle is solvable.

    M - A numpy matrix representing a Sudoku board. Initially, cells with
        value 0 are considered empty, and cells with other values are
        considered fixed.
    row - the current row
    col - the current column
    """
    # Find the first empty cell from [row, col]. Stop if we pass the end of the
    # puzzle.
    while row < 9 and M[row, col] != 0:
        row, col = next_coordinate(row, col)

    # If we passed the last row (row 8) then we've solved the puzzle, so just
    # return true.
    if row == 9:
        return True

    # Otherwise, we need to do the standard guessing logic below:
    # Find forbidden values.
    F = set()

    # Find all values in the same column
    for k in range(9):
        F.add(M[row, k])

    # Find all values in the same row
    for k in range(9):
        F.add(M[k, col])

    # Slightly trickier, we also need the numbers in the 3x3 grid containing
    # the number. box_row and box_col are the row and column of the top left
    # cell in the current box.
    box_row = row - row % 3
    box_col = col - col % 3

    # Now check the 3x3 box starting at box_row, box_col
    for k in range(3):
        for l in range(3):
            F.add(M[box_row + k, box_col + l])

    # General idea (THIS IS THE PART YOU HAVE TO DO):
    # For the cell at location [row, col] consider all possible values between
    # 1 and 9 not creating a conflict with earlier values currently in M.
    # For every legal choice, check whether it leads to a solution by making a
    # recursive call.
    #
    # If a solution exists, the recursive call returns True and True is
    # returned (this means no further values need to be considered for cell
    # M[row, col].
    #
    # If no solution exists, the next possible value is tried. After all
    # possible values have been considered and none led to success, False is
    # returned.


    # We get to this statement if no possible assignment to M[row,col] led to
    # a solution. Set the cell back to empty and return False.
    value = 1
    while value < 10:
        if not value in F:
            M[row, col] = value
            nextRow, nextColumn = next_coordinate(row, col)
            if solve(M, nextRow, nextColumn):
                return True
        value = value+1
            
    M[row, col] = 0
    return False

def main():
    args = sys.argv[1:]
    if not args:
        print 'usage: argument_test.py [file path]'
        sys.exit(1)
    ''' If you will use one argument only'''
    filepath = args[0]
    print filepath
    fileopener = open(filepath)
    datalists = []
    data = fileopener.readlines()
    for row in data:
        datarow = row.replace('\n', '')
        datarow = datarow.replace(' ', '')
        datarow = datarow.replace('.', '0')
        datalists.append(list(datarow))
    print datalists
    dataarray = np.matrix(datalists, dtype=np.int)
    print dataarray
    print solve(dataarray)
    if (solve(dataarray) == True):
        print dataarray 
        file_name = 'solved_sudoku.txt'
        sys.stdout = open (file_name,'wt')
        print str(dataarray).replace(' ', '').replace('.', '').replace('[', '').replace(']', '')
      
    fileopener.close()
   
    

if __name__ == '__main__':
    main()
    pass
