README

!!!To setup the client-server communication, both the client and the server device should be connected to the same WiFi access point!!!

In order to update/build a data set, you should use the computeAPParam.py module from the EZServer.
Today it has only one table, with a data set from Precis:

c.execute("CREATE TABLE IF NOT EXISTS ap_loc_precis (bssId varchar(25), Pi0 double precision, path_loss double precision, latitude double precision, longitude double precision)")

All those parameters will be later used by the server to run the algorithm and perform the localization.

If you want to add a new dataset of another building, you should update the latitude/longitude limits from EZServer.py, accordingly to the location of the desired building in which the localization will be performed.

Afterwards, simply running the EZServer.py module will perform the localization for the client. So if you keep moving through the building, your location will be updated accordingly to the server's algorithm output.
