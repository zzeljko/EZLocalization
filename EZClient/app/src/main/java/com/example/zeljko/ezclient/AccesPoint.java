package com.example.zeljko.ezclient;

/**
 * Created by zeljko on 21.03.2018.
 */

class AccesPoint {

    private String id;

    private float strength;
    private float pathLossExponent;
    private float transmitPowerHenceForth;

    private boolean known;

    public boolean isKnown() {
        return known;
    }
}
