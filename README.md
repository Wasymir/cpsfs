
# Command_Line_Python_Space_Simulator
___
___
### 0. Table of Contents
- [1. UI Explanation](https://github.com/Wasymir/cpsfs#1-ui-explanation)
- [2. Key Binding](https://github.com/Wasymir/cpsfs#2-key-binding)
- [3. Installation tutorial for non-technical people](https://github.com/Wasymir/cpsfs#3-installation-tutorial-for-non-technical-people)
___
___
## 1. Ui Explanation
___
![UI Image](img/ui_screen.png)
___
___
### S_Position -> Simplified Position
Is used to define a simplified position on the map, useful for navigation on map.
___
| property      | Description |
| :---        |    :----:   |
| z      | z axis integer position       | 
| x   | x axis integer position        | 
| y   | y axis integer position       | 
___
___
### D_Position -> Detailed Position
Is used to define a detailed position on the map, useful for determining the distance to the next map block.
___
| property      | Description |
| :---        |    :----:   |
| z      | z axis float position       | 
| x   | x axis float position        | 
| y   | y axis float position       | 
| rh   | relative height       | 
| R.H.W   | relative height warning - starts blinking if rh < 1|

___
___
### Rotation
___
Determines the slope and rotation of the ship about the axes.
___
| property      | Description |
| :---        |    :----:   |
| z      | z axis rotation (see 'a' angle at  1. picture)| 
| x   | x axis rotation (see 'b' angle at 2. picture)| 
___
1. picture

![Angle z image](img/rotzpic.png)
___
2. picture

![Angle z image](img/rozxpic.png)
___
___
### Velocity
Is used to define a movement speed at every axis and engine thrust.
___
| property      | Description |
| :---        |    :----:   |
| z      | z axis movement speed       | 
| x   | x axis movement speed        | 
| y   | y axis movement speed       | 
| tr   | engine thrust       |
___
___
### Fuel
Is used to define a fuel level.
___
| property      | Description |
| :---        |    :----:   |
| fl      | fuel level       | 
| F.L.W   | Fuel Level Warning - starts blinking if fl < 50 |
___
___
### Auto_TK_Sys -> Automatic Take-off and Landing System
___
| property      | Description |
| :---        |    :----:   |
| S.I      | State Indicator       | 
___
| S.I state      | Description |
| :---        |    :----:   |
| solid      | landed       (press t to take-off)| 
| blinking   | landing conditions met (press l to land)|
| loading  | landing / take-off in progress (wait)|

___
___
### Terrain Height map
Used for navigation and determination of altitude on a given map block.
___
![terrain map pic](img/terrainmappic.png)

| map cell value      | Description |
| :---        |    :----:   |
| number      | terrain height       | 
| !   | block of the map that you can crash into        | 
| @   | your ship       | 
| #   | block outside of map       |
___
___
### X_axis_AGSS -> X axis Advanced Graphic Surface Scanner
Used to navigate perpendicular to the x axis.
___
![X axis AGSS pic](img/agssxpic.png)

| map cell value      | Description |
| :---        |    :----:   |
| *      | empty map block       | 
| X   | filled map block        | 
| @   | your ship       | 
| #   | block outside of map       |
___
___
### Y_axis_AGSS -> Y axis Advanced Graphic Surface Scanner
Used to navigate perpendicular to the y axis.
___
![Y axis AGSS pic](img/agssypic.png)

| map cell value      | Description |
| :---        |    :----:   |
| *      | empty map block       | 
| X   | filled map block        | 
| @   | your ship       | 
| #   | block outside of map       |
___
___
## 2. Key Binding
___
| key      | function |
| :---        |    :----:   |
|   w    |   Pitch up  (raises x axis rotation)   | 
|   s   |    Pitch down (decrease x axis rotation)    | 
|   a   |    Yaw left (decrease z axis rotation)   | 
|   d   |    Yaw right (raises z axis rotation)   | 
|  q    |    Thrust up  (raises thrust)  | 
|  e    |    Thrust Down (decrease thrust)   | 
|  x    |   Thrust Emergency Brake (sets thrust to 0)    | 
|  z    |   Thrust Max (sets thrust to 100)    | 
|  c    |   Thrust Min (sets thrust to -100)    | 
|  r    |  Landing Engines up (raises z axis movement velocity)     | 
|  f    |  Landing Engines down (decrease z axis movement velocity)    | 
|  g    |  quit     | 
___
___
## 3. Installation tutorial for non-technical people
___
1. Download and install [Github Desktop](https://desktop.github.com/)

2. Clone Repository to your computer:
   - Open Github Desktop.
   - Click 'Clone repository from the Internet...' button.
   - Select 'Url' option
   - Paste link to this repository and choose download dir.
   
3. If you want to get the current version of repository just select pull option from Repository tab.
4. If you don't have python, install it. According to this [tutorial](https://www.youtube.com/watch?v=IDo_Gsv3KVk).
5. If you are using Windows just run 'run.cmd' file, but if you are using Linux or MacOs run this commands in terminal (remember to replace the brackets)
> cd (path to folder with the repository)\
> pip install -r requirements.txt\
> python cpsfs.py

   




