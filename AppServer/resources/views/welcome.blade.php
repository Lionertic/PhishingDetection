<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Phishing Detector</title>

    <!-- Fonts -->
    <link rel="icon" href="{{ asset('favicon.png') }}" type="image/x-icon"/>
    <link href="https://fonts.googleapis.com/css?family=Nunito:200,600" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
    <link href="{{ asset('/css/style.css') }}" rel="stylesheet">

</head>
<body>
<div class="flex-center position-ref full-height">
    <div class="content">
        <div class="title m-b-md">
            Detect Phishing
        </div>
        <div class="links">
            <input type="text" class="form-control" id="urlInput" placeholder="https://www.google.com/"><br>
            <button type="submit" id="check">Go</button>
        </div>
    </div>
    <!-- Button trigger modal -->
    <button type="button" class=" hidden btn btn-primary btn-lg" data-toggle="modal" data-target="#myModal"></button>
    <input type="hidden" id="response">
    <!-- Modal -->
    <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span
                            aria-hidden="true">&times;</span></button>
                    <h4 class="modal-title" id="myModalLabel">Modal title</h4>
                </div>
                <div class="modal-body">
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" id="positive" data-dismiss="modal">Correct</button>
                    <button type="button" class="btn btn-primary" id="negative" data-dismiss="modal">Wrong</button>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
<script src="{{ asset('/js/script.js') }}"></script>
</html>
