package com.example.zeljko.ezclient;

import android.Manifest;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.IBinder;
import android.provider.Settings;
import android.support.annotation.Nullable;
import android.support.v4.app.ActivityCompat;
import android.util.Log;

/**
 * Created by zeljko on 21.03.2018.
 */

public class ScannerService extends Service implements IOnWifiDataCallback {

    private static final int MIN_TIME_BETWEEN_SCANS = 1000;
    private static final int MIN_DISTANCE_BETWEEN_SCANS = 0;

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

        locationManager = (LocationManager) getApplicationContext().getSystemService(Context.LOCATION_SERVICE);
        createLocationListener();

        if (ActivityCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.ACCESS_FINE_LOCATION) !=
                PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(getApplicationContext(),
                Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED)
            return ;

        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, MIN_TIME_BETWEEN_SCANS,
                MIN_DISTANCE_BETWEEN_SCANS, locationListener);

        wifiScanner = new WifiScanner(getApplicationContext(), this);
    }

    private void createLocationListener() {

        locationListener = new LocationListener() {
            @Override
            public void onLocationChanged(Location location) {
                Intent intent = new Intent("location_update");
                intent.putExtra("location", location.getLatitude() + " " + location.getLongitude());

                sendBroadcast(intent);
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
        Log.d("callback", scan.toString());
        Intent intent = new Intent("wifi_scan");
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        intent.putExtra("wifi_record_list", scan.toString());
        sendBroadcast(intent);
    }
}
