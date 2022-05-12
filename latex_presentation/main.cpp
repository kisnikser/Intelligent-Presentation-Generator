#include <iostream>
#include <fstream>
#include <string>
#include <Windows.h>

using namespace std;

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

    ofstream document("document.tex");

    if (!document.is_open())
    {
        cout << "Error! (Document cannot be created)" << endl;
        exit(-3);
    }

    document << "\\documentclass[12pt, a4paper]{extarticle}\n"     <<
                "\\usepackage[T2A]{fontenc}\n"   <<
                "\\usepackage[utf8]{inputenc}\n" <<
                "\\usepackage{indentfirst}\n"    <<
                "\\usepackage{extsizes}\n"       <<
                "\\usepackage[top = 20mm, bottom = 20mm, left = 20mm, right = 20mm]{geometry}\n"       <<
                "\\setlength\\parindent{5ex}"    <<
                "\\linespread{1.3}"              <<
                "\\frenchspacing"                <<
                "\\pagestyle{empty}"             <<
                "\\begin{document}\n\t"          <<
                "\\input{sections.tex}\n"        <<
                "\\end{document}";

    document.close();

    ofstream frames("frames.tex");

    if (!frames.is_open())
    {
        cout << "Error! (Frames cannot be created)" << endl;
        exit(-4);
    }

    ofstream sections("sections.tex");

    if (!sections.is_open())
    {
        cout << "Error! (Sections cannot be created)" << endl;
        exit(-5);
    }

    ifstream keywords("keywords.txt");

    if (!keywords.is_open())
    {
        cout << "Error! (Keywords cannot be read)" << endl;
        exit(-6);
    }

    for (int i = 1; i < argc; i++)
    {
        ifstream section(argv[i]);

        if (!section.is_open())
        {
            cout << "Error! (Section " << i - 1 << " cannot be read)" << endl;
            exit(-4);
        }

        char buffer_1[100000];
        section.getline(buffer_1, sizeof(buffer_1));

        char buffer_2[1000];
        keywords.getline(buffer_2, sizeof(buffer_2));
        
        sections << "\\subsection*{" << buffer_2 << "}\n\t" <<
                      buffer_1 << "\n\n";

        frames << "\\begin{frame}{" << buffer_2 << "}\n\t"     <<
                  "\\begin{figure}[h!]\n\t" <<
                  "\\centering\n\t" <<
                  "\\includegraphics[width = 0.8\\textwidth]{image_" << i - 1 << "}\n" <<
                  "\\end{figure}" <<
                  "\n\\end{frame}\n\n";

        section.close();
    }

    sections.close();
    frames.close();
    system("pdflatex presentation.tex");
    system("pdflatex document.tex");
    system("mkdir latex");
    system("move presentation* latex");
    system("move document* latex");
    system("move frames.tex latex");
    system("move sections.tex latex");
    system("copy latex\\presentation.pdf presentation.pdf");
    system("copy latex\\document.pdf document.pdf");
    system("presentation.pdf");

    return 0;
}