USERS = {'editor': 'editor',
         'viewer': 'viewer'}
GROUPS = {'editor': ['group:editors']}


def groupfinder(userid, request):
    print "GROUP", userid, "\n" * 10
    if userid == 'revesansparole':
        return 'admin'
