# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()

compFactory = clientApi.GetEngineCompFactory()


class HunterPlayerCompassScreen(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
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
        self.menu_button_path = "/menu_panel/menu_button"

        self.currentKeepCompassToggleShow = True
        self.currentDistanceDisplayToggleShow = True
        self.currentCoordinateDisplayToggleShow = True
        self.currentMenuButtonToggleShow = True
        self.x_sliderAbsValue = 0
        self.y_sliderAbsValue = 0
        self.s_sliderAbsValue = 0.5
        self.x_sliderDisplayValue = 0
        self.y_sliderDisplayValue = 0
        self.s_sliderDisplayValue = 1
        self.x_sliderRealValue = 0
        self.y_sliderRealValue = 0
        self.sx_sliderRealValue = 1
        self.sy_sliderRealValue = 1
        self.sliderValue = 0
        self.settingbox_panel_display = 0
        self.image_panel_path = "/menu_panel/image_panel"
        self.slider_panel_path = "/menu_panel/settingbox_panel"

    def Create(self):
        print("===== FpsBattleScreen Create =====")
        self.AddTouchEventHandler("/menu_panel/messagebox_panel/button_panel/button(0)", self.OnCancelButtonTouch, {"isSwallow": True})
        self.AddTouchEventHandler("/menu_panel/messagebox_panel/button_panel/button(1)", self.OnJoinHunterButtonTouch, {"isSwallow": True})
        self.AddTouchEventHandler("/menu_panel/messagebox_panel/button_panel/button(2)", self.OnJoinPreyButtonTouch, {"isSwallow": True})
        self.AddTouchEventHandler("/menu_panel/messagebox_panel/button_panel/button(5)", self.OnCleanListButtonTouch, {"isSwallow": True})
        self.AddTouchEventHandler("/menu_panel/messagebox_panel/button_panel/button(3)", self.OnSwitchCompassButtonTouch, {"isSwallow": True})
        self.AddTouchEventHandler("/menu_panel/messagebox_panel/button_panel/button(4)", self.OnLockOrUnlockButtonTouch, {"isSwallow": True})
        self.AddTouchEventHandler("/menu_panel/messagebox_panel/button_panel/button(6)", self.OnMyWordsButtonTouch, {"isSwallow": True})
        self.AddTouchEventHandler("/menu_panel/messagebox_panel/button_panel/button(7)", self.OnActivateButtonTouch, {"isSwallow": True})
        self.AddTouchEventHandler("/menu_panel/messagebox_panel/button_panel/button(8)", self.OnSettingButtonTouch, {"isSwallow": True})
        self.AddTouchEventHandler("/menu_panel/settingbox_panel/button(0)", self.OnSettingCancelButtonTouch, {"isSwallow": True})
        self.AddTouchEventHandler("/menu_panel/menu_button", self.OpenCompassMenuTouch, {"isSwallow": True})
        self.AddTouchEventHandler("/menu_panel/settingbox_panel/background_button", self.OnBackgroundButtonTouch, {"isSwallow": True})

        self.sliderPanelItem = self.GetBaseUIControl(self.slider_panel_path)
        self.XSlider = self.sliderPanelItem.GetChildByPath("/x_slider").asSlider()
        self.YSlider = self.sliderPanelItem.GetChildByPath("/y_slider").asSlider()
        self.SSlider = self.sliderPanelItem.GetChildByPath("/s_slider").asSlider()
        self.XSliderLabelItem = self.sliderPanelItem.GetChildByPath("/x_axis_value").asLabel()
        self.YSliderLabelItem = self.sliderPanelItem.GetChildByPath("/y_axis_value").asLabel()
        self.SSliderLabelItem = self.sliderPanelItem.GetChildByPath("/scale_value").asLabel()
        self.imagePanelItem = self.GetBaseUIControl(self.image_panel_path)

    def Init(self):

        self.XSlider.SetSliderValue(self.x_sliderAbsValue)
        self.YSlider.SetSliderValue(self.y_sliderAbsValue)
        self.SSlider.SetSliderValue(self.s_sliderAbsValue)

        for number in range(0, 28):
            path = "/menu_panel/image_panel/image(%d)" % number
            self.SetVisible(path, False, False)
        #
        # for number in range(0, 9):
        #     path = "/menu_panel/messagebox_panel/button_panel/button(%d)" % number
        #     self.SetVisible(path, False, False)
        #
        # self.SetVisible(self.messagebox_menu_title_path, False, False)
        # self.SetVisible(self.messagebox_background_image_path, False, False)
        # self.SetVisible(self.messagebox_box_image_path, False, False)
        # self.SetVisible(self.settingbox_box_image_path, False, False)
        # self.SetVisible(self.settingbox_menu_title_path, False, False)
        # self.SetVisible(self.settingbox_background_image_path, False, False)
        # self.SetVisible(self.settingbox_close_button_path, False, False)

        self.SetVisible(self.messagebox_panel_path, False, False)
        self.SetVisible(self.settingbox_panel_path, False, False)

        if self.currentMenuButtonToggleShow == 0:
            self.SetVisible(self.menu_button_path, False, False)

        # messagebox_panel_input_panel = self.GetBaseUIControl(self.messagebox_panel_path).asInputPanel()
        # ret1 = messagebox_panel_input_panel.SetIsSwallow(True)
        # print(ret1)
        # settingbox_panel_input_panel = self.GetBaseUIControl(self.settingbox_panel_path).asInputPanel()
        # ret2 = settingbox_panel_input_panel.SetIsSwallow(True)
        # print(ret2)

        player_id = clientApi.GetLocalPlayerId()
        player_name_comp = clientApi.GetEngineCompFactory().CreateName(player_id)
        player_name = player_name_comp.GetName()
        data = {"player_id": player_id, "player_name": player_name}
        clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
        print("准备向服务端发送请求")
        clientSystem.NotifyToServer("RequestSettingData", data)
        print("已完成向服务端发送请求")

        self.UpdateScreen(False)

    def OnBackgroundButtonTouch(self, args):
        pass

    def OpenCompassMenuTouch(self, args):
        if self.settingbox_panel_display == 0:
            self.SetVisible(self.messagebox_panel_path, True)
            # messagebox_panel_input_panel = self.GetBaseUIControl(self.messagebox_panel_path).asInputPanel()
            # print(str(messagebox_panel_input_panel) + "123654")
            # ret1 = messagebox_panel_input_panel.SetIsSwallow(True)
            # print(str(ret1) + "123456")
            # settingbox_panel_input_panel = self.GetBaseUIControl(self.settingbox_panel_path).asInputPanel()
            # ret2 = settingbox_panel_input_panel.SetIsSwallow(True)
            # print(ret2)

    @ViewBinder.binding(ViewBinder.BF_SliderChanged | ViewBinder.BF_SliderFinished)
    def OnXSliderChange(self, value, isFinish, _unused):
        self.x_sliderAbsValue = value
        self.x_sliderDisplayValue = self.x_sliderAbsValue
        self.x_sliderRealValue = self.x_sliderDisplayValue * (1 - 0.15 * 0.5)
        text = str(round(self.x_sliderDisplayValue, 2))
        self.XSliderLabelItem.SetText(text)
        ret = self.imagePanelItem.SetFullPosition(axis="x", paramDict={"followType": "parent",
                                                                       "relativeValue": self.x_sliderRealValue})
        return ViewRequest.Refresh

    @ViewBinder.binding(ViewBinder.BF_BindFloat)
    def ReturnXSliderValue(self):
        return self.x_sliderAbsValue

    @ViewBinder.binding(ViewBinder.BF_BindInt)
    def ReturnXSliderStep(self):
        return 1

    @ViewBinder.binding(ViewBinder.BF_SliderChanged | ViewBinder.BF_SliderFinished)
    def OnYSliderChange(self, value, isFinish, _unused):
        self.y_sliderAbsValue = value
        self.y_sliderDisplayValue = self.y_sliderAbsValue
        self.y_sliderRealValue = self.y_sliderDisplayValue * (1 - 0.25 * 0.5)
        text = str(round(self.y_sliderDisplayValue, 2))
        self.YSliderLabelItem.SetText(text)
        ret = self.imagePanelItem.SetFullPosition(axis="y", paramDict={"followType": "parent",
                                                                       "relativeValue": self.y_sliderRealValue})
        return ViewRequest.Refresh

    @ViewBinder.binding(ViewBinder.BF_BindFloat)
    def ReturnYSliderValue(self):
        return self.y_sliderAbsValue

    @ViewBinder.binding(ViewBinder.BF_BindInt)
    def ReturnYSliderStep(self):
        return 1

    @ViewBinder.binding(ViewBinder.BF_SliderChanged | ViewBinder.BF_SliderFinished)
    def OnSSliderChange(self, value, isFinish, _unused):
        self.s_sliderAbsValue = value
        self.s_sliderDisplayValue = 2 ** (self.s_sliderAbsValue * 2 - 1)
        self.sx_sliderRealValue = self.s_sliderDisplayValue * 0.15
        self.sy_sliderRealValue = self.s_sliderDisplayValue * 0.25
        text = str(round(self.s_sliderDisplayValue, 2))
        self.SSliderLabelItem.SetText(text)
        ret1 = self.imagePanelItem.SetFullSize(axis="x", paramDict={"followType": "parent", "relativeValue": self.sx_sliderRealValue})
        ret2 = self.imagePanelItem.SetFullSize(axis="y", paramDict={"followType": "parent", "relativeValue": self.sy_sliderRealValue})
        return ViewRequest.Refresh

    @ViewBinder.binding(ViewBinder.BF_BindFloat)
    def ReturnSSliderValue(self):
        return self.s_sliderAbsValue

    @ViewBinder.binding(ViewBinder.BF_BindInt)
    def ReturnSSliderStep(self):
        return 1

    def ChangeToggleState(self, dic):
        print("准备更改参数")
        if "enable_keep_compass" in dic:
            self.currentKeepCompassToggleShow = dic["enable_keep_compass"]
        if "enable_distance_display" in dic:
            self.currentDistanceDisplayToggleShow = dic["enable_distance_display"]
        if "enable_coordinate_display" in dic:
            self.currentCoordinateDisplayToggleShow = dic["enable_coordinate_display"]
        if "enable_menu_button" in dic:
            self.currentMenuButtonToggleShow = dic["enable_menu_button"]
        if self.currentMenuButtonToggleShow == 1:
            self.SetVisible(self.menu_button_path, True)
        else:
            self.SetVisible(self.menu_button_path, False, False)
        print("已完成更改参数")
        return ViewRequest.Refresh

    @ViewBinder.binding(ViewBinder.BF_ToggleChanged)
    def OnKeepCompassToggleChangeCallback(self, args):
        self.currentKeepCompassToggleShow = args["state"]
        player_id = clientApi.GetLocalPlayerId()
        player_name_comp = clientApi.GetEngineCompFactory().CreateName(player_id)
        player_name = player_name_comp.GetName()
        data = {"player_id": player_id, "player_name": player_name}
        clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
        print("准备向服务端发送请求")
        clientSystem.NotifyToServer("TryEnableKeepCompass", data)
        print("已完成向服务端发送请求")
        return ViewRequest.Refresh

    @ViewBinder.binding(ViewBinder.BF_BindBool)
    def ReturnKeepCompassToggleState(self):
        return self.currentKeepCompassToggleShow

    @ViewBinder.binding(ViewBinder.BF_ToggleChanged)
    def OnDistanceDisplayToggleChangeCallback(self, args):
        self.currentDistanceDisplayToggleShow = args["state"]
        player_id = clientApi.GetLocalPlayerId()
        player_name_comp = clientApi.GetEngineCompFactory().CreateName(player_id)
        player_name = player_name_comp.GetName()
        data = {"player_id": player_id, "player_name": player_name}
        clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
        print("准备向服务端发送请求")
        clientSystem.NotifyToServer("TryEnableDistanceDisplay", data)
        print("已完成向服务端发送请求")
        return ViewRequest.Refresh

    @ViewBinder.binding(ViewBinder.BF_BindBool)
    def ReturnDistanceDisplayToggleState(self):
        return self.currentDistanceDisplayToggleShow

    @ViewBinder.binding(ViewBinder.BF_ToggleChanged)
    def OnCoordinateDisplayToggleChangeCallback(self, args):
        self.currentCoordinateDisplayToggleShow = args["state"]
        player_id = clientApi.GetLocalPlayerId()
        player_name_comp = clientApi.GetEngineCompFactory().CreateName(player_id)
        player_name = player_name_comp.GetName()
        data = {"player_id": player_id, "player_name": player_name}
        clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
        print("准备向服务端发送请求")
        clientSystem.NotifyToServer("TryEnableCoordinateDisplay", data)
        print("已完成向服务端发送请求")
        return ViewRequest.Refresh

    @ViewBinder.binding(ViewBinder.BF_BindBool)
    def ReturnCoordinateDisplayToggleState(self):
        return self.currentCoordinateDisplayToggleShow

    @ViewBinder.binding(ViewBinder.BF_ToggleChanged)
    def OnMenuButtonToggleChangeCallback(self, args):
        self.currentMenuButtonToggleShow = args["state"]
        player_id = clientApi.GetLocalPlayerId()
        player_name_comp = clientApi.GetEngineCompFactory().CreateName(player_id)
        player_name = player_name_comp.GetName()
        data = {"player_id": player_id, "player_name": player_name}
        clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
        print("准备向服务端发送请求")
        clientSystem.NotifyToServer("TryEnableMenuButton", data)
        print("已完成向服务端发送请求")
        return ViewRequest.Refresh

    @ViewBinder.binding(ViewBinder.BF_BindBool)
    def ReturnMenuButtonToggleState(self):
        return self.currentMenuButtonToggleShow

    def OnCancelButtonTouch(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            print(33333333333)
            # for number in range(0, 9):
            #     path = "/menu_panel/messagebox_panel/button_panel/button(%d)" % number
            #     self.SetVisible(path, False, False)

            # self.SetVisible(self.messagebox_menu_title_path, False, False)
            # self.SetVisible(self.messagebox_background_image_path, False, False)
            # self.SetVisible(self.messagebox_box_image_path, False, False)

            self.SetVisible(self.messagebox_panel_path, False, False)

        elif touchEvent == touchEventEnum.TouchCancel:
            pass

    def OnJoinHunterButtonTouch(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            print("(1)")
            player_id = clientApi.GetLocalPlayerId()
            player_name_comp = clientApi.GetEngineCompFactory().CreateName(player_id)
            player_name = player_name_comp.GetName()
            data = {"player_id": player_id, "player_name": player_name, "message": "hunter set"}
            clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
            clientSystem.NotifyToServer("OnJoinHunterButtonTouch", data)

    def OnJoinPreyButtonTouch(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            print("(2)")
            player_id = clientApi.GetLocalPlayerId()
            player_name_comp = clientApi.GetEngineCompFactory().CreateName(player_id)
            player_name = player_name_comp.GetName()
            data = {"player_id": player_id, "player_name": player_name, "message": "prey set"}
            clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
            clientSystem.NotifyToServer("OnJoinHunterButtonTouch", data)

    def OnCleanListButtonTouch(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            print("(5)")
            player_id = clientApi.GetLocalPlayerId()
            player_name_comp = clientApi.GetEngineCompFactory().CreateName(player_id)
            player_name = player_name_comp.GetName()
            data = {"player_id": player_id, "player_name": player_name, "message": "pah reset"}
            clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
            clientSystem.NotifyToServer("OnJoinHunterButtonTouch", data)

    def OnActivateButtonTouch(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            print("(7)")
            player_id = clientApi.GetLocalPlayerId()
            player_name_comp = clientApi.GetEngineCompFactory().CreateName(player_id)
            player_name = player_name_comp.GetName()
            data = {"player_id": player_id, "player_name": player_name, "message": "activate or change"}
            clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
            clientSystem.NotifyToServer("OnActivateButtonTouch", data)

    def OnLockOrUnlockButtonTouch(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            print("(4)")
            player_id = clientApi.GetLocalPlayerId()
            player_name_comp = clientApi.GetEngineCompFactory().CreateName(player_id)
            player_name = player_name_comp.GetName()
            data = {"player_id": player_id, "player_name": player_name, "message": "stop"}
            clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
            clientSystem.NotifyToServer("OnLockOrUnlockButtonTouch", data)

    def OnSwitchCompassButtonTouch(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            print("(3)")
            player_id = clientApi.GetLocalPlayerId()
            player_name_comp = clientApi.GetEngineCompFactory().CreateName(player_id)
            player_name = player_name_comp.GetName()
            data = {"player_id": player_id, "player_name": player_name, "message": "switch"}
            clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
            clientSystem.NotifyToServer("OnSwitchCompassButtonTouch", data)

    def OnMyWordsButtonTouch(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            print("(4)")
            player_id = clientApi.GetLocalPlayerId()
            player_name_comp = clientApi.GetEngineCompFactory().CreateName(player_id)
            player_name = player_name_comp.GetName()
            data = {"player_id": player_id, "player_name": player_name, "message": "my words"}
            clientSystem = clientApi.GetSystem("hunter_player_compass_mod", "PlayerCompassClientSystem")
            clientSystem.NotifyToServer("OnMyWordsButtonTouch", data)

    def OnSettingButtonTouch(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            print(33333333333)

            # self.SetVisible(self.settingbox_background_image_path, True)
            # self.SetVisible(self.settingbox_box_image_path, True)
            # self.SetVisible(self.settingbox_menu_title_path, True)
            # self.SetVisible(self.settingbox_close_button_path, True)

            self.SetVisible(self.settingbox_panel_path, True)
            for number in range(0, 28):
                path = "/menu_panel/image_panel/image(%d)" % number
                self.SetVisible(path, True)
            self.SetVisible(self.messagebox_panel_path, False, False)
            self.settingbox_panel_display = 1
            # for number in range(0, 28):
            #     path = "/menu_panel/image_panel/image(%d)" % number
            #     self.SetVisible(path, True)

        elif touchEvent == touchEventEnum.TouchCancel:
            pass

    def OnSettingCancelButtonTouch(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        # 按钮事件
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            print(33333333333)

            # self.SetVisible(self.settingbox_background_image_path, False, False)
            # self.SetVisible(self.settingbox_box_image_path, False, False)
            # self.SetVisible(self.settingbox_menu_title_path, False, False)
            # self.SetVisible(self.settingbox_close_button_path, False, False)

            self.SetVisible(self.settingbox_panel_path, False, False)
            for number in range(0, 28):
                path = "/menu_panel/image_panel/image(%d)" % number
                self.SetVisible(path, False, False)
            self.SetVisible(self.messagebox_panel_path, True)
            self.settingbox_panel_display = 0
            # for number in range(0, 28):
            #     path = "/menu_panel/image_panel/image(%d)" % number
            #     self.SetVisible(path, False, False)

            self.UpdateScreen(True)

        elif touchEvent == touchEventEnum.TouchCancel:
            pass