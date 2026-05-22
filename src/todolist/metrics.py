from prometheus_client import Counter, generate_latest, REGISTRY
from django.http import HttpResponse


# Create counters for GET and POST requests
get_requests_counter = Counter(
    'http_get_requests_total',
    'Total number of GET requests',
    ['method']
)

post_requests_counter = Counter(
    'http_post_requests_total',
    'Total number of POST requests',
    ['method']
)


class PrometheusMetricsMiddleware:
    """Middleware to track GET and POST requests"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Track the request
        if request.method == 'GET':
            get_requests_counter.labels(method='GET').inc()
        elif request.method == 'POST':
            post_requests_counter.labels(method='POST').inc()
        
        response = self.get_response(request)
        return response


def metrics_view(request):
    """View that returns Prometheus metrics"""
    metrics = generate_latest(REGISTRY)
    return HttpResponse(metrics, content_type='text/plain; charset=utf-8')
