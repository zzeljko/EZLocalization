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
    IGpsDataCallback gpsDataCallback;

    GpsLocationListener(Context context, IGpsDataCallback gpsDataCallback) {
        this.context = context;
        gpsAvailable = false;
        this.gpsDataCallback = gpsDataCallback;
    }

    @Override
    public void onLocationChanged(Location location) {
        this.location = location;
        gpsDataCallback.onGpsLocationChanged(location);
    }

    @Override
    public void onStatusChanged(String s, int status, Bundle bundle) {
        gpsAvailable = (status == LocationProvider.AVAILABLE);
        gpsDataCallback.onGpsAvailabilityChange(gpsAvailable);
    }

    @Override
    public void onProviderEnabled(String s) {

    }

    @Override
    public void onProviderDisabled(String s) {

    }

}