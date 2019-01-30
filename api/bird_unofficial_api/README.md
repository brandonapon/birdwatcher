# iot_test
This is a basic script to access the bird API.
Last Updated: 01/12/2019

How to run:
python polling_main.py

General overview:
The bird_api.py file contains all the functions necessary to login and pull data from the bird REST api. The polling_main.py is the main script where the bird_api functions as well as a general scheduler (located in periodic_polling.py) are used to pull data periodically.

Things to implement:
1. Format the output data to be useable
2. Parse the output data
3. implement google maps heatmap
