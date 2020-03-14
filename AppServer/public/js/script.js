$("#negative").click(() => {
    var url = $("input").val();
    url = url.replace(".", "%2E");
    resp = $("#response").val();
    feedback = resp === "-1" ? 1 : -1;
    $.get("/api/feedback", {url: url, feedback: feedback}, function (data, status) {
    });
});

$("#check").click(event => {
    let $this = $(event.target);
    let url = $("input").val();
    url = url.replace(".", "%2E");

    if ($this.hasClass('active') || $this.hasClass('success')) {
        return false;
    } else if ($this.hasClass('error')) {
        $this.removeClass('error animated pulse');
    }
    $this.addClass('active');
    setTimeout(() => {
        $this.addClass('loader');
    }, 125);
    $.get("/api/check", {url: url}, function (data, status) {
        if (data.status !== 0) {
            $this.removeClass('loader active');
            $this.text('Success');
            $this.addClass('success animated pulse');
            $(".modal-body").html(data.message + "\n Please provide feedback");
            $("#response").val(data.status);
            $(".hidden").click();
            setTimeout(() => {
                $this.text('Go');
                $this.removeClass('success animated pulse');
                $this.blur();
            }, 500);
        } else {
            $this.removeClass('loader active');
            $this.text('Error');
            $this.addClass('error animated pulse');
            setTimeout(() => {
                $this.text('Go');
                $this.removeClass('error animated pulse');
                $this.blur();
            }, 500);
        }


    }).fail(() => {
        $this.removeClass('loader active');
        $this.text('Error');
        $this.addClass('error animated pulse');
        setTimeout(() => {
            $this.text('Go');
            $this.removeClass('error animated pulse');
            $this.blur();
        }, 500);
    });
});

$(document).keydown((event) => {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode === '13') {
        $("#check").click();
    }
});
