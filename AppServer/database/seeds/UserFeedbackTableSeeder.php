<?php

use Illuminate\Database\Seeder;

class UserFeedbackTableSeeder extends Seeder
{

    /**
     * Auto generated seed file
     *
     * @return void
     */
    public function run()
    {
        DB::table('UserFeedback')->delete();
    }
}
