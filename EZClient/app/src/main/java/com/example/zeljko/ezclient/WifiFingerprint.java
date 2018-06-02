package com.example.zeljko.ezclient;

import android.net.wifi.ScanResult;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by zeljko on 18.04.2018.
 */

public class WifiFingerprint {

    private List<WifiRecord> recordList;
    private long timestamp;

    public WifiFingerprint(List<ScanResult> wifiScanResults) {
        recordList = new ArrayList<>();

        for (ScanResult result : wifiScanResults) {
            recordList.add(new WifiRecord(result.BSSID,
                    result.level));
        }

        this.timestamp = System.currentTimeMillis();
    }

    public WifiFingerprint(List<WifiRecord> wifiRecords, long timestamp) {

        recordList = new ArrayList<>();
        for (WifiRecord wr : wifiRecords)
            recordList.add(wr);

        this.timestamp = timestamp;
    }

    public List<WifiRecord> getRecordList() {
        return recordList;
    }

    public String toString() {
        StringBuffer message = new StringBuffer();

        message.append("{\n\t\"wr\": \n\t\t[");
        message.append("\n");

        for (WifiRecord record : recordList) {
            message.append("\t\t\t{\n");
            message.append("\t\t\t\t\"b\": \"" + record.bssId + "\",\n");
            message.append("\t\t\t\t\"s\": \"" + record.signal + "\"\n");
            message.append("\t\t\t},\n\n");
        }
        message.deleteCharAt(message.lastIndexOf(","));

        message.append("\t\t],\n");
        message.append("\t\"t\": \"" + timestamp + "\"");
        message.append("\n}");
        return message.toString();
    }
}
