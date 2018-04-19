package com.example.zeljko.ezclient;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    private CommunicationChannel channel;
    private BroadcastReceiver gpsBroadcastReceiver;
    private BroadcastReceiver wifiBroadcastReceiver;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        channel = new CommunicationChannel();

        Intent intent = new Intent(getApplicationContext(), ScannerService.class);
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

        if (wifiBroadcastReceiver == null)
            wifiBroadcastReceiver = new BroadcastReceiver() {
                @Override
                public void onReceive(Context context, Intent intent) {
                    Toast.makeText(getApplicationContext(), intent.getExtras().get("wifi_record_list").toString(), Toast.LENGTH_SHORT).show();
                }
            };

        registerReceiver(gpsBroadcastReceiver, new IntentFilter("location_update"));
        registerReceiver(wifiBroadcastReceiver, new IntentFilter("wifi_scan"));
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
