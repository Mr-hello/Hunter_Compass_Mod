# -*- coding: utf-8 -*-

from mod.common.mod import Mod

import mod.server.extraServerApi as serverApi

import mod.client.extraClientApi as clientApi


@Mod.Binding(name="hunter_player_compass_mod", version="0.0.1")
class hunter_player_compass_mod(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def hunter_player_compass_modServerInit(self):
        print("serverApi.RegisterSystem")
        serverApi.RegisterSystem('hunter_player_compass_mod', 'PlayerCompassServerSystem', 'hunter_player_compass_mod.PlayerCompassServerSystem.PlayerCompassServerSystem')

    @Mod.DestroyServer()
    def hunter_player_compass_modServerDestroy(self):
        pass

    @Mod.InitClient()
    def hunter_player_compass_modClientInit(self):
        clientApi.RegisterSystem("hunter_player_compass_mod", "PlayerCompassClientSystem", "hunter_player_compass_mod.PlayerCompassClientSystem.PlayerCompassClientSystem")

    @Mod.DestroyClient()
    def hunter_player_compass_modClientDestroy(self):
        pass
