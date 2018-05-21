package com.example.zeljko.ezclient;

import android.location.Location;
import android.os.Parcelable;

import java.io.Serializable;

/**
 * Created by zeljko on 21.05.2018.
 */

class GPSFingerprint {

    Location location;

    public GPSFingerprint(Location location) {
        this.location = location;
    }

    @Override
    public String toString() {
        StringBuffer message = new StringBuffer();

        message.append("{\n\t\"gps_record\": \n\t\t{");
        message.append("\n");

        message.append("\t\t\t\t\"lat\": \"" + location.getLatitude() + "\",\n");
        message.append("\t\t\t\t\"long\": \"" + location.getLongitude() + "\"\n");
        message.append("\t\t}");

        message.append("\n}");
        return message.toString();
    }
}
