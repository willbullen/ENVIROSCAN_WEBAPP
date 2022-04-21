from datetime import timedelta

BEAT_SCHEDULE = {
    'get-status': [
        {
            # will call update_picarro method of BackgroundJobConsumer
            'type': 'get.status',
            # message to pass to the consumer
            'message': {'testing': 'one'},
            # Every minute
            'schedule': timedelta(seconds=60)
        },
    ]
}