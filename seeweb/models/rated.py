from sqlalchemy import Column, Integer


def rating_to_float(rating):
    frac = (rating / 100.) * 5.
    return int(frac * 10) / 10.


def float_to_rating(val):
    return int(val / 5. * 100)


class Rated(object):
    """Abstract class used for all objects with a rating
    """
    rating_value = Column(Integer, default=50)
    rating_doc = Column(Integer, default=50)
    rating_install = Column(Integer, default=50)
    rating_usage = Column(Integer, default=50)

    def format_ratings(self):
        """List ratings in rated object

        Return an ordered list of rating names, rating score
        """
        ratings = [("Value", rating_to_float(self.rating_value)),
                   ("Documentation", rating_to_float(self.rating_doc)),
                   ("Installation", rating_to_float(self.rating_install)),
                   ("Usage", rating_to_float(self.rating_usage))]

        return ratings

    def affect_ratings(self, ratings):
        """Affect ratings to an object.

        Inverse of 'format_ratings' function.
        """
        ratings = dict((name.lower(), rating) for name, rating in ratings)
        self.rating_value = float_to_rating(ratings["value"])
        self.rating_doc = float_to_rating(ratings["documentation"])
        self.rating_install = float_to_rating(ratings["installation"])
        self.rating_usage = float_to_rating(ratings["usage"])
