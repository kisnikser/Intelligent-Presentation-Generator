#define _USE_MATH_DEFINES
#include <iostream>
#include <SDL.h>
#include <SDL_image.h>

SDL_Window* win = NULL;
SDL_Renderer* ren = NULL;

using namespace std;

int win_width = 1000, win_heigth = 800;

void DeInit(int error) {
	//if (ren != NULL) SDL_DestroyRenderer(ren);
	if (win != NULL) SDL_DestroyWindow(win);
	IMG_Quit();
	SDL_Quit();
	exit(error);
}

void Init() {
	if (SDL_Init(SDL_INIT_VIDEO) != 0) {
		printf("Couldn't init SDL! Error: %s", SDL_GetError());
		system("pause");
		DeInit(1);
	}

	int res;
	if ((res = IMG_Init(IMG_INIT_PNG | IMG_INIT_JPG)) == 0) {
		printf("Couldn't init SDL_Image! Error: %s", SDL_GetError());
		system("pause");
		DeInit(1);
	}
	if (res & IMG_INIT_PNG) printf("Initialized PNG library.\n"); else printf("Couldn't init PNG library.\n");
	if (res & IMG_INIT_JPG) printf("Initialized JPG library.\n"); else printf("Couldn't init JPG library.\n");

	win = SDL_CreateWindow("Just another window", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
		win_width, win_heigth, SDL_WINDOW_SHOWN | SDL_WINDOW_RESIZABLE);
	if (win == NULL) {
		printf("Couldn't create window Error: %s", SDL_GetError());
		system("pause");
		DeInit(1);
	}

	/*ren = SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED);
	if (ren == NULL) {
		printf("Couldn't create renderer! Error %s", SDL_GetError());
		system("pause");
		DeInit(1);
	}*/
}

int main(int argc, char* argv[]) {
	Init();

	SDL_Surface* surface = IMG_Load("Cat.jpg");
	if (surface == NULL) {
		printf("Couldn't load image! Error: %s", SDL_GetError());
		system("pause");
		DeInit(1);
	}

	SDL_Surface* win_surf = SDL_GetWindowSurface(win);

	SDL_Event ev;
	bool isRunning = true;

	while (isRunning) {
		while (SDL_PollEvent(&ev)) {
			switch (ev.type) {
			case SDL_QUIT:
				isRunning = false;
				break;

			case SDL_WINDOWEVENT:
				if (ev.window.event == SDL_WINDOWEVENT_SIZE_CHANGED) {
					win_width = ev.window.data1;
					win_heigth = ev.window.data2;
				}
				break;
			}
		}

		SDL_BlitSurface(surface, NULL, win_surf, NULL);

		SDL_UpdateWindowSurface(win);

/*#pragma region DRAWING
		SDL_SetRenderDrawColor(ren, 255, 255, 255, 255);
		SDL_RenderClear(ren);

#pragma endregion

		SDL_RenderPresent(ren);
		SDL_Delay(20);*/
	}

	SDL_FreeSurface(surface);
	DeInit(0);
	return 0;
}