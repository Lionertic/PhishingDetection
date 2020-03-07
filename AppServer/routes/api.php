<?php

Route::get('/check', 'UrlController@check')->middleware('throttle:30');

Route::get("/feedback", "UrlController@feedback")->middleware('throttle:30');
