def score(val):
    frac = (val / 100.) * 5.
    return int(frac * 10) / 10.


def format_ratings(project):
    """Format ratings in project.

    Return an ordered list of rating names, rating score
    """
    ratings = [("Value", score(project.rating_value)),
               ("Documentation", score(project.rating_doc)),
               ("Installation", score(project.rating_install)),
               ("Usage", score(project.rating_usage))]

    return ratings
