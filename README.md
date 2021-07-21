# SFLA for Robot Path Planning
This is an implementation of the Shuffled Frog leaping Algorithm for
autonomus navigation of mobile Robots.
It uses the Coppeliasim legacy remote API to control a Pioneer P3-DX.

What's in each file?
File | Description
-----|-------------
SFLA | Contains the algorithm as a Python class
followsfla | A jupyter notebook to try the algorithm with a given list of obstacles. If needed, it includes the needed code to simulate the obtained path with Coppelia.
