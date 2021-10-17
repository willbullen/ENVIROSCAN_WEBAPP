from datetime import timedelta

BEAT_SCHEDULE = {
    'testing-print': [
        {
            # will call update_picarro method of BackgroundJobConsumer
            'type': 'test.print',
            # message to pass to the consumer
            'message': {'testing': 'one'},
            # Every minute
            'schedule': timedelta(seconds=60)
        },
    ]
}