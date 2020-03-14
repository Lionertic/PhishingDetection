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
                    if (data.status !== 0) {
                        $this.removeClass('loader active');
                        $this.text('Success');
                        $this.addClass('success animated pulse');
                        $(".modal-body").html(data.message + "\n Please provide feedback");
                        $(".hidden").click();
                        $("#response").val(data.status);
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

    $("#negative").click(() => {
        var url = $("input").val();
        url = url.replace(".", "%2E");
        resp = $("#response").val();
        feedback = resp === "-1" ? 1 : -1;

        $.ajax({
            url: "http://localhost/api/feedback?url=" + url + "&feedback=" + feedback,
            type: "GET",
            contentType: "application/json",
            timeout: 20000,
            accepts: "application/json",
            dataType: "json",
            crossDomain: true,
            success: function (data, status, jqXHR) {
                bkg.console.log(data);
                window.close();
            },
            error: function (jqXHR, status) {
                bkg.console.log(jqXHR);
                window.close();
            }
        });
    });

    $(document).keypress((event) => {
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if (keycode === 13) {
            $("#check").click();
        }
    });
}, false);
