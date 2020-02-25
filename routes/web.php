<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Route::post('/fillUrls', function() {
    $file = Storage::disk('local')->get('feed.txt');
    $urls = explode("\n",$file);

    foreach ($urls as $url){
        $parsedUrl = parse_url($url);
        if (key_exists("host",$parsedUrl)) {
            $host = $parsedUrl['host'];
            $domain = App\Url::where('url', $host)->firstOrFail();
            if ( $domain ) {
                $domain = new App\Url();
                $domain->url = $host;
                $domain->save();
            }
        }
    }

    return response()->json(['status_code' => 200, 'message' => 'Done Inserting']);
});
