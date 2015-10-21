# Flexlm Monitor with RRD

## Description
This is flask app for monitoring Flexlm servers. You can specify an rdd file and 
the columns you want then plot the results as a d3 chart. You will need to set up
the rrd file and collect the usage data from the flexlm server.

Requirments
lmutil
python, rrdtool
sqlite
flask

See the requirments.txt for the nessary python packages.

To run the application.
```
python flexlm_app.py runserver
```
point your browser at: http://localhost:5000/

The application was orginally written to replace somthing that I had written in 
the past that worked but was not that portable. It was also written to try out 
flask. Hence could most probably be structured a little bit better. 

## Credits
Glyphicons - for the use of the icons

beaugunderson -  https://github.com/beaugunderson/flexlm-license-status 
Used their regular expressions for parsing the lmutil output.



