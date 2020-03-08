chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
    let url = tab.url;
    url = url.replace(".", "%2E");

    if (changeInfo.status === 'loading' && tab.active) {
        $.ajax({
            url: "http://localhost/api/check?url=" + url,
            type: "GET",
            contentType: "application/json",
            timeout: 20000,
            accepts: "application/json",
            dataType: "json",
            crossDomain: true,
            success: function (data, status, jqXHR) {
                if (data.message !== "Its good url") {
                    alert("error " + data.message);
                }
            },
            error: function (jqXHR, status) {
                console.log(jqXHR)
            }
        });
    }
});