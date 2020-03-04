<?php

Route::get('/check', 'UrlController@check')->middleware('throttle:30');

Route::put("/feedback", "UrlController@feedback")->middleware('throttle:30');
