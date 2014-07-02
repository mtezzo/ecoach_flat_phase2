
// Google Analytics 
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

jQuery(document).ready(function($){
    if(CONF.production()) 
        ga('create', 'UA-37331371-4', 'umich.edu');
    else
        ga('create', 'UA-37331371-3', 'umich.edu');
});

// handles pushing log events both to our internal logging api and google analytics
var logger = {
    page_dynamics: function(cat, action) {
        // log event
        var logCategory = cat;
        var logAction = action;
        var elog = {}
        elog.eventCategory = logCategory;
        elog.eventAction = logAction;
        logger.logEvent(false, elog); 
    },
    logEvent: function(pageview, elog, json) {
        elog = elog || {}
        // configure data
        var locationWithHash = (window.location.pathname + window.location.search + window.location.hash);
        var href = CONF.logger_url;
        jQuery.ajax({
            //TODO: change this to POST once you have a working endpoint
            type: "GET", 
            url: href,
            data: { 
                url: locationWithHash,
                category: elog.eventCategory || 'null',
                action: elog.eventAction || 'null',
                label: elog.eventLabel || 'null',
                value: elog.eventValue || 0,
                json: JSON.stringify(json) || '{}'
            }
        });
        //NOTE: per GA terms of service username cannot be sent to GA 
        if (pageview){
            ga('send', 'pageview', {
                'page': locationWithHash
            });
        }
        if (elog){
            ga('send', 'event', elog);
        }
    }
};


