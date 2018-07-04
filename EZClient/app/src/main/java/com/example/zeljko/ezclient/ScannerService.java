package com.example.zeljko.ezclient;

import android.Manifest;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Criteria;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.IBinder;
import android.provider.Settings;
import android.support.annotation.Nullable;
import android.support.v4.app.ActivityCompat;
import android.util.Log;
import android.widget.Toast;

/**
 * Created by zeljko on 21.03.2018.
 */

public class ScannerService extends Service implements IOnWifiDataCallback {

    private static final long MIN_TIME_BETWEEN_SCANS = 0;
    private static final float MIN_DISTANCE_BETWEEN_SCANS = 0;

    private static final float ACCURACY_LIMIT = 10;
    private static final int GPS_SAMPLES_PER_SCAN = 10;

    private int numberOfGpsSamples;

    private LocationManager locationManager;
    private LocationListener locationListener;
    private WifiScanner wifiScanner;

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onCreate() {
        numberOfGpsSamples = 0;
        firstTime = true;
        locationManager = (LocationManager) getApplicationContext().getSystemService(Context.LOCATION_SERVICE);
        createLocationListener();

        if (ActivityCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.ACCESS_FINE_LOCATION) !=
                PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(getApplicationContext(),
                Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED)
            return ;

        Criteria criteria = new Criteria();
        criteria.setAccuracy(Criteria.ACCURACY_FINE);
        criteria.setPowerRequirement(Criteria.POWER_HIGH);
        criteria.setAltitudeRequired(false);
        criteria.setSpeedRequired(false);
        criteria.setCostAllowed(true);
        criteria.setBearingRequired(false);
        criteria.setHorizontalAccuracy(Criteria.ACCURACY_HIGH);
        criteria.setVerticalAccuracy(Criteria.ACCURACY_HIGH);

        locationManager.requestLocationUpdates(MIN_TIME_BETWEEN_SCANS, MIN_DISTANCE_BETWEEN_SCANS, criteria, locationListener, null);

        wifiScanner = new WifiScanner(getApplicationContext(), this);
    }

    boolean firstTime;

    private void createLocationListener() {
        locationListener = new LocationListener() {
            @Override
            public void onLocationChanged(Location location) {
                if (location.getAccuracy() > ACCURACY_LIMIT) {
                    firstTime = true;
                    return;
                }


                if (firstTime) {
                    Toast.makeText(getApplicationContext(), "new location", Toast.LENGTH_SHORT).show();
                    firstTime = false;
                    numberOfGpsSamples = 0;
                }

                numberOfGpsSamples++;
                Toast.makeText(getApplicationContext(), "" + numberOfGpsSamples, Toast.LENGTH_SHORT).show();
                if (numberOfGpsSamples == GPS_SAMPLES_PER_SCAN) {
                    Toast.makeText(getApplicationContext(), "move", Toast.LENGTH_SHORT).show();
                    Intent intent = new Intent("location_update");
                    intent.putExtra("location", new GPSFingerprint(location).toString());

                    sendBroadcast(intent);
                    numberOfGpsSamples = 0;
                    return;
                }
            }

            @Override
            public void onStatusChanged(String s, int i, Bundle bundle) {

            }

            @Override
            public void onProviderEnabled(String s) {


            }

            @Override
            public void onProviderDisabled(String s) {
                Intent intent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

                startActivity(intent);
            }
        };
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (locationManager != null)
            locationManager.removeUpdates(locationListener);
        if (wifiScanner != null)
            wifiScanner.stopScanning();
    }

    @Override
    public void onWiFiSample(WifiFingerprint scan) {
        Intent intent = new Intent("wifi_scan");
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        intent.putExtra("wifi_record_list", scan.toString());
        sendBroadcast(intent);
    }
}
