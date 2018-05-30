package com.example.zeljko.ezclient;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.util.Log;
import android.widget.Toast;

import java.util.List;

/**
 * Created by zeljko on 21.03.2018.
 */

class WifiScanner extends BroadcastReceiver {

    private IOnWifiDataCallback wiFiDataCallback;
    private WifiManager wifiManager;
    private Context context;

    public WifiScanner(Context context, IOnWifiDataCallback wiFiDataCallback) {
        super();

        this.context = context;
        this.wiFiDataCallback = wiFiDataCallback;

        wifiManager = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);

        if (!wifiManager.isWifiEnabled()) {
            Toast.makeText(context, "Please enable WIFI!", Toast.LENGTH_SHORT).show();
            return;
        }


        context.registerReceiver(this, new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
        wifiManager.startScan();
    }

    @Override
    public void onReceive(Context context, Intent intent) {

        List<ScanResult> wifiScanResults = wifiManager.getScanResults();

        WifiFingerprint wifiFingerprint = new WifiFingerprint(wifiScanResults);
        wiFiDataCallback.onWiFiSample(wifiFingerprint);
        wifiManager.startScan();
    }

    public void stopScanning() {
        context.unregisterReceiver(this);
    }
}
