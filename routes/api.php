<?php

use Illuminate\Http\Request;

Route::get('/check',function () {
    $client = new GuzzleHttp\Client();
    $res = $client->get("Flasks:80/");
    
    dd(json_decode($res->getBody()->getContents()));
    echo $res->getStatusCode();
    // "200"
    echo $res->getHeader('content-type')[0];
    // 'application/json; charset=utf8'
    // echo ;
});