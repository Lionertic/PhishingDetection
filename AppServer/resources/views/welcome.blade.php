<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Laravel</title>

        <!-- Fonts -->
        <link href="https://fonts.googleapis.com/css?family=Nunito:200,600" rel="stylesheet">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

        <!-- Styles -->
        <style>
            html, body {
                background-color: #fff;
                color: #636b6f;
                font-family: 'Nunito', sans-serif;
                font-weight: 200;
                height: 100vh;
                margin: 0;
            }

            .full-height {
                height: 100vh;
            }

            .flex-center {
                align-items: center;
                display: flex;
                justify-content: center;
            }

            .position-ref {
                position: relative;
            }

            .content {
                text-align: center;
            }

            .title {
                font-size: 84px;
            }

            .links > a {
                color: #636b6f;
                padding: 0 25px;
                font-size: 13px;
                font-weight: 600;
                letter-spacing: .1rem;
                text-decoration: none;
                text-transform: uppercase;
            }

            .m-b-md {
                margin-bottom: 30px;
            }
        </style>
    </head>
    <body>
    <div class="flex-center position-ref full-height">
        <div class="content">
            <div class="title m-b-md">
                Detect Phishing
            </div>
            <div class="links">
                <label for="exampleInputEmail1">URL</label>
                <input label="url" type="text" class="form-control" id="urlInput" placeholder="https://www.google.com/">
                <button onclick="check();">CHECK</button>
            </div>
        </div>
        <!-- Button trigger modal -->
<button type="button" class="hidden" class="btn btn-primary btn-lg" data-toggle="modal" data-target="#myModal">
</button>

<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myModalLabel">Modal title</h4>
      </div>
      <div class="modal-body">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" id="positive" data-dismiss="modal">Yes</button>
        <button type="button" class="btn btn-primary" id="negative" data-dismiss="modal">No</button>
      </div>
    </div>
  </div>
</div>
    </div>
    </body>
    <script>
        function check() {
            var url = $("input").val();
            url = url.replace(".", "%2E");
            $.get("/api/check", {url: url}, function (data, status) {
                if (status === "success"){
                    $(".modal-body").html(data.message + "\n Please provide feedback")
                    $(".hidden").click()
                }
            });
        }
        $("#positive").click(()=>{
            feedback(1)
        })
        $("#negative").click(()=>{
            feedback(-1)
        })
        function feedback(feedback) {
            var url = $("input").val();
            url = url.replace(".", "%2E");
            $.get("/api/feedback", {url: url,feedback:feedback}, function (data, status) {});
        }
    </script>
</html>
