package com.example.zeljko.ezclient;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    private BroadcastReceiver gpsBroadcastReceiver;
    private BroadcastReceiver wifiBroadcastReceiver;

    private Button startButton;
    private Button stopButton;

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
                        new MessageSender().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, message, getString(R.string.gps_message_to_server));
                    }
                };

            if (wifiBroadcastReceiver == null)
                wifiBroadcastReceiver = new BroadcastReceiver() {
                    @Override
                    public void onReceive(Context context, Intent intent) {

                        String message = intent.getExtras().get("wifi_record_list").toString();
//                        Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
                        new MessageSender().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, message, getString(R.string.wifi_message_to_server));

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
