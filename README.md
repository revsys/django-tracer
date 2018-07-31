django-tracer
========================
[![Build Status](https://travis-ci.org/revsys/django-tracer.svg?branch=master)](https://travis-ci.org/revsys/django-tracer)

Generate a UUID for all requests to Django to be used in logging and error reporting for traceability. 

# Why? 

Why would you want to use this silly little thing? Well in a containerized, orchestrated, microservice world with centralized logging it's often hard to figure out where things have gone wrong.  

This little middleware adds a UUID to the normal Django request object which you can use to add to add to things like: 

- All of your log messages
- Error reports to Sentry/Rollbar/etc
- Pass along to other internal services

Along with generating and attaching a UUID to each request, the middleware also automatically adds the UUID to the response headers as `X-Request-ID` so anyone consuming your responses, say as an API, can use that as a reference point for reporting errors back to you. 

# Installation

Add `tracer` to `INSTALLED_APPS` in your settings. 

Then add `tracer.middleware.RequestID` to the top of your `MIDDLEWARE` settings. 

# Usage with standard logging

```
import logging

from django.http import HttpResponse

logger = logging.getLogger(__name__)

def some_view(request):
    """ simple log example """
    logger.info("Whee!", extra={'request_id': request.id})
    return HttpResponse("example content")
```

## Other ways to use this Request ID

There are several other places you may consider wanting to use the ID to improve traceability: 

- Pass it as an argument to any Celery tasks you generate so there is a clear path between the incoming request and the tasks that were generated from it
- Pass it as a header or argument to other internal APIs or services 
- Attach it to a bound [structlog](http://www.structlog.org/) object so it is always included in your log output

# Thanks! 

Special thanks to [Rolf Håvard Blindheim](https://github.com/rhblind) for graciously turning over the name `django-tracer` to us to be able to use it for this project. 

## Need help?

[REVSYS](http://www.revsys.com?utm_medium=github&utm_source=django-tracer) can help with your Python, Django, and infrastructure projects. If you have a question about this project, please open a GitHub issue. If you love us and want to keep track of our goings-on, here's where you can find us online:

<a href="https://revsys.com?utm_medium=github&utm_source=django-tracer"><img src="https://pbs.twimg.com/profile_images/915928618840285185/sUdRGIn1_400x400.jpg" height="50" /></a>
<a href="https://twitter.com/revsys"><img src="https://cdn1.iconfinder.com/data/icons/new_twitter_icon/256/bird_twitter_new_simple.png" height="43" /></a>
<a href="https://www.facebook.com/revsysllc/"><img src="https://cdn3.iconfinder.com/data/icons/picons-social/57/06-facebook-512.png" height="50" /></a>
<a href="https://github.com/revsys/"><img src="https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png" height="53" /></a>
<a href="https://gitlab.com/revsys"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/GitLab_Logo.svg/2000px-GitLab_Logo.svg.png" height="44" /></a>
