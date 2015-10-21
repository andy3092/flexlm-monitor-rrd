# Flexlm Monitor with RRD

## Description
This is flask app for monitoring Flexlm servers. You can specify an rdd file and 
the columns you want then plot the results as a d3 chart. You will need to set up
the rrd file and collect the usage data from the flexlm server.

Requirments
lmutil, python, rrdtool, sqlite

To install the nessary python packages
```
pip install -r requirements.txt
```

To run the application
```
python flexlm_app.py runserver
```

point your browser at: http://localhost:5000/

Once you have added a server you can check on the current users and a 
view a usage chart if you have added an rrd file to the server.

You can also specify a time peroid by using the following URL syntax

```
http://localhost:5000/servers/usage/<server name>/<time peroid>

e.g. 
http://localhost:5000/servers/usage/my_server/1y
```

The corrosponding json end point is
http://localhost:5000/servers/usage/data/<server name>/<time peroid>

The application was orginally written to replace somthing that I had written in 
the past that worked but was not that portable. It was also developed to try 
out flask. Hence could most probably be structured a little bit better. 

## Credits
Glyphicons - for the use of the icons

beaugunderson -  https://github.com/beaugunderson/flexlm-license-status 
Used their regular expressions for parsing the lmutil output.



