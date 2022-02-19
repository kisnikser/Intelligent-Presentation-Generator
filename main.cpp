#include "headers.h"

int main(){
    setlocale(LC_ALL, "ru");

    std::ofstream sections;

    sections.open("./latex/sections.tex");

    if (!sections.is_open()){
        std::cout << "Ошибка открытия файла!" << std::endl;
        exit(1);
    }

    std::ofstream section_1;

    section_1.open("./latex/section_1.tex");

    if (!section_1.is_open()){
        std::cout << "Ошибка открытия файла!" << std::endl;
        exit(2);
    }

    sections << "\\begin{frame}" << std::endl << "\\input{section_1.tex}" << std::endl << "\\end{frame}" << std::endl;

    section_1 << "Hello, world!" << std::endl;

    sections.close();
    section_1.close();

    return 0;
}