<?php

namespace App\Http\Controllers;

use App\Url;
use App\UserFeedback;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\ClientException;
use Illuminate\Contracts\Filesystem\FileNotFoundException;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class UrlController extends Controller
{
    public function check(Request $request)
    {

        $url = str_replace("%2E", ".", $request->url);

        $url = addScheme($url);
        $parsedUrl = parse_url($url);

        if (key_exists("host", $parsedUrl)) {
            $host = $parsedUrl['host'];
            if (isUrl($host)) {

                $domain = Url::where('url', $host)->first();

                if ($domain) {
                    if ($domain->isGood) {
                        return response()->json(['status' => 1, 'message' => 'Url is fine'], 200);
                    } else {
                        return response()->json(['status' => -1, 'message' => 'Can be used for phishing data'], 200);
                    }
                } else {
                    try {
                        $client = new Client();
                        $params = [
                            'query' => [
                                'url' => $url
                            ]
                        ];
                        $res = $client->get("flask:80/check", $params);
                        $status = json_decode($res->getBody()->getContents(), true)['status'];
                        if ($status > 0) {
                            return response()->json(['status' => 1, 'message' => 'Url is fine'], 200);
                        } else {
                            return response()->json(['status' => -1, 'message' => 'Can be used for phishing data'], 200);
                        }
                    } catch (ClientException $exception) {
                        return response()->json(['status' => 0, 'message' => 'Flask error'], 500);
                    }
                }
            } else {
                return response()->json(['status' => 0, 'message' => 'Bad url ' . $url], 400);
            }
        } else {
            return response()->json(['status' => 0, 'message' => 'Bad url ' . $url], 400);
        }
    }

    public function getUrls()
    {
        try {
            $client = new Client();
            $res = $client->get("https://openphish.com/feed.txt");

            $urlList = $res->getBody()->getContents();
            Storage::disk('local')->put('feed.txt', $urlList);

            return response()->json(['status' => 1, 'message' => 'Success getting the list'], 200);

        } catch (ClientException $exception) {
            return response()->json(['status' => 0, 'message' => 'Error getting the list'], 500);
        }
    }

    public function fillUrls()
    {
        try {
            $file = Storage::disk('local')->get('feed.txt');
            $urls = explode("\n", $file);

            foreach ($urls as $url) {
                $parsedUrl = parse_url($url);
                if (key_exists("host", $parsedUrl)) {
                    $host = $parsedUrl['host'];
                    $domain = Url::where('url', $host)->first();
                    if (!$domain) {
                        $domain = new Url();
                        $domain->url = $host;
                        $domain->isGood = false;
                        $domain->save();
                    }
                }
            }

            return response()->json(['status' => 1, 'message' => 'Done Inserting'], 200);
        } catch (FileNotFoundException $fileNotFoundException) {
            return response()->json(['status' => 0, 'message' => 'Error getting file'], 200);
        }
    }


    public function feedback(Request $request)
    {
        $url = addScheme($request->url);
        $url = str_replace("%2E", ".", $url);

        $feedback = $request->feedback;
        $parsedUrl = parse_url($url);
        if (key_exists("host", $parsedUrl)) {
            $host = $parsedUrl['host'];

            $userFeedback = UserFeedback::where('url', $host)->first();
            if (!$userFeedback) {
                $userFeedback = new UserFeedback();
                $userFeedback->url = $host;
                $userFeedback->location = -1;
            }

            $urlInfo = Url::where("url", $host)->first();
            if (!$urlInfo) {
                $urlInfo = new Url();
                $urlInfo->url = $host;
            }

            $userFeedback->feedback += $feedback;
            $urlInfo->feedback = $feedback > 0;

            $client = new Client();
            $params = [
                'query' => [
                    'url' => $url,
                    'loc' => $userFeedback->location,
                    'feedback' => $userFeedback->feedback
                ]
            ];

            try {
                $res = $client->get("flask:80/retrain", $params);
                $location = json_decode($res->getBody()->getContents(), true)["location"];
                if ($location) {
                    $userFeedback->location = $location;
                } else {
                    return response()->json(['status' => 0, 'message' => 'Flask error'], 500);
                }
                $userFeedback->save();
                $urlInfo->save();
                return response()->json(['status' => 1, 'message' => 'Thanks for feedback'], 200);
            } catch (ClientException $exception) {
                return response()->json(['status' => 0, 'message' => 'Flask error'], 500);
            }
        } else {
            return response()->json(['status' => 0, 'message' => 'Error'], 200);
        }
    }
}
