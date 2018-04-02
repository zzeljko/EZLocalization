package com.example.zeljko.ezclient;

import android.location.Location;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;

import java.util.List;

public class MainActivity extends AppCompatActivity {

    private GpsScanner gpsScanner;
    private WiFiScanner wiFiScanner;
    private CommunicationChannel channel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        gpsScanner = new GpsScanner(this);
        wiFiScanner = new WiFiScanner();
        channel = new CommunicationChannel();

        startEz();
    }

    private void startEz() {

        if(gpsScanner.checkGpsAvail()) {
            Location coord = gpsScanner.getGpsCoord();
            Toast.makeText(this, coord + "", Toast.LENGTH_SHORT).show();
            List<AccesPoint> wiFiUnknownAPList = wiFiScanner.getUnknownAccessPointList();

            channel.sendToEzServer(new ServerMessage(coord, wiFiUnknownAPList));
            startEz();
        }

        List<AccesPoint> wiFiAPList = wiFiScanner.getVisibleAccessPointList();
        channel.sendToEzServer(new ServerMessage(wiFiAPList));
        Toast.makeText(this, "gps not avail", Toast.LENGTH_SHORT).show();

        startEz();
    }

}
