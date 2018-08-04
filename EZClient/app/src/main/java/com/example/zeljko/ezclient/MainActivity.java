package com.example.zeljko.ezclient;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.Circle;
import com.google.android.gms.maps.model.CircleOptions;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;

public class MainActivity extends AppCompatActivity implements OnMapReadyCallback, IOnEZUpdate{

    private BroadcastReceiver gpsBroadcastReceiver;
    private BroadcastReceiver wifiBroadcastReceiver;

    private Button startButton;
    private Button stopButton;

    private float newLat;
    private float newLong;

    private IOnEZUpdate callbackContext;
    GoogleMap googleMap;
    MarkerOptions currentPos;
    CircleOptions circlePos;
    Circle circle;

    @Override
    public void onMapReady(GoogleMap googleMap) {
        this.googleMap = googleMap;
//        marker = googleMap.addMarker(currentPos);
        circle = googleMap.addCircle(circlePos);
    }

    @Override
    public void onEZUpdateCallback(String latitude, String longitude) {
        newLat = Float.parseFloat(latitude);
        newLong = Float.parseFloat(longitude);

        LatLng pos = new LatLng(newLat, newLong);
//        marker.setPosition(pos);
        circle.setCenter(pos);
        googleMap.moveCamera(CameraUpdateFactory.newLatLngZoom(pos, 18));
    }

    private class StartButtonClickListener implements Button.OnClickListener {

        @Override
        public void onClick(View view) {

            Intent intent = new Intent(getApplicationContext(), ScannerService.class);
            startService(intent);

            if (gpsBroadcastReceiver == null)
                gpsBroadcastReceiver = new BroadcastReceiver() {
                    @Override
                    public void onReceive(Context context, Intent intent) {

                        String message = intent.getExtras().get("location").toString();
//                        Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
                        new MessageSender(callbackContext).executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, message, getString(R.string.gps_message_to_server));
                    }
                };

            if (wifiBroadcastReceiver == null)
                wifiBroadcastReceiver = new BroadcastReceiver() {
                    @Override
                    public void onReceive(Context context, Intent intent) {

                        String message = intent.getExtras().get("wifi_record_list").toString();
//                        Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
                        new MessageSender(callbackContext).executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, message, getString(R.string.wifi_message_to_server));

                    }
                };

            registerReceiver(gpsBroadcastReceiver, new IntentFilter("location_update"));
            registerReceiver(wifiBroadcastReceiver, new IntentFilter("wifi_scan"));
        }
    }

    private class StopButtonClickListener implements Button.OnClickListener {

        @Override
        public void onClick(View view) {
            Intent intent = new Intent(getApplicationContext(), ScannerService.class);
            stopService(intent);

            if (gpsBroadcastReceiver != null)
                unregisterReceiver(gpsBroadcastReceiver);

            if (wifiBroadcastReceiver != null)
                unregisterReceiver(wifiBroadcastReceiver);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        callbackContext = this;
        currentPos = new MarkerOptions().position(new LatLng(0, 0))
                .title("Marker in PRECIS");
        circlePos = new CircleOptions().center(new LatLng(0, 0)).radius(0.2).fillColor(Color.BLUE);

        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.google_map);
        mapFragment.getMapAsync(this);

        startButton = findViewById(R.id.startButton);
        stopButton = findViewById(R.id.stopButton);

        startButton.setOnClickListener(new StartButtonClickListener());
        stopButton.setOnClickListener(new StopButtonClickListener());
    }

    @Override
    protected void onResume() {
        super.onResume();
    }

    @Override
    protected  void onDestroy() {
        super.onDestroy();

        Intent intent = new Intent(getApplicationContext(), ScannerService.class);
        stopService(intent);

        if (gpsBroadcastReceiver != null)
            unregisterReceiver(gpsBroadcastReceiver);

        if (wifiBroadcastReceiver != null)
            unregisterReceiver(wifiBroadcastReceiver);
    }
}
