#include "Maze.h"

// Create 3-dimensional array of layers, rows, and columns
Maze::Maze(int row, int column, int layer)
{
	mazeRow = row;
	mazeColumn = column;
	mazeLayer = layer;
	mazeArray = new int**[mazeLayer];
	for (int i = 0; i < mazeLayer; ++i)
	{
		mazeArray[i] = new int*[mazeRow];
		for (int j = 0; j < mazeRow; ++j)
		{
			mazeArray[i][j] = new int[mazeColumn];
		}
	}
}

// Free memory
Maze::~Maze(void) 
{
	for (int i = 0; i < mazeLayer; ++i)
	{
		for (int j = 0; j < mazeRow; ++j)
		{
			delete[] mazeArray[i][j];
		}
		delete[] mazeArray[i];
	}
	delete[] mazeArray;
}

/** Set maze value
@parm height
@parm width
@parm layer
@parm value
*/
void Maze::setValue(int layer, int row, int column, int value)
{
	mazeArray[layer][row][column] = value;
}

/** Solve maze
@return true if solveable, else false
*/
// Wrapper function
bool Maze::find_maze_path()
{
	return find_maze_path(0, 0, 0);
}

// Recursive function
bool Maze::find_maze_path(int row, int column, int layer)
{
	if (row < 0 || column < 0 || layer < 0 || row >= mazeRow || column >= mazeColumn ||
		layer >= mazeLayer) return false;
	else if (mazeArray[layer][row][column] != OPEN) return false;
	else if (row == mazeRow - 1 && column == mazeColumn - 1 && layer == mazeLayer - 1)
	{
		mazeArray[layer][row][column] = EXIT;
		return true;
	}
	// Changes values for location in the maze based on which path taken in the maze
	else
	{
		mazeArray[layer][row][column] = PATH;
		if (find_maze_path(row - 1, column, layer))
		{
			mazeArray[layer][row][column] = UP;
			return true;
		}
		else if (find_maze_path(row + 1, column, layer))
		{
			mazeArray[layer][row][column] = DOWN;
			return true;
		}
		else if (find_maze_path(row, column - 1, layer))
		{
			mazeArray[layer][row][column] = LEFT;
			return true;
		}
		else if (find_maze_path(row, column + 1, layer))
		{
			mazeArray[layer][row][column] = RIGHT;
			return true;
		}
		else if (find_maze_path(row, column, layer - 1))
		{
			mazeArray[layer][row][column] = OUT;
			return true;
		}
		else if (find_maze_path(row, column, layer + 1))
		{
			mazeArray[layer][row][column] = IN;
			return true;
		}

		else
		{
			mazeArray[layer][row][column] = TEMPORARY;
			return false;
		}
	}
}

/** Output maze (same order as input maze)
@return string of 2D layers
*/
string Maze::toString() const
{
	ostringstream out;
	for (int layer = 0; layer < mazeLayer; ++layer)
	{
		out << "Layer " << layer + 1 << endl;
		for (int row = 0; row < mazeRow; ++row)
		{
			for (int column = 0; column < mazeColumn; ++column)
			{
				if (mazeArray[layer][row][column] == OPEN || 
					mazeArray[layer][row][column] == TEMPORARY) out << "_ ";
				else if (mazeArray[layer][row][column] == BLOCKED) out << "X ";
				else if (mazeArray[layer][row][column] == LEFT) out << "L ";
				else if (mazeArray[layer][row][column] == RIGHT) out << "R ";
				else if (mazeArray[layer][row][column] == UP) out << "U ";
				else if (mazeArray[layer][row][column] == DOWN) out << "D ";
				else if (mazeArray[layer][row][column] == IN) out << "I ";
				else if (mazeArray[layer][row][column] == OUT) out << "O ";
				else if (mazeArray[layer][row][column] == EXIT) out << "E ";
				else out << mazeArray[layer][row][column] << " ";
			}
			out << endl;
		}
	}
	return out.str();
}