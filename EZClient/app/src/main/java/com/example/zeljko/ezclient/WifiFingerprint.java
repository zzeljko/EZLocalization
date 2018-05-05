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

    /*
    {
        "wifi_records":
            [
                {
                    "bssId":
                    "signal":
                    "channel":
                },
            ]
        "timestamp":

    }
     */
    public String toString() {
        StringBuffer message = new StringBuffer();

        message.append("{\n\t\"wifi_records\": \n\t\t[");
        message.append("\n");

        for (WifiRecord record : recordList) {
            message.append("\t\t\t{\n");
            message.append("\t\t\t\t\"bssId\": \"" + record.bssId + "\",\n");
            message.append("\t\t\t\t\"signal\": \"" + record.signal + "\",\n");
            message.append("\t\t\t\t\"channel\": \"" + record.channel + "\"\n");
            message.append("\t\t\t},\n\n");
        }
        message.deleteCharAt(message.lastIndexOf(","));

        message.append("\t\t],\n");
        message.append("\t\"timestamp\": \"" + timestamp + "\"");
        message.append("\n}");
        return message.toString();
    }
}
