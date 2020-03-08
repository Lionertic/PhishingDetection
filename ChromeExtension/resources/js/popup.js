document.addEventListener('DOMContentLoaded', function () {
    let $this = $("#check");
    let outerUrl;
    $this.click(() => {
        chrome.tabs.getSelected(null, (tab) => {
            let url = $("#urlInput").val();

            if (!url) {
                url = tab.url
            }
            if ($this.hasClass('active') || $this.hasClass('success')) {
                return false;
            } else if ($this.hasClass('error')) {
                $this.removeClass('error animated pulse');
            }
            $this.addClass('active');
            setTimeout(() => {
                $this.addClass('loader');
            }, 125);
            outerUrl = url;
            $.ajax({
                url: "http://localhost/api/check?url=" + url,
                type: "GET",
                contentType: "application/json",
                timeout: 20000,
                accepts: "application/json",
                dataType: "json",
                crossDomain: true,
                success: function (data, status, jqXHR) {
                    if (status === "success") {
                        $this.removeClass('loader active');
                        $this.text('Success');
                        $this.addClass('success animated pulse');
                        $(".modal-body").html(data.message + "\n Please provide feedback");
                        $(".hidden").click();
                        $("#resp").append("error " + data.message)
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
                },
                error: function (jqXHR, status) {
                    $this.removeClass('loader active');
                    $this.text('Error');
                    $this.addClass('error animated pulse');
                    setTimeout(() => {
                        $this.text('Go');
                        $this.removeClass('error animated pulse');
                        $this.blur();
                    }, 500);
                }
            });
        });
    });
    var bkg = chrome.extension.getBackgroundPage();
    bkg.console.log($("#positive"));
    $("#positive").click(() => {
        feedback(outerUrl, 1)
    });

    $("#negative").click(() => {
        feedback(outerUrl, -1)
    });
}, false);

function feedback(url, feedback) {
    window.close();
    $.ajax({
        url: "http://localhost/api/feedback?url=" + url + "&feedback=" + feedback,
        type: "GET",
        contentType: "application/json",
        timeout: 20000,
        accepts: "application/json",
        dataType: "json",
        crossDomain: true,
        success: function (data, status, jqXHR) {
        },
        error: function (jqXHR, status) {
        }
    });
}
