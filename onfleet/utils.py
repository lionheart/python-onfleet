import datetime

try:
    import pytz
    utc = pytz.utc
except ImportError:
    ZERO = datetime.timedelta(0)

    class UTC(datetime.tzinfo):
      def utcoffset(self, dt):
        return ZERO
      def tzname(self, dt):
        return "UTC"
      def dst(self, dt):
        return ZERO

    utc = UTC()

def unix_time(dt):
    epoch = datetime.datetime.fromtimestamp(0, tz=utc)
    delta = dt - epoch
    # Return milliseconds
    return delta.total_seconds() * 1000.0
