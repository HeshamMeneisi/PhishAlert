cache = true
function checkResponse(response, tid)
{
	if(response == "OK")
		icon = "safe.png"
	else
		icon = "risky.png"
	chrome.browserAction.setIcon({
    path : icon,
    tabId: tid
	});
}
function checkCurrentTab()
{
	chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
		var url = tabs[0].url;
		chrome.browserAction.setIcon({
		path : "checking.png",
		tabId: tabs[0].id
		});
		if(cache && localStorage[url]){
			checkResponse(localStorage[url], tabs[0].id)
			return
		}
		console.log(url)
        $.ajax({
            url: 'http://127.0.0.1:5000/checkURL',
            data: {url:url},
            type: 'POST',
            success: function(response) {
				localStorage[url] = response
                checkResponse(response, tabs[0].id);
            },
            error: function(error) {
				localStorage[url] = response
                checkResponse(error, tabs[0].id);
            }
		});
	});
}
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
	if (changeInfo.status == 'complete') {
		checkCurrentTab();
	}
});
chrome.tabs.onActivated.addListener(function(activeInfo){
	checkCurrentTab();
});