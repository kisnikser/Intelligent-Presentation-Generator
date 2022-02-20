#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include "Python.h"
using namespace std;

int main()
{
	//Initialize the python instance
	Py_Initialize();

	//Run a simple file
	FILE* PScriptFile = fopen("test.py", "r");

	if (PScriptFile) {
		PyRun_SimpleFile(PScriptFile, "test.py");
		fclose(PScriptFile);
	}

	//Close the python instance
	Py_Finalize();
}