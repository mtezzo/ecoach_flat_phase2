from django.core.urlresolvers import reverse

def steps_nav(user, selected):
    
    all_steps = [
            #'text'         
            #   'styling_class(es)',    
            #       'links_to'
            #           'permission_required'
            #               'selected'
            ['1. Create BCC', 
                '',  
                    reverse('myemailer:bcc'),
                        'staff',
                            'bcc',

            ],
            ['2. Draft Message', 
                '',  
                    reverse('myemailer:draft'),
                        'staff',
                            'draft',
            ],
            ['3. Send/Save Email', 
                '',  
                    reverse('myemailer:send'),
                        'staff',
                            'send',
            ],
            ['4. Archive', 
                '',  
                    reverse('myemailer:archive'),
                        'staff',
                            'archive',
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

