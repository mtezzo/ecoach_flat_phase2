from django.contrib.auth.models import User
from .models import Source1
from .models import Common1

def configure_source_data(username):
    # THIS IS A HACK TO ENSURE ALL THE ENTRY POINTS ADD THE RIGHT SOURCE ROW FOR A USER
    ret = False
    # ensure the user entry
    me = User.objects.filter(username=username)
    if len(me) < 1:
        me = User(username=username)
        me.save() 
    else:
        me = me[0]

    # ensure the source entry
    ss = Source1.objects.filter(user_id=me)
    if len(ss) < 1:
        # After the enrollment period add a copy of Albert Einstein's data to non-enrolled users 
        ss = Source1(user_id=me)
        ss.save()
        ret = True
    
    ss = Common1.objects.filter(user_id=me)
    if len(ss) < 1:
        # After the enrollment period add a copy of Albert Einstein's data to non-enrolled users 
        ss = Common1(user_id=me)
        ss.save()
        ret = True

    return ret
        
 
        
 
            
 

