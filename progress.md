Discussion on 01/18/2019

* Convert data from 2 sources into a normalized format
* Write scripts to spit out csv in defined schema for easier downstream analysis/modelling/visualization
* Schema of CSV file (as of now):
    - id : Bike id (String)
    - latitude : (Float)
    - longitude : (Float)
    - battery_level: (Int, Default Val: None)
    - captive: (Boolean, Default Val : False)
    - time_stamp: (dateTime object)