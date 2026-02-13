# -*- coding: utf-8 -*-

from mod.common.mod import Mod


@Mod.Binding(name="Script_NeteaseModbLsQF4W1", version="0.0.1")
class Script_NeteaseModbLsQF4W1(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def Script_NeteaseModbLsQF4W1ServerInit(self):
        pass

    @Mod.DestroyServer()
    def Script_NeteaseModbLsQF4W1ServerDestroy(self):
        pass

    @Mod.InitClient()
    def Script_NeteaseModbLsQF4W1ClientInit(self):
        pass

    @Mod.DestroyClient()
    def Script_NeteaseModbLsQF4W1ClientDestroy(self):
        pass
