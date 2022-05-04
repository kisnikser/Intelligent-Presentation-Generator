#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <thread>

using namespace std;

int main(int argc, char* argv[])
{
    setlocale(LC_ALL, "rus"); // корректное отображение кириллицы

    if (argc == 1)
    {
        cout << "Error! (Not enough sections)";
        exit(-1);
    }

    ofstream presentation("presentation.tex");

    if (!presentation.is_open())
    {
        cout << "Error! (Presentation cannot be created)" << endl;
        exit(-2);
    }

    presentation << "\\documentclass{beamer}\n"        <<
                    "\\usepackage[T2A]{fontenc}\n"     <<
                    "\\usepackage[utf8]{inputenc}\n"   <<
                    "\\usetheme{Berlin}\n\n"           <<
                    "\\begin{document}\n\t"            <<
                    "\\input{frames.tex}\n"            <<
                    "\\end{document}";

    presentation.close();

    ofstream frames("frames.tex");

    if (!frames.is_open())
    {
        cout << "Error! (Frames cannot be created)" << endl;
        exit(-3);
    }

    for (int i = 1; i < argc; i++)
    {
        ifstream section(argv[i]);

        if (!section.is_open())
        {
            cout << "Error! (Section " << i << " cannot be read)" << endl;
            exit(-4);
        }

        char buffer[100000];
        section.getline(buffer, sizeof(buffer));
        
        frames << "\\begin{frame}\n\t" <<
                      buffer           <<
                  "\n\\end{frame}\n\n";

        section.close();
    }

    frames.close();
    system("pdflatex presentation.tex");
    system("mkdir latex");
    system("move presentation* latex");
    system("copy latex\\presentation.pdf presentation.pdf");
    system("move frames.tex latex");
    system("presentation.pdf");

    return 0;
}