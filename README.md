To run:

1. `poetry install`
2. `poetry run python main.py --debug`

Assets from:
https://opengameart.org/content/space-ship-mech-construction-kit-2

Plans:
1. [x] Main menu 
2. [ ] Interface, UI panels
    * left panel: game info: current turn, current player
    * right panel: current player info: ships, current ship: moves, hp, mode, weapons; buttons to switch weapons/mode
3. [x] Camera, (minimap?)
4. [ ] Utilize `update` method in scenes(?)
5. [ ] Different screen sizes: adapt grid to show whole cells, adapt panels to show whole text. Allow resize/fullscreen (in menu perhaps)
