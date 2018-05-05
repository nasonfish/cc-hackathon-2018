#!/usr/bin/env python3.4

from digest.login.user import User
from digest.containers import Organization, OrganizationPermission

#u = User("nasonfish", "d_barnes@coloradocollege.edu", "changeme1")
User.query.first().make_admin()

#u2 = User("test", "test", "test")
#u3 = User("hello", "hi", "hey")
#u4 = User("another", "person", "now")


#ccsga = Organization("CCSGA")
#music = Organization("Music Department")
#art = Organization("Art Department")
#geology = Organization("Geology Department")

#OrganizationPermission(u, music, True)
#OrganizationPermission(u2, ccsga, False)
#OrganizationPermission(u3, art, True)
#OrganizationPermission(u4, geology, True)
