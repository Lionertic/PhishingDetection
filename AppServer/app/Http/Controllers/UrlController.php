<?php

namespace App\Http\Controllers;

use App\Url;
use App\UserFeedback;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\ClientException;
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

                if ($domain) {
                    return response()->json(['message' => 'It is Phishing url'], 200);
                } else {
                    try {
                        $client = new Client();
                        $params = [
                            'query' => [
                               'url' => $url
                            ]
                         ];
                        $res = $client->get("flask:80/",$params);
                        $responseJson = json_decode($res->getBody()->getContents());
                        return response()->json($responseJson, 200);

                    } catch (ClientException $exception) {
                        return response()->json(['message' => 'Flask error'], 500);
                    }
                }
            } else {
                return response()->json(['message' => 'bad url ' . $url], 400);
            }
        } else {
            return response()->json(['message' => 'bad url ' . $url], 400);
        }
    }

    public function getUrls()
    {
        $client = new Client();
        $res = $client->get("https://openphish.com/feed.txt");

        $urlList = $res->getBody()->getContents();
        Storage::disk('local')->put('feed.txt', $urlList);

        return response()->json(['message' => 'Success getting the list'], 200);
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

        return response()->json(['message' => 'Done Inserting'], 200);
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
                $client = new Client();
                $params = [
                    'query' => [
                        'url' => $url,
                        'loc' => $domain->location,
                        'feedback' => $domain->feedback
                    ]
                ];
                $res = $client->get("flask/retrain",$params);
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
                $client = new Client();
                $params = [
                    'query' => [
                        'url' => $url,
                        'loc' => -1,
                        'feedback' => $userFeedback->feedback
                    ]
                ];
                $urlInfo = Url::where("url",$host)->first();
                if ( ! $urlInfo ) {
                    $urlInfo = new Url();
                    $urlInfo->url = $host;
                    if ( $feedback == 1 ) {
                        $urlInfo->isGood = true;
                    } else {
                        $urlInfo->isGood = false;
                    }
                    $urlInfo->save();
                }
                $res = $client->get("flask/retrain",$params);
                $location = json_decode($res->getBody()->getContents(),true)["location"];
                $userFeedback->location = $location;
                $userFeedback->save();
            }
        }

        return response()->json(['message' => 'Thanks for feedback'], 200);
    }
}
