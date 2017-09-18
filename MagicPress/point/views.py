from MagicPress.point import point


@point.route('/')
def home():
    return 'hello flask'