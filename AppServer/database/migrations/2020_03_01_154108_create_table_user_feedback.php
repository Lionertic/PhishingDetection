<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateTableUserFeedback extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('UserFeedback', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('url', 500)->unique();
            $table->tinyInteger('feedback')->default(0);
            $table->timestamps();
            $table->foreign("url")->references("url")->on("Urls")->onDelete("cascade");
        });

        Schema::enableForeignKeyConstraints();
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('table_user_feedback');
    }
}
