

def groupfinder(userid, request):
    print "GROUP", userid, "\n" * 10
    if userid == 'revesansparole':
        return ['group:admins']
