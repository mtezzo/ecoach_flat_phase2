from django.core.urlresolvers import reverse

def steps_nav(user, selected):
    all_steps = [
            #'text'         
            #   'styling_class(es)',    
            #       'links_to'
            #           'permission_required'
            #               'selected'
            ['Your Tail', 
                '',  
                    reverse('myusage:your_tail'),
                        'staff',
                            'your_tail'
            ],
            ["Everyone's Tail", 
                '',  
                    reverse('myusage:everyone_tail'),
                        'staff',
                            'eveyone_tail'
            ],
            ["Usage Vectors", 
                '',  
                    reverse('myusage:usage_vector'),
                        'staff',
                            'usage_vector'
            ]
        ]

    steps_nav = []
    for nn in all_steps:
        # style the selected option
        if nn[4] == selected:
            nn[1] = 'current'
        # permission?
        if nn[3] == 'any':
            steps_nav.append(nn)
        elif nn[3] == 'staff' and user.is_staff:
            steps_nav.append(nn)

    return steps_nav

