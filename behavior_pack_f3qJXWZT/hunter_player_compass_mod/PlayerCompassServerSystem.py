# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import math

ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()


# self.hunter_ids = {"123": {"name":"111", "target": 1}, "321": {"name":"222", "target": 2}}
# self.prey_ids = ['-4294967295']
class PlayerCompassServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        print("__init__")
        self.player_tp_cache = {}
        self.prey_ids = []
        self.hunter_ids = {}
        self.prey_pos = ()
        self.hunter_pos = ()
        # self.hunter_body_rot = {}
        self.relative_position = ()
        self.enable_coordinate_display = 1
        self.enable_distance_display = 1
        self.enable_keep_compass = 1
        self.enable_menu_button = 1
        self.levelid = ""
        self.ListenEvent()

    def ListenEvent(self):
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
                            "ItemUseAfterServerEvent",
                            self, self.compass_using_server_event)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self,
                            self.on_chat)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnScriptTickServer", self,
                            self.on_script_tick)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnScriptTickServer", self,
                            self.replace_compass)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
                            "PlayerIntendLeaveServerEvent", self, self.player_leave)

        # button
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassClientSystem",
                            "OnJoinHunterButtonTouch", self, self.on_chat_touch_button)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassClientSystem",
                            "OnActivateButtonTouch", self, self.compass_using_server_event_touch_button)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassClientSystem",
                            "OnSwitchCompassButtonTouch", self, self.compass_using_server_event_touch_button)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassClientSystem",
                            "OnLockOrUnlockButtonTouch", self, self.lock_or_unlock_identity)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassClientSystem",
                            "OnMyWordsButtonTouch", self, self.notify_players)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassClientSystem",
                            "TryEnableKeepCompass", self, self.try_enable_keep_compass)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassClientSystem",
                            "TryEnableDistanceDisplay", self, self.try_enable_distance_display)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassClientSystem",
                            "TryEnableCoordinateDisplay", self, self.try_enable_coordinate_display)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassClientSystem",
                            "TryEnableMenuButton", self, self.try_enable_menu_button)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassClientSystem",
                            "RequestSettingData", self, self.send_setting_data)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassClientSystem",
                            "ReceiveBodyRot", self, self.receive_body_rot)
        self.ListenForEvent("hunter_player_compass_mod", "PlayerCompassClientSystem",
                            "IsInBoat", self, self.is_player_in_boat)

        print("self.ListenForEvent")

    def is_player_in_boat(self, is_in_boat_dic):
        player_id = is_in_boat_dic["player_id"]
        is_in_boat = is_in_boat_dic["is_in_boat"]
        if player_id in list(self.hunter_ids.keys()):
            self.hunter_ids[player_id]["is_in_boat"] = is_in_boat

    def receive_body_rot(self, body_rot_dic):
        player_id = body_rot_dic["player_id"]
        body_rot = body_rot_dic["body_rot"]
        if player_id in list(self.hunter_ids.keys()):
            self.hunter_ids[player_id]["body_rot"] = body_rot

    def send_setting_data(self, data):
        player_id = data["player_id"]
        setting_data_dict = {"enable_keep_compass": self.enable_keep_compass,
                             "enable_coordinate_display": self.enable_coordinate_display,
                             "enable_distance_display": self.enable_distance_display,
                             "enable_menu_button": self.enable_menu_button}
        print("准备向客户端发送设置数据")
        self.NotifyToClient(player_id, 'ReceiveSettingData', setting_data_dict)
        print("已完成向客户端发送设置数据")
        pass

    def try_enable_keep_compass(self, data):
        player_id = data["player_id"]
        operation_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
        operation = operation_comp.GetPlayerOperation()
        if operation >= 2:
            if self.enable_keep_compass == 1:
                self.enable_keep_compass = 0
            else:
                self.enable_keep_compass = 1
            if self.enable_keep_compass == 1:
                msg = "系统：已开启指南针死亡不掉落"
            else:
                msg = "系统：已关闭指南针死亡不掉落"
            player_id_list = serverApi.GetPlayerList()
            for player_id in player_id_list:
                player_id_dict = {"player_id": player_id}
                self.send_setting_data(player_id_dict)
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                msg_comp.NotifyOneMessage(player_id, msg)
        else:
            msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
            msg = "系统： 权限不足"
            msg_comp.NotifyOneMessage(player_id, msg)
            enable_keep_compass_dict = {"enable_keep_compass": self.enable_keep_compass}
            print("准备向客户端发送请求(权限不足)")
            self.NotifyToClient(player_id, 'EnableKeepCompass', enable_keep_compass_dict)
            print("已完成向客户端发送请求(权限不足)")

    def try_enable_distance_display(self, data):
        player_id = data["player_id"]
        operation_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
        operation = operation_comp.GetPlayerOperation()
        if operation >= 2:
            if self.enable_distance_display == 1:
                self.enable_distance_display = 0
            else:
                self.enable_distance_display = 1
            if self.enable_distance_display == 1:
                msg = "系统：已开启猎物距离显示"
            else:
                msg = "系统：已关闭猎物距离显示"
            player_id_list = serverApi.GetPlayerList()
            for player_id in player_id_list:
                player_id_dict = {"player_id": player_id}
                self.send_setting_data(player_id_dict)
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                msg_comp.NotifyOneMessage(player_id, msg)
        else:
            msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
            msg = "系统： 权限不足"
            msg_comp.NotifyOneMessage(player_id, msg)
            enable_distance_display_dict = {"enable_distance_display": self.enable_distance_display}
            print("准备向客户端发送请求(权限不足)")
            self.NotifyToClient(player_id, 'EnableDistanceDisplay', enable_distance_display_dict)
            print("已完成向客户端发送请求(权限不足)")

    def try_enable_coordinate_display(self, data):
        player_id = data["player_id"]
        operation_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
        operation = operation_comp.GetPlayerOperation()
        if operation >= 2:
            if self.enable_coordinate_display == 1:
                self.enable_coordinate_display = 0
            else:
                self.enable_coordinate_display = 1
            if self.enable_coordinate_display == 1:
                msg = "系统：已开启猎物坐标显示"
            else:
                msg = "系统：已关闭猎物坐标显示"
            player_id_list = serverApi.GetPlayerList()
            for player_id in player_id_list:
                player_id_dict = {"player_id": player_id}
                self.send_setting_data(player_id_dict)
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                msg_comp.NotifyOneMessage(player_id, msg)
        else:
            msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
            msg = "系统： 权限不足"
            msg_comp.NotifyOneMessage(player_id, msg)
            enable_coordinate_display_dict = {"enable_coordinate_display": self.enable_coordinate_display}
            print("准备向客户端发送请求(权限不足)")
            self.NotifyToClient(player_id, 'EnableCoordinateDisplay', enable_coordinate_display_dict)
            print("已完成向客户端发送请求(权限不足)")

    def try_enable_menu_button(self, data):
        player_id = data["player_id"]
        operation_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
        operation = operation_comp.GetPlayerOperation()
        if operation >= 2:
            if self.enable_menu_button == 1:
                self.enable_menu_button = 0
            else:
                self.enable_menu_button = 1
            if self.enable_menu_button == 1:
                msg = "系统：已开启菜单按钮"
            else:
                msg = "系统：已关闭菜单按钮"
            player_id_list = serverApi.GetPlayerList()
            for player_id in player_id_list:
                player_id_dict = {"player_id": player_id}
                self.send_setting_data(player_id_dict)
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                msg_comp.NotifyOneMessage(player_id, msg)
        else:
            msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
            msg = "系统： 权限不足"
            msg_comp.NotifyOneMessage(player_id, msg)
            enable_menu_button_dict = {"enable_menu_button": self.enable_menu_button}
            print("准备向客户端发送请求(权限不足)")
            self.NotifyToClient(player_id, 'EnableMenuButton', enable_menu_button_dict)
            print("已完成向客户端发送请求(权限不足)")

    def notify_players(self, data):
        # 获取玩家ID
        player_id = data['player_id']
        player_name = data['player_name']
        message = data['message']
        if message == "my words":
            msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
            msg1 = "此模组就是你想玩的那种指南针！"
            msg3 = "个人开发实在不易，因此转为最低程度的付费，还请希望谅解。"
            msg4 = "如有bug和建议，欢迎到评论区反馈！"
            msg5 = "祝您玩得开心！"
            msg = msg1 + "\n" + msg3 + "\n" + msg4 + "\n" + msg5
            msg_comp.NotifyOneMessage(player_id, msg)

    def player_leave(self, event):
        player_id = event['playerId']
        # player_name_comp = serverApi.GetEngineCompFactory().CreateName(player_id)
        # player_name = player_name_comp.GetName()
        hunter_id_values = list(self.hunter_ids.keys())
        if player_id in self.prey_ids:
            self.prey_ids.remove(player_id)
            # for hunter_id in self.hunter_ids:
            #     msg_comp = serverApi.GetEngineCompFactory().CreateMsg(hunter_id)
            #     msg = "系统: 猎物 玩家 \""+player_name+"\" 已退出"
            #     msg_comp.NotifyOneMessage(hunter_id, msg)
        elif player_id in hunter_id_values:
            for key, value in self.hunter_ids.items():
                if key == player_id:
                    self.hunter_ids.pop(player_id)
                    break
                    # for hunter_id in self.hunter_ids:
                    #     msg_comp = serverApi.GetEngineCompFactory().CreateMsg(hunter_id)
                    #     msg = "系统: 猎人 玩家 \""+player_name+"\" 已退出"
                    #     msg_comp.NotifyOneMessage(hunter_id, msg)
                    # msg_comp = serverApi.GetEngineCompFactory().CreateMsg(self.prey_id)
                    # msg = "系统: 猎人 玩家 \"" + player_name + "\" 已退出"
                    # msg_comp.NotifyOneMessage(self.prey_id, msg)

    def compass_using_server_event(self, event):
        # print(self.prey_ids)
        # print(self.hunter_ids)

        if event['itemDict']['newItemName'] == "hunter_player_compass:hunter_player_compass":
            player_id = event['entityId']
            hunter_id_values = list(self.hunter_ids.keys())

            diction = {}
            diction["id"] = player_id

            self.NotifyToClient(player_id, 'OpenCompassMenu', self.hunter_ids)

            # # self.NotifyToClient(player_id, 'ChangeCompassTexture', {})
            #
            # # self.NotifyToClient(player_id, 'ChangeCompassTexture', diction)
            #
            # # comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
            # # item_dict = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, 0)
            # # comp.SetItemLayer(item_dict, 1, 'hunter_player_compass:hunter_player_compass_27')
            # # comp.SpawnItemToPlayerInv(item_dict, player_id, 0)
            #
            # if len(self.prey_ids) == 0:
            #     msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
            #     msg = "系统: 目前没有猎物，无法追踪 (提示: 在聊天栏发送\"prey set\", 发送的玩家即可成为猎物。" \
            #           "管理员可以通过发送\"prey reset\"来清空猎物人选)"
            #     msg_comp.NotifyOneMessage(player_id, msg)
            #
            # elif player_id in self.prey_ids:
            #     msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
            #     msg = "系统： 你是猎物，无法使用猎人指南针"
            #     msg_comp.NotifyOneMessage(player_id, msg)
            #
            # # 换人
            # elif player_id in hunter_id_values:
            #
            #     prey_sum = len(self.prey_ids)
            #
            #     self.hunter_ids[str(player_id)]["target"] += 1
            #     if self.hunter_ids[str(player_id)]["target"] > prey_sum:
            #         self.hunter_ids[str(player_id)]["target"] = 0
            #         msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
            #         msg = "系统：已停用猎人指南针"
            #         msg_comp.NotifyOneMessage(player_id, msg)
            #     else:
            #         prey_id = self.prey_ids[self.hunter_ids[str(player_id)]["target"] - 1]
            #         prey_name_comp = serverApi.GetEngineCompFactory().CreateName(prey_id)
            #         prey_name = prey_name_comp.GetName()
            #         msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
            #         msg = "系统：猎人指南针已指向 " + prey_name
            #         msg_comp.NotifyOneMessage(player_id, msg)
            # else:
            #     msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
            #     msg = "系统：你不是猎人，无法使用猎人指南针 (提示: 在聊天栏发送\"hunter set\", 发送的玩家即可成为猎人。"\
            #           "管理员可以通过发送\"hunter reset\"来清空猎物人选)"
            #     msg_comp.NotifyOneMessage(player_id, msg)
            #
            # print(self.hunter_ids)
            # print(self.prey_ids)

    def compass_using_server_event_touch_button(self, data):

        # 获取玩家ID
        player_id = data['player_id']
        player_name = data['player_name']
        message = data['message']

        hunter_id_values = list(self.hunter_ids.keys())

        diction = {}
        diction["id"] = player_id

        levelid = serverApi.GetLevelId()
        levelid_dic = {"levelid": levelid}
        self.NotifyToClient(player_id, 'ReceiveLevelIdData', levelid_dic)

        if len(self.prey_ids) == 0:
            msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
            msg = "系统: 目前没有猎物，无法追踪"
            msg_comp.NotifyOneMessage(player_id, msg)

        elif player_id in self.prey_ids:
            msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
            msg = "系统： 你是猎物，无法使用猎人指南针"
            msg_comp.NotifyOneMessage(player_id, msg)

        # 换人
        elif player_id in hunter_id_values:

            if "is_active" not in self.hunter_ids[str(player_id)]:
                self.hunter_ids[str(player_id)]["is_active"] = 0
            if "target" not in self.hunter_ids[str(player_id)]:
                self.hunter_ids[str(player_id)]["target"] = 0

            prey_sum = len(self.prey_ids)

            if message == "activate or change":
                self.hunter_ids[str(player_id)]["is_active"] = 1
                if self.hunter_ids[str(player_id)]["target"] >= prey_sum:
                    self.hunter_ids[str(player_id)]["target"] = 1
                else:
                    self.hunter_ids[str(player_id)]["target"] += 1
                prey_id = self.prey_ids[self.hunter_ids[str(player_id)]["target"] - 1]
                prey_name_comp = serverApi.GetEngineCompFactory().CreateName(prey_id)
                prey_name = prey_name_comp.GetName()
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                msg = "系统：猎人指南针已指向 " + prey_name
                msg_comp.NotifyOneMessage(player_id, msg)

            elif message == "stop":
                self.hunter_ids[str(player_id)]["is_active"] = 0
                self.hunter_ids[str(player_id)]["target"] = 0
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                msg = "系统：已停用猎人指南针"
                msg_comp.NotifyOneMessage(player_id, msg)

            elif message == "switch":
                if self.hunter_ids[str(player_id)]["is_active"] == 1:
                    self.hunter_ids[str(player_id)]["is_active"] = 0
                    self.hunter_ids[str(player_id)]["target"] = 0
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                    msg = "系统：已停用猎人指南针"
                    msg_comp.NotifyOneMessage(player_id, msg)
                else:
                    self.hunter_ids[str(player_id)]["is_active"] = 1
                    self.hunter_ids[str(player_id)]["target"] = 1
                    prey_id = self.prey_ids[self.hunter_ids[str(player_id)]["target"] - 1]
                    prey_name_comp = serverApi.GetEngineCompFactory().CreateName(prey_id)
                    prey_name = prey_name_comp.GetName()
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                    msg = "系统：已启用猎人指南针,指向目标 " + prey_name
                    msg_comp.NotifyOneMessage(player_id, msg)

        else:
            msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
            msg = "系统：你不是猎人，无法使用猎人指南针"
            msg_comp.NotifyOneMessage(player_id, msg)

        print(self.hunter_ids)
        print(self.prey_ids)

    def lock_or_unlock_identity(self):
        pass

    def on_script_tick(self):
        # 1. 初始化缓存字典
        if not hasattr(self, 'prey_last_pos_cache'):
            self.prey_last_pos_cache = {}

        # 2. 【关键修改】全局更新所有猎物的位置缓存
        # 无论猎人是否在看他们，都要实时记录他们当前所在维度的位置
        if self.prey_ids:
            for pid in self.prey_ids:
                # 获取猎物当前维度
                p_dim_comp = serverApi.GetEngineCompFactory().CreateDimension(pid)
                if not p_dim_comp: continue
                p_dim = p_dim_comp.GetEntityDimensionId()

                # 获取猎物当前坐标
                p_pos_comp = compFactory.CreatePos(pid)
                if not p_pos_comp: continue
                p_pos = p_pos_comp.GetPos()

                if p_pos:
                    if pid not in self.prey_last_pos_cache:
                        self.prey_last_pos_cache[pid] = {}
                    # 记录该猎物在当前维度的最新位置
                    self.prey_last_pos_cache[pid][p_dim] = p_pos

        # 3. 处理非猎人玩家 UI
        player_ui_data = self.CreateEventData()
        player_id_list = serverApi.GetPlayerList()
        for player_id in player_id_list:
            if player_id not in self.hunter_ids:
                player_ui_data['id'] = player_id
                player_ui_data['direction'] = -1
                self.NotifyToClient(player_id, 'ChangeCompassTexture', player_ui_data)

        # 4. 猎人追踪逻辑
        if len(self.prey_ids) != 0 and len(self.hunter_ids) != 0:
            portion = 360 / 28.0
            start_angle = -180 + portion / 2
            end_angle = 180 - portion / 2

            for hunter_id, value in self.hunter_ids.items():
                pos_comp = compFactory.CreatePos(hunter_id)
                self.hunter_pos = pos_comp.GetPos()
                hunter_dimension_comp = serverApi.GetEngineCompFactory().CreateDimension(hunter_id)
                hunter_dimension = hunter_dimension_comp.GetEntityDimensionId()

                if 0 < value["target"] <= len(self.prey_ids):
                    prey_id = self.prey_ids[value["target"] - 1]

                    # 获取猎物当前的真实维度（用于判断是否跨维度）
                    prey_dimension_comp = serverApi.GetEngineCompFactory().CreateDimension(prey_id)
                    prey_real_dimension = prey_dimension_comp.GetEntityDimensionId()

                    # === 决定目标坐标 ===
                    target_pos = None
                    is_tracking_last_known = False

                    if hunter_dimension == prey_real_dimension:
                        # 情况A: 同维度，直接获取实时坐标
                        prey_pos_comp = compFactory.CreatePos(prey_id)
                        target_pos = prey_pos_comp.GetPos()
                    else:
                        # 情况B: 不同维度，从全局缓存中查找猎物在猎人维度的最后位置
                        # 因为步骤2已经全局更新过，这里取到的一定是猎物离开该维度前的最新位置
                        if prey_id in self.prey_last_pos_cache and hunter_dimension in self.prey_last_pos_cache[
                            prey_id]:
                            target_pos = self.prey_last_pos_cache[prey_id][hunter_dimension]
                            is_tracking_last_known = True

                    # === 开始计算方向 ===
                    if target_pos is not None:
                        hunter_x_pos = self.hunter_pos[0]
                        hunter_y_pos = self.hunter_pos[1]
                        hunter_z_pos = self.hunter_pos[2]

                        prey_x_pos = target_pos[0]
                        prey_y_pos = target_pos[1]
                        prey_z_pos = target_pos[2]

                        hunter_rot_comp = compFactory.CreateRot(hunter_id)
                        [hunter_v_rot, hunter_h_rot] = hunter_rot_comp.GetRot()

                        if self.hunter_ids[hunter_id]["is_in_boat"] == 1:
                            body_rot = self.hunter_ids[hunter_id]["body_rot"]
                            if body_rot + 180 > 360:
                                yushu = (body_rot + 180) % 360
                                body_rot = -180 + yushu
                            elif body_rot + 180 < 0:
                                yushu = -((-(body_rot + 180)) % 360)
                                body_rot = 180 + yushu
                            hunter_h_rot = body_rot

                        hp_x_pos = hunter_x_pos - prey_x_pos
                        hp_y_pos = hunter_y_pos - prey_y_pos
                        hp_z_pos = hunter_z_pos - prey_z_pos

                        hp_distance = (hp_x_pos ** 2 + hp_y_pos ** 2 + hp_z_pos ** 2) ** 0.5

                        if (hunter_x_pos - prey_x_pos) == 0:
                            hp_x_pos = 1.0

                        prey_angle = math.atan(hp_z_pos / hp_x_pos)
                        prey_angle = prey_angle * 180 / math.pi
                        if hp_x_pos > 0:
                            prey_angle += 180
                        prey_angle -= 90

                        if prey_angle > 0:
                            if -180 <= hunter_h_rot <= (-180 + prey_angle):
                                hunter_h_rot += 360
                        if prey_angle < 0:
                            if (180 + prey_angle) <= hunter_h_rot <= 180:
                                hunter_h_rot -= 360

                        hp_angle = hunter_h_rot - prey_angle

                        # === Action Bar 显示 ===
                        if self.enable_coordinate_display + self.enable_distance_display != 0:
                            hunter_comp = compFactory.CreateCommand(hunter_id)
                            command = "/titleraw @s actionbar {\"rawtext\": [{\"text\":\""

                            # 如果是残影，显示灰色且带标记
                            status_prefix = "§6§l" if not is_tracking_last_known else "§7§l[残影] "

                            if self.enable_coordinate_display == 1:
                                command += status_prefix + "坐标: " + str(int(round(prey_x_pos, 0))) + " " + str(
                                    int(round(prey_y_pos, 0))) + " " + str(int(round(prey_z_pos, 0))) + "\n"

                            if self.enable_distance_display == 1:
                                dist_text = ""
                                if -hp_y_pos > 0:
                                    dist_text = "距离: ︽ "
                                elif round(hp_y_pos) == 0:
                                    dist_text = "距离: == "
                                else:
                                    dist_text = "距离: ︾ "
                                command += status_prefix + dist_text + str(int(round(hp_distance, 0)))

                            command += "\"}]}"
                            hunter_comp.SetCommand(command, hunter_id)

                        # === 指南针纹理 ===
                        direction_data = self.CreateEventData()
                        direction_data['id'] = hunter_id

                        if hp_angle < start_angle or hp_angle > end_angle:
                            direction_data['direction'] = 0
                        elif start_angle + portion < hp_angle < start_angle + portion * 27:
                            direction_data['direction'] = 27 - (int((hp_angle - start_angle) / portion))
                        else:
                            direction_data['direction'] = 27

                        if value["is_active"] == 1:
                            self.NotifyToClient(hunter_id, 'ChangeCompassTexture', direction_data)

                    else:
                        # 无法追踪（不同维度且无历史记录）
                        prey_name_comp = serverApi.GetEngineCompFactory().CreateName(prey_id)
                        prey_name = prey_name_comp.GetName()

                        hunter_comp = compFactory.CreateCommand(hunter_id)
                        command = "/titleraw @s actionbar {\"rawtext\": [{\"text\":\"§c§l" + prey_name + " 不在当前维度，且无残留踪迹\"}]}"
                        hunter_comp.SetCommand(command, hunter_id)

                        if value["is_active"] == 1:
                            direction_data = self.CreateEventData()
                            direction_data['id'] = hunter_id
                            direction_data['direction'] = 0
                            self.NotifyToClient(hunter_id, 'ChangeCompassTexture', direction_data)

                elif self.hunter_ids[str(hunter_id)]["target"] == 0:
                    player_ui_data['id'] = hunter_id
                    player_ui_data['direction'] = -1
                    self.NotifyToClient(hunter_id, 'ChangeCompassTexture', player_ui_data)
                else:
                    self.hunter_ids[str(hunter_id)]["target"] = 0

        elif len(self.prey_ids) == 0 and len(self.hunter_ids) != 0:
            for hunter_id in self.hunter_ids:
                player_ui_data['id'] = hunter_id
                player_ui_data['direction'] = -1
                self.NotifyToClient(hunter_id, 'ChangeCompassTexture', player_ui_data)

    def replace_compass(self):
        if self.enable_keep_compass == 1:
            player_id_list = serverApi.GetPlayerList()
            for player_id in player_id_list:
                player_name_comp = serverApi.GetEngineCompFactory().CreateName(player_id)
                player_name = player_name_comp.GetName()
                hunter_hasitem_comp = compFactory.CreateCommand(player_id)
                command = "/clear "+player_name+" hunter_player_compass:hunter_player_compass 0 1"
                is_hasitem_and_clear = hunter_hasitem_comp.SetCommand(command, player_id)
                # print(command)
                if is_hasitem_and_clear is True:
                    command = "/give "+player_name+" hunter_player_compass:hunter_player_compass 1 1 {\"minecraft:keep_on_death\":{}}"
                    hunter_hasitem_comp.SetCommand(command, player_id)
        else:
            player_id_list = serverApi.GetPlayerList()
            for player_id in player_id_list:
                player_name_comp = serverApi.GetEngineCompFactory().CreateName(player_id)
                player_name = player_name_comp.GetName()
                hunter_hasitem_comp = compFactory.CreateCommand(player_id)
                command = "/clear "+player_name+" hunter_player_compass:hunter_player_compass 1 1"
                is_hasitem_and_clear = hunter_hasitem_comp.SetCommand(command, player_id)

                if is_hasitem_and_clear is True:
                    command = "/give "+player_name+" hunter_player_compass:hunter_player_compass 1 0"
                    hunter_hasitem_comp.SetCommand(command, player_id)

    def on_chat(self, event):
        # 获取玩家ID
        player_id = event['playerId']
        player_name = event['username']
        # 获取聊天消息
        message = event['message']

        hunter_id_values = list(self.hunter_ids.keys())

        if message == "prey set":
            if player_id in hunter_id_values:
                for key, value in self.hunter_ids.items():
                    if key == player_id:
                        # 移除包含目标字符串的键
                        self.hunter_ids.pop(key)
                        break
            if player_id in self.prey_ids:
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                msg = "系统：你已经是猎物了"
                msg_comp.NotifyOneMessage(player_id, msg)

            else:
                self.prey_ids.append(player_id)
                player_name_comp = serverApi.GetEngineCompFactory().CreateName(player_id)
                player_name = player_name_comp.GetName()
                prey_msg = "系统： 已将 " + player_name + " 设置为猎物"

                for prey_id in self.prey_ids:
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(prey_id)
                    msg_comp.NotifyOneMessage(prey_id, prey_msg)
                for hunter_id, value in self.hunter_ids.items():
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(hunter_id)
                    msg_comp.NotifyOneMessage(hunter_id, prey_msg)

        elif message == "hunter set":
            if player_id in self.prey_ids:
                self.prey_ids.remove(player_id)

            if player_id in hunter_id_values:
                for key, value in self.hunter_ids.items():
                    if key == player_id:
                        msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                        msg = "系统：你已经是猎物了"
                        msg_comp.NotifyOneMessage(player_id, msg)
                        break

            else:
                self.hunter_ids[str(player_id)] = {}
                self.hunter_ids[str(player_id)]["name"] = player_name
                self.hunter_ids[str(player_id)]["target"] = 0
                self.hunter_ids[str(player_id)]["is_active"] = 0
                prey_msg = "系统： 已将 " + self.hunter_ids[str(player_id)]["name"] + " 设置为猎人"

                for prey_id in self.prey_ids:
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(prey_id)
                    msg_comp.NotifyOneMessage(prey_id, prey_msg)
                for hunter_id, value in self.hunter_ids.items():
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(hunter_id)
                    msg_comp.NotifyOneMessage(hunter_id, prey_msg)

        elif message == "prey reset":
            operation_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
            operation = operation_comp.GetPlayerOperation()
            if operation >= 2:
                prey_msg = "系统： 已清空猎物人选"
                for prey_id in self.prey_ids:
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(prey_id)
                    msg_comp.NotifyOneMessage(prey_id, prey_msg)
                for hunter_id, value in self.hunter_ids.items():
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(hunter_id)
                    msg_comp.NotifyOneMessage(hunter_id, prey_msg)
                self.prey_ids = []

            else:
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                prey_msg = "系统： 权限不足"
                msg_comp.NotifyOneMessage(player_id, prey_msg)

        elif message == "hunter reset":
            operation_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
            operation = operation_comp.GetPlayerOperation()
            if operation >= 2:
                prey_msg = "系统： 已清空猎人人选"
                for prey_id in self.prey_ids:
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(prey_id)
                    msg_comp.NotifyOneMessage(prey_id, prey_msg)
                for hunter_id, value in self.hunter_ids.items():
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(hunter_id)
                    msg_comp.NotifyOneMessage(hunter_id, prey_msg)
                self.hunter_ids = {}

            else:
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                prey_msg = "系统： 权限不足"
                msg_comp.NotifyOneMessage(player_id, prey_msg)

        elif message == "pah reset":
            operation_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
            operation = operation_comp.GetPlayerOperation()
            if operation >= 2:
                prey_msg = "系统： 已清空猎物和猎人人选"
                for prey_id in self.prey_ids:
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(prey_id)
                    msg_comp.NotifyOneMessage(prey_id, prey_msg)
                for hunter_id, value in self.hunter_ids.items():
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(hunter_id)
                    msg_comp.NotifyOneMessage(hunter_id, prey_msg)
                self.prey_ids = []
                self.hunter_ids = {}

            else:
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                prey_msg = "系统： 权限不足"
                msg_comp.NotifyOneMessage(player_id, prey_msg)

    def on_chat_touch_button(self, data):
        # 获取玩家ID
        player_id = data['player_id']
        player_name = data['player_name']
        # 获取聊天消息
        message = data['message']
        print("touch_button")

        hunter_id_values = list(self.hunter_ids.keys())

        if message == "prey set":
            print("prey set")
            if player_id in hunter_id_values:
                for key, value in self.hunter_ids.items():
                    if key == player_id:
                        # 移除包含目标字符串的键
                        self.hunter_ids.pop(key)
                        break
            if player_id in self.prey_ids:
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                msg = "系统：你已经是猎物了"
                msg_comp.NotifyOneMessage(player_id, msg)

            else:
                self.prey_ids.append(player_id)
                player_name_comp = serverApi.GetEngineCompFactory().CreateName(player_id)
                player_name = player_name_comp.GetName()
                prey_msg = "系统： 已将 " + player_name + " 设置为猎物"

                player_id_list = serverApi.GetPlayerList()
                for player_id in player_id_list:
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                    msg_comp.NotifyOneMessage(player_id, prey_msg)

        elif message == "hunter set":
            print("hunter set")
            if player_id in self.prey_ids:
                self.prey_ids.remove(player_id)

            if player_id in hunter_id_values:
                for key, value in self.hunter_ids.items():
                    if key == player_id:
                        msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                        msg = "系统：你已经是猎物了"
                        msg_comp.NotifyOneMessage(player_id, msg)
                        break

            else:
                self.hunter_ids[str(player_id)] = {}
                self.hunter_ids[str(player_id)]["name"] = player_name
                self.hunter_ids[str(player_id)]["target"] = 0
                prey_msg = "系统： 已将 " + self.hunter_ids[str(player_id)]["name"] + " 设置为猎人"

                player_id_list = serverApi.GetPlayerList()
                for player_id in player_id_list:
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                    msg_comp.NotifyOneMessage(player_id, prey_msg)

        elif message == "prey reset":
            operation_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
            operation = operation_comp.GetPlayerOperation()
            if operation >= 2:
                prey_msg = "系统： 已清空猎物人选"
                player_id_list = serverApi.GetPlayerList()
                for player_id in player_id_list:
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                    msg_comp.NotifyOneMessage(player_id, prey_msg)
                self.prey_ids = []

            else:
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                prey_msg = "系统： 权限不足"
                msg_comp.NotifyOneMessage(player_id, prey_msg)

        elif message == "hunter reset":
            operation_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
            operation = operation_comp.GetPlayerOperation()
            if operation >= 2:
                prey_msg = "系统： 已清空猎人人选"
                player_id_list = serverApi.GetPlayerList()
                for player_id in player_id_list:
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                    msg_comp.NotifyOneMessage(player_id, prey_msg)
                self.hunter_ids = {}

            else:
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                prey_msg = "系统： 权限不足"
                msg_comp.NotifyOneMessage(player_id, prey_msg)

        elif message == "pah reset":
            print("pah reset")
            operation_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
            operation = operation_comp.GetPlayerOperation()
            if operation >= 2:
                prey_msg = "系统： 已清空猎物和猎人人选"
                player_id_list = serverApi.GetPlayerList()
                for player_id in player_id_list:
                    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                    msg_comp.NotifyOneMessage(player_id, prey_msg)
                self.prey_ids = []
                self.hunter_ids = {}

            else:
                msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
                prey_msg = "系统： 权限不足"
                msg_comp.NotifyOneMessage(player_id, prey_msg)

    # OnScriptTickServer的回调函数，会在引擎tick的时候调用，1秒30帧（被调用30次）
    def OnTickServer(self):
        """
        Driven by event, One tick way
        """
        pass

    # 这个Update函数是基类的方法，同样会在引擎tick的时候被调用，1秒30帧（被调用30次）
    def Update(self):
        """
        Driven by system manager, Two tick way
        """
        pass

    def Destroy(self):
        pass
