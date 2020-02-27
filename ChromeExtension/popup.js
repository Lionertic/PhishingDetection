document.addEventListener('DOMContentLoaded', function() {
    var checkPageButton = document.getElementById('checkPage');
    checkPageButton.addEventListener('click', function() {
      chrome.tabs.getSelected(null, function(tab) {
          var url = $("#urls").val()
          if ( !url ) {
              url = tab.url
          }
        $.ajax({
            url:  "http://localhost/api/check?url=" + url,
            type: "GET",
            contentType: "application/json",
            timeout: 5000,
            accepts:"application/json",
            dataType:"json",
            crossDomain : true,
            success: function (data, status, jqXHR) {
                if (data.status == 201) {
                    $("#resp").append("error "+data.message)
                }
            },
            error: function (jqXHR, status) {
            }
        });
      });
    }, false);
  }, false);