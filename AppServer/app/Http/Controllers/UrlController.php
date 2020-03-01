<?php

namespace App\Http\Controllers;

use App\Url;
use App\UserFeedback;
use GuzzleHttp\Client;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class UrlController extends Controller
{
    public function check(Request $request)
    {

        $url = str_replace("%2E", ".", $request->url);

        $url = addScheme($url);

        if (isUrl($url)) {
            $parsedUrl = parse_url($url);
            if (key_exists("host",$parsedUrl)) {
                $host = $parsedUrl['host'];
                $domain =  Url::where('url',$host)->first();

                if ( $domain ) {
                    return response()->json([ 'status' => 201, 'message' => 'It is Phishing url' ]);
                } else {
                    $client = new Client();
                    $res = $client->get("flask:80/");

                     $responseJson = $res->getBody()->getContents();

                    return response()->json($responseJson);
                }

            }
        } else {
            return response()->json(['status' => 400, 'message' => 'bad url ' . $url]);
        }

    }

    public function getUrls()
    {
        $client = new Client();
        $res = $client->get("https://openphish.com/feed.txt");

        $urlList = $res->getBody()->getContents();
        Storage::disk('local')->put('feed.txt', $urlList);

        return response()->json(['status' => 200, 'message' => 'Success getting the list']);
    }

    public function fillUrls()
    {
        $file = Storage::disk('local')->get('feed.txt');
        $urls = explode("\n", $file);

        foreach ($urls as $url) {
            $parsedUrl = parse_url($url);
            if (key_exists("host", $parsedUrl)) {
                $host = $parsedUrl['host'];
                $domain = Url::where('url', $host)->first();
                if ( !$domain ) {
                    $domain = new Url();
                    $domain->url = $host;
                    $domain->isGood = false;
                    $domain->save();
                }
            }
        }

        return response()->json(['status_code' => 200, 'message' => 'Done Inserting']);
    }

    public function view()
    {
        $urls = Url::get();
        $list = [];
        foreach ($urls as $url) {
            array_push($list, $url->url);
        }

        return view('list', ['urls' => $list]);
    }

    public function feedback(Request $request)
    {
        $url = addScheme($request->url);
        $feedback = $request->feedback;
        $parsedUrl = parse_url($url);

        if (key_exists("host", $parsedUrl)) {
            $host = $parsedUrl['host'];
            $domain = UserFeedback::where('url', $host)->first();
            if ($domain) {
                $domain->feedback += $feedback;
                $urlInfo = $domain->url($host);
                if ($domain->feedback > 0 && !$urlInfo->isGood) {
                    $urlInfo->isGood = true;
                } elseif ($domain->feedback < 0 && $urlInfo->isGood) {
                    $urlInfo->isGood = false;
                }
                $domain->save();
                $urlInfo->save();
            } else {
                $userFeedback = new UserFeedback();
                $userFeedback->url = $host;
                $userFeedback->feedback = $feedback;
                $userFeedback->save();
            }
        }

        return response()->json(['status' => 200, 'message' => 'Thanks for feedback']);
    }
}
