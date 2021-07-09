# Overview
In this project I'm going to implement a game named HoleInTheWallGame based on the game show Hole In The Wall.
The game basically displays a character that is controlled by the real life poses of the player. 
Towards that character come moving walls with holes shaped as a specific position and the player must mimic this position to pass through the wall or he will crash and destroy the wall. 
The objective is to pass through as many walls as possible without crashing them.

# Game Play
<iframe width="560" height="315" src="https://www.youtube.com/embed/a2zWyde3zBQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

# Guidelines
1. Download these files.
2. Add the Given Unity Part to your own Unity Project.
3. Edit your build settings to be this order of Scenes (File -> Build Settings -> Scenes In Build):
    - Scenes/StartGameScreen.
    - Scenes/GamePlay.
    - Scenes/ScoreScreen.
4. To run the game:
    - Run the game from Unity.
    - Press **Play** button.
    - Pause the game 
    - Run hole_in_the_wall_game_runner.py till we see the connection
    - Un Pause the game and play normally.
    - **If we lose the game and want to play again, press the Play Again button and go back to stage (3.3).**
  
Note: We need (4.3) stage since I didn't add automatic execution of (4.4) from the code yet and have to do it manually - so in order for the character to stay in place, we do it till we establish the connection with python) then we un pause in (4.5)

# Used Tools
Python Part:
  * Pose Estimation:
    - [Media Pipe Poses](https://google.github.io/mediapipe/solutions/pose.html)
  * Image Displaying and Editing:
    - [cv2 from opencv-python](https://pypi.org/project/opencv-python/)

Unity Part:
  * Animation Riggind Package (Min Version: Unity 2019.3):
    - To use it too:
      * Edit ->Project Settings -> Project Manager -> Enable Preview Packages.
      * Windwoss -> Package Manager -> Search for Animain Rigging and install.
  * [TextMesh Pro](https://docs.unity3d.com/Manual/com.unity.textmeshpro.html)
  * Assets used (From Unity Asset Store):
    - [3D Character Dummy](https://assetstore.unity.com/packages/3d/characters/humanoids/humans/3d-character-dummy-178395)
    - [Unity Particle Pack(For the explosion effect)](https://assetstore.unity.com/packages/essentials/tutorial-projects/unity-particle-pack-127325)
    
# Credits
* Project by: Anis Mograbi and Mohammad Tawil.
* Mentored by: Yinon Oshrat.
