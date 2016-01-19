def rating_to_float(rating):
    frac = (rating / 100.) * 5.
    return int(frac * 10) / 10.


def float_to_rating(val):
    return int(val / 5. * 100)


def format_ratings(rated):
    """List ratings in rated object

    Return an ordered list of rating names, rating score
    """
    ratings = [("Value", rating_to_float(rated.rating_value)),
               ("Documentation", rating_to_float(rated.rating_doc)),
               ("Installation", rating_to_float(rated.rating_install)),
               ("Usage", rating_to_float(rated.rating_usage))]

    return ratings
