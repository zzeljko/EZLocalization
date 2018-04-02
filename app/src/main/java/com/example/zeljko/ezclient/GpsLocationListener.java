package com.example.zeljko.ezclient;

import android.content.Context;
import android.location.Location;
import android.location.LocationProvider;
import android.os.Bundle;
import android.widget.Toast;

/**
 * Created by zeljko on 21.03.2018.
 */

class GpsLocationListener implements android.location.LocationListener {

    Context context;
    boolean gpsAvailable;
    Location location;

    GpsLocationListener(Context context) {
        this.context = context;
        gpsAvailable = false;
    }

    @Override
    public void onLocationChanged(Location location) {
        this.location = location;
        Toast.makeText(context, "got location", Toast.LENGTH_LONG).show();
    }

    @Override
    public void onStatusChanged(String s, int status, Bundle bundle) {
        gpsAvailable = (status == LocationProvider.AVAILABLE);
    }

    @Override
    public void onProviderEnabled(String s) {

    }

    @Override
    public void onProviderDisabled(String s) {

    }

    public boolean checkGpsAvailable() {
        return gpsAvailable;
    }

    public Location getGpsCoord() {
        return location;
    }
}
