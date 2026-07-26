from rest_framework.throttling import UserRateThrottle


class PostCreateThrottle(UserRateThrottle):
    scope = "post_create"
