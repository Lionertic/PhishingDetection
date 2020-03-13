<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Url extends Model
{
    protected $primaryKey = 'id';
    protected $table = "Urls";

    public function userFeedback()
    {
        return $this->hasOne('App\UserFeedback');
    }
}
