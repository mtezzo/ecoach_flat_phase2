from django.utils.decorators import method_decorator

from djangotailoring.tracking.decorators import log_page_view

class LogPageViewMixin(object):
    """A simple mix-in class to write an event on every request to the view.
    events are written using the `log_page_view` decorator in
    `djangotailoring.tracking.decorators`.
    """
    @method_decorator(log_page_view)
    def dispatch(self, request, *args, **kwargs):
        return super(LogPageViewMixin, self).dispatch(request, *args, **kwargs)
    

