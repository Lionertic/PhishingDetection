<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Url;

class UrlController extends Controller
{
    public function check (Request $request) {

        $url = str_replace("%2E",".",$request->url);

        $url = addScheme($url);

        if (isUrl($url)) {
            $parsedUrl = parse_url($url);
            if (key_exists("host",$parsedUrl)) {
                $host = $parsedUrl['host'];
                $domain =  Url::where('url',$host)->first();

                if ( $domain ) {
                    return response()->json([ 'status' => 201, 'message' => 'It is Phishing url' ]);
                } else {
                     $client = new \GuzzleHttp\Client();
                     $res = $client->get("flask:80/");

                     $responseJson = $res->getBody()->getContents();

                    return response()->json($responseJson);
                }

            }
        } else {
            return response()->json([ 'status' => 400, 'message' => 'bad url '.$url ]);
        }

    }

    public function fillUrls () {
        $file = Storage::disk('local')->get('feed.txt');
        $urls = explode("\n",$file);

        foreach ($urls as $url){
            $parsedUrl = parse_url($url);
            if (key_exists("host",$parsedUrl)) {
                $host = $parsedUrl['host'];
                $domain = Url::where('url', $host)->firstOrFail();
                if ( !$domain ) {
                    $domain = new App\Url();
                    $domain->url = $host;
                    $domain->save();
                }
            }
        }

        return response()->json(['status_code' => 200, 'message' => 'Done Inserting']);
    }

    public function view () {
        $urls = Url::get();
        $list = [] ;
        foreach ( $urls as $url) {
            array_push($list,$url->url);
        }

        return view('list', ['urls' => $list] );
    }
}
