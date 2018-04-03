package com.example.zeljko.ezclient;

import android.location.Location;

/**
 * Created by zeljko on 03.04.2018.
 */

public interface IGpsDataCallback {

    public void onGpsAvailabilityChange(boolean avail);
    public void onGpsLocationChanged(Location location);
}
