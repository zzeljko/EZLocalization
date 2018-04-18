package com.example.zeljko.ezclient;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    private WiFiScanner wiFiScanner;
    private CommunicationChannel channel;
    private BroadcastReceiver gpsBroadcastReceiver;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        wiFiScanner = new WiFiScanner();
        channel = new CommunicationChannel();

        Intent intent = new Intent(getApplicationContext(), GpsScannerService.class);
        startService(intent);
    }

    @Override
    protected void onResume() {
        super.onResume();

        if (gpsBroadcastReceiver == null)
            gpsBroadcastReceiver = new BroadcastReceiver() {
                @Override
                public void onReceive(Context context, Intent intent) {
                    Toast.makeText(getApplicationContext(), intent.getExtras().get("location").toString(), Toast.LENGTH_SHORT).show();
                }
            };

        registerReceiver(gpsBroadcastReceiver, new IntentFilter("location_update"));
    }

    @Override
    protected  void onDestroy() {
        super.onDestroy();

        Intent intent = new Intent(getApplicationContext(), GpsScannerService.class);
        stopService(intent);

        if (gpsBroadcastReceiver != null)
            unregisterReceiver(gpsBroadcastReceiver);
    }
}
