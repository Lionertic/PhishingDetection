$("#positive").click(() => {
    feedback(1)
});

$("#negative").click(() => {
    feedback(-1)
});

function feedback(feedback) {
    var url = $("input").val();
    url = url.replace(".", "%2E");
    $.get("/api/feedback", {url: url, feedback: feedback}, function (data, status) {
    });
}

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
        if (status === "success") {
            $this.removeClass('loader active');
            $this.text('Success');
            $this.addClass('success animated pulse');
            $(".modal-body").html(data.message + "\n Please provide feedback");
            $(".hidden").click()
        } else {
            $this.removeClass('loader active');
            $this.text('Error');
            $this.addClass('error animated pulse');
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
