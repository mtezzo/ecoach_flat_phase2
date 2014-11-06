import re

class NavInfo:

    def __init__(self, requested):
        self.m_subsite = '/'
        self.m_requested = [] # not initializing this killed me for 2 hours!
        self.m_menu = dict()

        # main menu tab items (can be a super set, just has to be in order)
        self.m_tabs = ([
        "Coached Courses",
        "About E<sup>2</sup>Coach",
        "Tailoring Example",
        "Coaching Team",
        "Press",
        "Contact",
        ])

        # nav data structure to populate
        for tt in self.m_tabs:
            self.m_menu[tt] = []

        # STRUCTURE ==> menu["TAB_TEXT"].append( ["SIDE_TEXT" "UNIQUE_URL"])
        # ---everyone must have one entry---
       
        self.m_menu["Coached Courses"].append(["", "mycourses"])
        self.m_menu["About E<sup>2</sup>Coach"].append(["", "about"])
        self.m_menu["Tailoring Example"].append(["", "tailoring"])
        self.m_menu["Coaching Team"].append(["", "team"])
        self.m_menu["Press"].append(["", "press"])
        self.m_menu["Contact"].append(["", "contact"])

        # prune out the dead tabs
        tabs = dict()
        for tt in self.m_menu:
            if len(self.m_menu[tt]) > 0:
                # save requested url
                tabs[tt] = self.m_menu[tt]
        self.m_menu = tabs 

        # rustle up the menu selection
        self.map_requested(requested)

    def map_requested(self, req):
        req = str(req.lstrip('/'))
        #req = req[len(self.m_subsite):]
        re1 = re.compile(r'^.*\/')
        res1 = re1.search(req)
        try:
            req = str(res1.group()).rstrip('/')
        except:
            pass

        for tab in self.m_menu:
            ii = 0
            for sub in self.m_menu[tab]:
                if req == sub[1]:
                    # hopefully we find the request, save the tab and number of sub
                    self.m_requested.append(tab)
                    self.m_requested.append(ii)
                    self.m_requested.append(sub[1])
                    return
                ii += 1
        # everyone has a tab, if we found no match default to it's first element
        self.m_requested.append(self.m_tabs[0])
        self.m_requested.append(0)
        self.m_requested.append("/")
           
    def side_menu(self):
        # this nav structure sort of assumes single unique string identifiers for resources....
        tab = self.m_requested[0]
        sub = self.m_requested[1]
        subs = []
        if len(self.m_menu[tab]) > 1:
            for ss in self.m_menu[tab]:
                tab = self.m_requested[0]
                sub = self.m_requested[1]
                comp = self.m_menu[tab][sub][1]
                if ss[1] == comp:
                    css = "current_side_item"
                else:
                    css = "side_item"
                href = self.m_subsite + ss[1]
                txt = ss[0]
                subs.append([txt, css, href])
        return subs

    def decide_template(self):
        sides = self.sidemenu()
        # greater than two because if there's only one sub we don't display/acknowledge a side menu
        if len(sides) > 1:
            return True
        else:
            return False

    def main_menu(self):
        #self.menu["Home"].append([" ", "JanX_Home", "Advice_X_Home"])
        # [word, class, href]
        # [key, key=selected, sub[0]]
        tab = self.m_requested[0]
        sub = self.m_requested[1]
        tabs = [] 
        for tt in self.m_menu: 
            if tt == tab: # mark the one you're on
                css = "current_page_item"
            else:
                css = "page_item" # leave the rest
            href = self.m_subsite + self.m_menu[tt][0][1]
            txt = tt
            tabs.append([txt, css, href])

        # sort/set the order
        ret = []
        for tt in self.m_tabs: 
            for ii in tabs:
                if ii[0] == tt:
                    ret.append(ii)
                    break
        return ret
          

