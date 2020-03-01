<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class UserFeedback extends Model
{
    protected $table = "UserFeedback";

    public function url($url)
    {
        return Url::where('url', $url)->first();
    }
}
