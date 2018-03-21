package com.example.zeljko.ezclient;

import android.location.Location;

import java.util.List;

/**
 * Created by zeljko on 21.03.2018.
 */

class ServerMessage {

    private Location position;
    private List<AccesPoint> apList;

    public ServerMessage(Location coord, List<AccesPoint> wiFiAPList) {
        position = coord;
        apList = wiFiAPList;
    }

    public ServerMessage(List<AccesPoint> wiFiAPList) {
        apList = wiFiAPList;
    }
}
