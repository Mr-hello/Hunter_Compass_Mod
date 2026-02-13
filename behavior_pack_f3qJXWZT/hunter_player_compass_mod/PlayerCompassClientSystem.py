# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from HunterPlayerCompassScreen import HunterPlayerCompassScreen
ClientSystem = clientApi.GetClientSystemCls()


class PlayerCompassClientSystem(ClientSystem):

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.HunterPlayerCompassUINode = None
        self.current_path = ""
        self.count = 0
        self.old_path = "/main/menu_panel/image_panel/image(0)"

        self.messagebox_background_image_path = "/menu_panel/messagebox_panel/background_image"
        self.messagebox_box_image_path = "/menu_panel/messagebox_panel/box_image"
        self.messagebox_menu_title_path = "/menu_panel/messagebox_panel/menu_title"
        self.settingbox_background_image_path = "/menu_panel/settingbox_panel/background_image"
        self.settingbox_box_image_path = "/menu_panel/settingbox_panel/box_image"
        self.settingbox_menu_title_path = "/menu_panel/settingbox_panel/menu_title"
        self.settingbox_close_button_path = "/menu_panel/settingbox_panel/button(0)"
        self.image_panel_path = "/menu_panel/image_panel_panel"
        self.messagebox_panel_path = "/menu_panel/messagebox_panel"
        self.settingbox_panel_path = "/menu_panel/settingbox_panel"

        self.enable_coordinate_display = 1
        self.enable_distance_display = 1
        self.enable_keep_compass = 1
        self.enable_menu_button = 1

        self.levelid = ""
        self.EntityTypeEnum = clientApi.GetMinecraftEnum().EntityType
        self.boat_type = self.EntityTypeEnum.BoatRideable

        self.ListenEvent()

    def ListenEvent(self):
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassServerSystem", "ChangeCompassTexture", self,
                            self.ChangeCompassTexture)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "UiInitFinished", self,
                            self.OnUIInitFinished)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnScriptTickClient", self,
                            self.SendBodyRot)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnScriptTickClient", self,
                            self.GetRiderId)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassServerSystem", "OpenCompassMenu", self,
                            self.OpenCompassMenu)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassServerSystem", "EnableKeepCompass", self,
                            self.EnableKeepCompass)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassServerSystem", "EnableDistanceDisplay", self,
                            self.EnableDistanceDisplay)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassServerSystem", "EnableCoordinateDisplay", self,
                            self.EnableCoordinateDisplay)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassServerSystem", "EnableMenuButton", self,
                            self.EnableMenuButton)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassServerSystem", "ReceiveSettingData", self,
                            self.ReceiveSettingData)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassServerSystem", "SetImagePanelVisible", self,
                            self.SetImagePanelVisible)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassServerSystem", "SetImagePanelInvisible", self,
                            self.SetImagePanelInvisible)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassServerSystem", "ReceiveLevelIdData", self,
                            self.ReceiveLevelIdData)

    def GetRiderId(self):
        player_id = clientApi.GetLocalPlayerId()
        get_rider_Id_comp = clientApi.GetEngineCompFactory().CreateGame(self.levelid)
        rider_Id = get_rider_Id_comp.GetRiderId(player_id)
        engine_type_comp = clientApi.GetEngineCompFactory().CreateEngineType(rider_Id)
        entity_type = engine_type_comp.GetEngineType()
        # print(entity_type)
        if entity_type == self.boat_type or entity_type == 218:
            is_in_boat = 1
            is_in_boat_dic = {"player_id": player_id, "is_in_boat": is_in_boat}
            clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
            clientSystem.NotifyToServer("IsInBoat", is_in_boat_dic)
        else:
            is_in_boat = 0
            is_in_boat_dic = {"player_id": player_id, "is_in_boat": is_in_boat}
            clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
            clientSystem.NotifyToServer("IsInBoat", is_in_boat_dic)

    def SendBodyRot(self):
        # print(2222)
        # print(self.levelid)
        player_id = clientApi.GetLocalPlayerId()
        body_rot_comp = clientApi.GetEngineCompFactory().CreateRot(player_id)
        body_rot = (body_rot_comp.GetBodyRot())
        body_rot_dic = {"player_id": player_id, "body_rot": body_rot}
        clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
        clientSystem.NotifyToServer("ReceiveBodyRot",  body_rot_dic)

    def ReceiveLevelIdData(self, levelid_dic):
        self.levelid = levelid_dic["levelid"]
        print("世界ID为：" + self.levelid)

    def ReceiveSettingData(self, data):
        self.enable_coordinate_display = data["enable_coordinate_display"]
        self.enable_distance_display = data["enable_distance_display"]
        self.enable_keep_compass = data["enable_keep_compass"]
        self.enable_menu_button = data["enable_menu_button"]
        enable_keep_compass_dict = {"enable_keep_compass": self.enable_keep_compass}
        enable_distance_display_dict = {"enable_distance_display": self.enable_distance_display}
        enable_coordinate_display_dict = {"enable_coordinate_display": self.enable_coordinate_display}
        enable_menu_button_dict = {"enable_menu_button": self.enable_menu_button}
        print("已接收服务端设置数据")
        self.EnableKeepCompass(enable_keep_compass_dict)
        self.EnableDistanceDisplay(enable_distance_display_dict)
        self.EnableCoordinateDisplay(enable_coordinate_display_dict)
        self.EnableMenuButton(enable_menu_button_dict)

    def EnableKeepCompass(self, dic):
        print("准备向UI发送请求")
        HunterPlayerCompassScreen.ChangeToggleState(self.HunterPlayerCompassUINode, dic)
        print("已完成向UI发送请求")

    def EnableDistanceDisplay(self, dic):
        print("准备向UI发送请求")
        HunterPlayerCompassScreen.ChangeToggleState(self.HunterPlayerCompassUINode, dic)
        print("已完成向UI发送请求")

    def EnableCoordinateDisplay(self, dic):
        print("准备向UI发送请求")
        HunterPlayerCompassScreen.ChangeToggleState(self.HunterPlayerCompassUINode, dic)
        print("已完成向UI发送请求")

    def EnableMenuButton(self, dic):
        print("准备向UI发送请求")
        HunterPlayerCompassScreen.ChangeToggleState(self.HunterPlayerCompassUINode, dic)
        print("已完成向UI发送请求")

    def OpenCompassMenu(self, dic):
        print(11111111111111)
        # player_id = clientApi.GetLocalPlayerId()
        # comp = clientApi.GetEngineCompFactory().CreateRot(player_id)
        # print(comp.GetBodyRot())
        # comp = clientApi.GetEngineCompFactory().CreateGame("4d2ea478-f7f0-4936-b626-eaac97cd624e")
        # print(comp.GetRiderId(player_id))
        # self.HunterPlayerCompassUINode.SetVisible(self.messagebox_menu_title_path, True)
        # self.HunterPlayerCompassUINode.SetVisible(self.messagebox_background_image_path, True)
        # self.HunterPlayerCompassUINode.SetVisible(self.messagebox_box_image_path, True)

        # for number in range(0, 9):
        #     path = "/menu_panel/messagebox_panel/button_panel/button(%d)" % number
        #     self.HunterPlayerCompassUINode.SetVisible(path, True)

        self.HunterPlayerCompassUINode.SetVisible(self.messagebox_panel_path, True)

    def SetImagePanelVisible(self):
        self.SetVisible(self.image_panel_path, True)

    def SetImagePanelInvisible(self):
        self.SetVisible(self.image_panel_path, False, False)

    def ChangeCompassTexture(self, diction):

        # 通过改变UI贴图实现指南针(成功)
        # self.HunterPlayerCompassUINode.SetVisible("", False)
        if diction['direction'] != -1:
            self.count += 1
            if self.count > 5:
                self.current_path = "/menu_panel/image_panel/image(%d)" % diction['direction']

                self.HunterPlayerCompassUINode.SetVisible(self.old_path, False)
                self.HunterPlayerCompassUINode.SetVisible(self.current_path, True)

                self.old_path = self.current_path
                self.count = 0
        else:
            for number in range(0, 27):
                path = "/menu_panel/image_panel/image(%d)" % number
                self.HunterPlayerCompassUINode.SetVisible(path, False)
        # self.HunterPlayerCompassUINode.SetVisible("/image_panel/image(0)", False)
        # # self.HunterPlayerCompassUINode.SetVisible("", True)
        # print("self.HunterPlayerCompassUINode.SetVisible(self.old_path, True)")

        # 通过改变材质实现指南针(失败)
        # comp = clientApi.GetEngineCompFactory().CreateItem(dict['id'])
        # direction = dict['direction']
        # texture_path = "textures/items/f-%d" % direction

        # comp.ChangeItemTexture("hunter_player_compass:hunter_player_compass", texture_path)

        # 监听引擎OnScriptTickClient事件，引擎会执行该tick回调，1秒钟30帧

    def OnUIInitFinished(self, args):
        print("OnUIInitFinished : %s", args)
        clientApi.RegisterUI("hunter_player_compass_mod", "hunter_player_compass_ui",
                             "hunter_player_compass_mod.HunterPlayerCompassScreen.HunterPlayerCompassScreen",
                             "hunter_player_compass_ui.main")
        self.HunterPlayerCompassUINode = clientApi.CreateUI("hunter_player_compass_mod", "hunter_player_compass_ui",
                                                            {"isHud": 1})

        if self.HunterPlayerCompassUINode:
            self.HunterPlayerCompassUINode.Init()

    # def NTS(self, data):
    #     self.NotifyToServer("OnJoinHunterButtonTouch", data)

    def OnTickClient(self):
        """
        Driven by event, One tick way
        """
        pass

    # 被引擎直接执行的父类的重写函数，引擎会执行该Update回调，1秒钟30帧
    def Update(self):
        """
        Driven by system manager, Two tick way
        """
        pass

    def Destroy(self):
        pass
