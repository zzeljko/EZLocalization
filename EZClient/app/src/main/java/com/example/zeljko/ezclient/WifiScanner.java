package com.example.zeljko.ezclient;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.util.Log;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by zeljko on 21.03.2018.
 */

class WifiScanner extends BroadcastReceiver {

    private IOnWifiDataCallback wiFiDataCallback;
    private WifiManager wifiManager;
    private Context context;

    private long timer;
    private List<WifiFingerprint> wifiFingerprints;
    private static final int WIFI_SCAN_INTERVAL = 3000;
    private static final int DEVIATION_THRESHOLD = 10;

    public WifiScanner(Context context, IOnWifiDataCallback wiFiDataCallback) {
        super();

        this.context = context;
        this.wiFiDataCallback = wiFiDataCallback;

        wifiFingerprints = new ArrayList<WifiFingerprint>();

        wifiManager = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);

        if (!wifiManager.isWifiEnabled()) {
            Toast.makeText(context, "Please enable WIFI!", Toast.LENGTH_SHORT).show();
            return;
        }


        context.registerReceiver(this, new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
        timer = System.currentTimeMillis();
        wifiManager.startScan();
    }

    @Override
    public void onReceive(Context context, Intent intent) {

        List<ScanResult> wifiScanResults = wifiManager.getScanResults();

        wifiFingerprints.add(new WifiFingerprint(wifiScanResults));

        long currentTime = System.currentTimeMillis();
        if (currentTime - timer > WIFI_SCAN_INTERVAL) {
            WifiFingerprint wifiFingerprint = getMeanWifiSamples(currentTime - (currentTime - timer) / 2);
            wiFiDataCallback.onWiFiSample(wifiFingerprint);
            wifiFingerprints.clear();
            timer = System.currentTimeMillis();
        }
        wifiManager.startScan();
    }

    private WifiFingerprint getMeanWifiSamples(long timestamp) {

        List<WifiRecordHelper> wifiRecordHelpers = new ArrayList<>();
        for (WifiFingerprint wifiFingerprint : wifiFingerprints) {

            List<WifiRecord> recordList = wifiFingerprint.getRecordList();
            for (WifiRecord wifiRecord : recordList) {

                String currentWifiRecordId = wifiRecord.getBssId();
                int currentWifiRecordSignal = wifiRecord.getSignal();
                boolean wifiRecordExists = false;
                for (WifiRecordHelper wifiRecordHelper : wifiRecordHelpers) {

                    if (wifiRecordHelper.getBssId().equals(currentWifiRecordId)) {
                        wifiRecordExists = true;
                        wifiRecordHelper.addSignal(currentWifiRecordSignal);
                        break;
                    }
                }
                if (!wifiRecordExists)
                    wifiRecordHelpers.add(new WifiRecordHelper(currentWifiRecordId, currentWifiRecordSignal));
            }
        }

        List<WifiRecord> meanWifiRecords = new ArrayList<>();
        for (WifiRecordHelper wifiRecordHelper : wifiRecordHelpers) {

            String currentBssId = wifiRecordHelper.getBssId();
            int currentMeanSignal = wifiRecordHelper.getMeanSignal();

            int standardDeviationSum = 0;
            int standardDeviationNoSamples = 0;

            for (WifiFingerprint wifiFingerprint : wifiFingerprints) {

                List<WifiRecord> recordList = wifiFingerprint.getRecordList();
                for (WifiRecord wifiRecordSample : recordList) {

                    if (wifiRecordSample.getBssId().equals(currentBssId)) {

                        standardDeviationNoSamples++;
                        int difference = wifiRecordSample.getSignal() - currentMeanSignal;
                        standardDeviationSum += (difference * difference);
                    }
                }
            }

            int deviation = (int) Math.sqrt(standardDeviationSum / standardDeviationNoSamples);
            if (deviation < DEVIATION_THRESHOLD)
                meanWifiRecords.add(new WifiRecord(currentBssId,  currentMeanSignal));
        }

        return new WifiFingerprint(meanWifiRecords, timestamp);
    }

    private class WifiRecordHelper {

        String bssId;
        int sumOfSignals;
        int numberOfSignals;

        WifiRecordHelper(String id, int signal) {

            bssId = id;
            sumOfSignals = signal;
            numberOfSignals = 1;
        }

        public void addSignal(int signal) {
            sumOfSignals += signal;
            numberOfSignals++;
        }

        public String getBssId() {
            return bssId;
        }

        public int getMeanSignal() {
            return sumOfSignals / numberOfSignals;
        }
    }

    public void stopScanning() {
        context.unregisterReceiver(this);
    }
}
