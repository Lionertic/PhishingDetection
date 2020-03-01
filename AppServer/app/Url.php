<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Url extends Model
{
    protected $primaryKey = 'id';
    private $url;
    protected $table = "Urls";

    public function userFeedback()
    {
        return $this->hasOne('App\UserFeedback');
    }
}
