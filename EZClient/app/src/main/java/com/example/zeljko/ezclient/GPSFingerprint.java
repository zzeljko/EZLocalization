package com.example.zeljko.ezclient;

import android.location.Location;
import android.os.Parcelable;

import java.io.Serializable;

/**
 * Created by zeljko on 21.05.2018.
 */

class GPSFingerprint {

    private Location location;
    private long timestamp;

    public GPSFingerprint(Location location) {
        this.location = location;
        timestamp = System.currentTimeMillis();
    }

    @Override
    public String toString() {
        StringBuffer message = new StringBuffer();

        message.append("{\n\t\"gr\": \n\t\t{");
        message.append("\n");

        message.append("\t\t\t\t\"la\": \"" + location.getLatitude() + "\",\n");
        message.append("\t\t\t\t\"lo\": \"" + location.getLongitude() + "\",\n");
        message.append("\t\t\t\t\"t\": \"" + location.getLongitude() + "\"\n");
        message.append("\t\t}");

        message.append("\n}");
        return message.toString();
    }
}
