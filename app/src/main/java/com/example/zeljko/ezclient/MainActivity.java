package com.example.zeljko.ezclient;

import android.location.Location;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;

import java.util.List;

public class MainActivity extends AppCompatActivity implements IGpsDataCallback {

    private GpsScanner gpsScanner;
    private WiFiScanner wiFiScanner;
    private CommunicationChannel channel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        gpsScanner = new GpsScanner(this, this);
        wiFiScanner = new WiFiScanner();
        channel = new CommunicationChannel();
    }

    @Override
    protected  void onDestroy() {
        super.onDestroy();
        gpsScanner.remove();
    }

    @Override
    public void onGpsAvailabilityChange(boolean avail) {
        if (!avail)
            Toast.makeText(this, "GPS not avail", Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onGpsLocationChanged(Location location) {
        Toast.makeText(this, location.toString(), Toast.LENGTH_SHORT).show();
    }
}
