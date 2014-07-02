from django.core.urlresolvers import reverse

see_from_listA  = ['student_linkback', 'static_linkback', 'coaches', 'student_view', 'staff_view']
see_from_listB  = ['student_linkback', 'student_view', 'staff_view']

def selector_main_nav(user, selected):

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
                    '', #reverse('myselector:course_select'),
                        'any',
                            see_from_listA,
                                'coaches',
                                    [],

            ],
            ['Staff View', 
                '',  
                    '', #reverse('mystaff:default'),
                        'staff',
                            see_from_listB,
                                'staff_view',
                                    selector_tasks_nav(user, selected),

            ],
            [''.join(['Logout: ', user.username]),      
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

def selector_tasks_nav(user, selected):
    
    all_tasks = [
            #'text'         
            #   'styling_class(es)',    
            #       'links_to'
            #           'permission_required'
            #               'selected' # looks irrlivant to staff nav...
            """
            ['Publisher', 
                '',  
                    reverse('mypublisher:default'),
                        'staff',
                            'publisher',

            ],
            """
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


