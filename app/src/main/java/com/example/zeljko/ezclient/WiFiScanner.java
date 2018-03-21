package com.example.zeljko.ezclient;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by zeljko on 21.03.2018.
 */

class WiFiScanner {

    public List<AccesPoint> getVisibleAccessPointList() {
        return new ArrayList<>();
    }

    public List<AccesPoint> getUnknownAccessPointList() {

        List<AccesPoint> unknownAccessPointList = new ArrayList<>();
        for (AccesPoint ap : getVisibleAccessPointList())
            if (!ap.isKnown())
                unknownAccessPointList.add(ap);

        return unknownAccessPointList;
    }
}
