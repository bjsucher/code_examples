#ifndef MAZE_H
#define MAZE_H

enum CellValue { OPEN, BLOCKED, PATH, EXIT, TEMPORARY, LEFT, RIGHT, UP, DOWN, IN, OUT };
#include "MazeInterface.h"
#include <iostream>
#include <string>
#include <sstream>
using namespace std;

class Maze : public MazeInterface
{
private:
	int ***mazeArray;
	int mazeRow;
	int mazeColumn;
	int mazeLayer;
public:
	Maze(int height, int width, int length);
	~Maze(void);

	/** Set maze value
	@parm height
	@parm width
	@parm layer
	@parm value
	*/
	void setValue(int height, int width, int length, int value);

	/** Solve maze
	@return true if solveable, else false
	*/
	bool find_maze_path();
	bool find_maze_path(int height, int width, int length);

	/** Output maze (same order as input maze)
	@return string of 2D layers
	*/
	string toString() const;
};
#endif // MAZE_H
