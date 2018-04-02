package com.example.zeljko.ezclient;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.support.v4.app.ActivityCompat;
import android.util.Log;

/**
 * Created by zeljko on 21.03.2018.
 */

class GpsScanner {

    private static final int MIN_TIME_BETWEEN_SCANS = 10;
    private static final int MIN_DISTANCE_BETWEEN_SCANS = 0;

    private LocationManager locationManager;
    private LocationListener locationListener;
    private Context context;

    GpsScanner(Context context) {

        locationManager = (LocationManager) context.getSystemService(Context.LOCATION_SERVICE);
        locationListener = new GpsLocationListener(context);

        if (ActivityCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) !=
                PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(context,
                Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED)
            return ;

        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, MIN_TIME_BETWEEN_SCANS,
                MIN_DISTANCE_BETWEEN_SCANS, locationListener);

        if (locationListener == null)
            Log.d("interior", "interior");
        else
            Log.d("ext", "ext");

        this.context = context;
    }

    public Location getGpsCoord() {
        return ((GpsLocationListener) locationListener).getGpsCoord();
    }

    public boolean checkGpsAvail() {
        return ((GpsLocationListener) locationListener).checkGpsAvailable();
    }
}
