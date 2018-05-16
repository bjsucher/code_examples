#include "Maze.h"
#include <iostream>
#include <string>
#include <fstream>
using namespace std;

// Check for memory leaks
#ifdef _MSC_VER
#define _CRTDBG_MAP_ALLOC 
#include <crtdbg.h>
#define VS_MEM_CHECK _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#else
#define VS_MEM_CHECK;
#endif

// Main function where the file is read in and output is created.

int main(int argc, char * argv[])
{

	VS_MEM_CHECK;

	// Check to see if input and output files are valid
	if (argc < 3)
	{
		cout << "Please provide name of input and output files" << endl;
		return 1;
	}
	cout << "Input file: " << argv[1] << endl;
	ifstream in(argv[1]);
	if (!in)
	{
		cout << "Unable to open " << argv[1] << " for input" << endl;
		return 1;
	}
	cout << "Output file: " << argv[2] << endl;
	ofstream out(argv[2]);
	if (!out)
	{
		in.close();
		cout << "Unable to open " << argv[2] << " for output" << endl;
	}

	int mazeLayer; 
	int mazeColumn;
	int mazeRow;

	// Read in the number of rows, columns, and layers
	in >> mazeRow >> mazeColumn >> mazeLayer;	

	Maze* myMaze = new Maze(mazeRow, mazeColumn, mazeLayer);

	// Read in the input values and send them to the Set Value function
	for (int i = 0; i < mazeLayer; ++i)
	{
		for (int j = 0; j < mazeRow; ++j)
		{
			for (int k = 0; k < mazeColumn; ++k)
			{
				int input;
				in >> input;
				myMaze->setValue(i, j, k, input);
			}
		}
	}

	// Read out the layers with underscores and X's
	out << "Solve Maze:" << endl;
	out << myMaze->toString() << endl;

	// Find a solution path if there is one
	if (myMaze->find_maze_path() == true)
	{
		out << "Solution:" << endl;
		out << myMaze->toString() << endl;
	}
	else out << "No Solution Exists!" << endl;

	// Delete Maze pointer in the main
	delete myMaze;

	return 0;
}
