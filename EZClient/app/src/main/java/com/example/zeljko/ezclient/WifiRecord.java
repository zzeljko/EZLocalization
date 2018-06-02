package com.example.zeljko.ezclient;

/**
 * Created by zeljko on 01.06.2018.
 */

public class WifiRecord {

    String bssId;
    int signal;

    public WifiRecord(String bssId, int signal) {
        this.bssId = bssId;
        this.signal = signal;
    }

    public String getBssId() {
        return bssId;
    }

    public int getSignal() {
        return signal;
    }
}
