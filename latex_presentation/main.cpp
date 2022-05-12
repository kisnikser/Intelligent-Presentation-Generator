#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <thread>
#include <Windows.h>
#include <charconv>

using namespace std;

std::wstring s2ws(const std::string& str)
{
    int size_needed = MultiByteToWideChar(CP_UTF8, 0, &str[0], (int)str.size(), NULL, 0);
    std::wstring wstrTo( size_needed, 0 );
    MultiByteToWideChar(CP_UTF8, 0, &str[0], (int)str.size(), &wstrTo[0], size_needed);
    return wstrTo;
}

int main(int argc, char* argv[])
{
    setlocale(LC_ALL, "rus"); // корректное отображение кириллицы

    if (argc == 1)
    {
        cout << "Error! (Not enough arguments)";
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
                    "\\graphicspath{{../topic_modelling/images}}\n"   <<
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

    int count = stoi(argv[1]);
    cout << count << endl;

    for (int i = 2; i <= count + 1; i++)
    {
        ifstream section(argv[i]);
        string title = argv[i + count];
        string number = to_string(i - 2);

        if (!section.is_open())
        {
            cout << "Error! (Section " << i - 2 << " cannot be read)" << endl;
            exit(-4);
        }

        /*char buffer[100000];
        section.getline(buffer, sizeof(buffer));
        
        frames << "\\begin{frame}\n\t" <<
                      buffer           <<
                  "\n\\end{frame}\n\n";*/

        frames << "\\begin{frame}{" << title << "}\n\t"     <<
                  "\\begin{figure}[h!]\n\t" <<
                  "\\centering\n\t" <<
                  "\\includegraphics[scale = 0.2]{image_" << number << "}\n" <<
                  "\\end{figure}" <<
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