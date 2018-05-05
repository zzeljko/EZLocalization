package com.example.zeljko.ezclient;

import android.location.Location;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

/**
 * Created by zeljko on 21.03.2018.
 */

interface ICommunicationChannel {

    @POST("gps_data")
    Call<Location> postGpsData(@Body Location location);
    @POST("wifi_data")
    Call<WifiFingerprint> postWifiData(@Body WifiFingerprint wifiFingerprint);
}
