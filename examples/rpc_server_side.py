#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2011  Dann Martens
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmpp.plugins.xep_0009.remote import Endpoint
from sleekxmpp.plugins.xep_0009.remote import remote
from sleekxmpp.plugins.xep_0009.remote import Remote
from sleekxmpp.plugins.xep_0009.remote import ANY_ALL
from sleekxmpp.plugins.xep_0009.remote import ACL
import threading

class Thermostat(Endpoint):

    def FQN(self):
        return 'thermostat'

    def __init__(self, initial_temperature):
        self._temperature = initial_temperature
        self._event = threading.Event()

    @remote
    def set_temperature(self, temperature):
        print("Setting temperature to %s" % temperature)
        self._temperature = temperature

    @remote
    def get_temperature(self):
        return self._temperature

    @remote(False)
    def release(self):
        self._event.set()

    def wait_for_release(self):
        self._event.wait()



def main():

    session = Remote.new_session('thermostat@ihijixmpp/rpc', '*****')

    #thermostat = session.new_handler(ANY_ALL, Thermostat, 18)
    thermostat = session.new_handler([(ACL.ALLOW, 'operator@ihijixmpp', 'thermostat.set_temperature'),
                                      (ACL.DENY, '*', '*')],
                                     Thermostat, 18)

    thermostat.wait_for_release()

    session.close()

if __name__ == '__main__':
    main()

