chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
    if (changeInfo.status == 'loading'  && tab.active) {
        $.ajax({
            url:  "http://localhost/api/check?url=" + tab.url,
            type: "GET",
            contentType: "application/json",
            timeout: 5000,
            accepts:"application/json",
            dataType:"json",
            crossDomain : true,
            success: function (data, status, jqXHR) {
                if (data.status == 201) {
                    alert("error "+data.message);
                }
            },
            error: function (jqXHR, status) {
            }
        });
    }
})