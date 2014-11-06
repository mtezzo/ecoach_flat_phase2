from django.core.urlresolvers import reverse
from django.conf import settings

def main_nav(user, selected):
    
    see_from_listA  = ['student_linkback', 'static_linkback', 'coaches', 'student_view', 'staff_view']
    see_from_listB  = ['student_linkback', 'student_view', 'staff_view']

    all_main = [
            #'text'         
            #   'styling_class(es)',    
            #       'links_to'
            #           'permission_required'
            #               '[seen_from]'
            #                   'selected'
            #                       subs
            ['Coaches', 
                '',  
                    reverse('myselector:course_select'),
                        'any',
                            see_from_listA,
                                'coaches',
                                    [],

            ],
            ['Messages', 
                '',  
                    #reverse('home'),
                    reverse('default:default'),
                    #reverse('default', kwargs={'msg_id':''}),
                    #reverse('myselector:course_select'),
                        'staff',
                            see_from_listA,
                                'student_view',
                                    [],
            ],
            ['Staff', 
                '',  
                    reverse('tourney:staff'),
                        'staff',
                            see_from_listB,
                                'staff_view',
                                    tasks_nav(user, selected),
            ],            [''.join(['Logout: ', user.username]),      
                '', 
                    reverse('myselector:mylogout'),
                        'any',
                            see_from_listA,
                                'never',
                                    [],
            ]
        ]

    main_nav = []
    for nn in all_main:
        # style the selected option
        if nn[5] == selected:
            nn[1] = 'current'
        # sceen from this page type?
        if selected in nn[4]:
            # permission?
            if nn[3] == 'any':
                main_nav.append(nn)
            elif nn[3] == 'staff' and user.is_staff:
                main_nav.append(nn)

    return main_nav


def tasks_nav(user, selected):
    
    all_tasks = [
            #'text'         
            #   'styling_class(es)',    
            #       'links_to'
            #           'permission_required'
            #               'selected' # looks irrlivant to staff nav...
            ['Tourneys', 
                '',  
                    reverse('tourney:new_bracket'),
                        'staff',
                            'tourney',
            ],
            ['Emailer', 
                '',  
                    reverse('myemailer:default'),
                        'staff',
                            'emailer',
            ],
        ]
    tasks_nav = []
    for nn in all_tasks:
        # style the selected option
        if nn[4] == selected:
            nn[1] = 'current'
        # permission?
        if nn[3] == 'any':
            tasks_nav.append(nn)
        elif nn[3] == 'staff' and user.is_staff:
            tasks_nav.append(nn)

    return tasks_nav


