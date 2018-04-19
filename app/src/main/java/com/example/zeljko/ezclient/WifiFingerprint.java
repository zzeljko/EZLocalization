package com.example.zeljko.ezclient;

import android.net.wifi.ScanResult;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by zeljko on 18.04.2018.
 */

public class WifiFingerprint {

    public class WifiRecord {

        String bssId;
        int signal;
        int channel;

        public WifiRecord(String bssId, int signal, int channel) {
            this.bssId = bssId;
            this.signal = signal;
            this.channel = channel;
        }
    }

    private List<WifiRecord> recordList;
    private long timestamp;

    public WifiFingerprint(List<ScanResult> wifiScanResults) {
        recordList = new ArrayList<WifiRecord>();

        for (ScanResult result : wifiScanResults) {
            recordList.add(new WifiRecord(result.BSSID,
                    result.level,
                    WifiChannel.getChannel(result.frequency)));
        }

        this.timestamp = System.currentTimeMillis();
    }

    public String toString() {
        StringBuffer message = new StringBuffer();
        message.append("<wifi t=\"");
        message.append(timestamp);
        message.append("\">\n");

        for (WifiRecord record : recordList) {
            message.append("<record bssId=\"");
            message.append(record.bssId);
            message.append("\" signal=\"");
            message.append(record.signal);
            message.append("\" channel=\"");
            message.append(record.channel);
            message.append("\" />\n");
        }
        message.append("</wifi>");

        return message.toString();
    }
}
