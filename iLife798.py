"""
慧生活798积分获取脚本
功能：自动签到、观看视频获取积分
支持青龙面板多账号
环境变量：
- HUI798_AUTH:  多个授权令牌，支持多种分隔符(&、#、@、|、,)
"""

import requests
import json
import time
import os
from datetime import datetime


def get_auth_from_env():
    """从环境变量获取授权令牌列表，支持多种格式"""
    auth_env = os.getenv('HUI798_AUTH', '')
    
    if not auth_env: 
        print("❌ 未找到环境变量 HUI798_AUTH，请设置后重试")
        print("💡 设置方法：")
        print("   单个账号：export HUI798_AUTH='你的授权令牌'")
        print("   多个账号：export HUI798_AUTH='token1&token2&token3'")
        return []
    
    # 支持多种分隔符：& # @ | ,
    for separator in ['&', '#', '@', '|', ',']:
        if separator in auth_env:
            auths = [auth.strip() for auth in auth_env.split(separator) if auth.strip()]
            print(f"✅ 从环境变量获取到 {len(auths)} 个账号")
            return auths
    
    auths = [auth_env.strip()]
    print(f"✅ 从环境变量获取到 {len(auths)} 个账号")
    return auths


class HuiLife798:
    """慧生活798积分管理类"""
    
    def __init__(self, authorization):
        self.authorization = authorization
        self.base_url = "https://i.ilife798.com/api/v1/acc/score"
        self. login_expired = False
        self.headers = {
            'User-Agent': "Android_ilife798_2.0.9",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json",
            'authorization': self.authorization,
            'applicationtype': "1,1",
            'versioncode': "2.0.9",
            'content-type': "application/json; charset=UTF-8"
        }
    
    def _send_request(self, endpoint, method='POST', payload=None, retry_on_frequent=True):
        """发送HTTP请求"""
        url = f"{self. base_url}/{endpoint}"
        
        try:
            if method. upper() == 'POST':
                response = requests.post(url, data=json.dumps(payload), headers=self.headers)
            else:
                response = requests.get(url, headers=self. headers)
            
            if endpoint == "mission-lst" and response.status_code == 200:
                try:
                    resp_data = response. json()
                    if resp_data.get('code') == -99: 
                        print("   ❌ 登录状态已过期，需要切换账号")
                        self.login_expired = True
                        return None
                except json.JSONDecodeError:
                    pass
            
            if retry_on_frequent and response.status_code == 200:
                try:
                    resp_data = response. json()
                    if resp_data. get('code') == -98:
                        print("   ⚠️  请求过于频繁，等待5秒后重试...")
                        time. sleep(5)
                        if method.upper() == 'POST':
                            response = requests.post(url, data=json.dumps(payload), headers=self.headers)
                        else:
                            response = requests.get(url, headers=self.headers)
                        print(f"   🔄 重试响应: {response. text}")
                except json. JSONDecodeError: 
                    pass
            
            return response
        except Exception as e:
            print(f"请求失败: {e}")
            return None
    
    def get_mission_list(self):
        """获取任务列表"""
        print("=" * 60)
        print("📋 获取任务列表")
        print("=" * 60)
        
        response = self._send_request("mission-lst", method='GET')
        if response:
            try: 
                data = response.json()
                
                if 'data' in data and 'accScoreRsp' in data['data']:
                    acc_info = data['data']['accScoreRsp']
                    print(f"👤 用户信息:")
                    print(f"   📍 地址: {acc_info.get('address', {}).get('prov', '')} {acc_info.get('address', {}).get('city', '')}")
                    print(f"   🎯 当前积分: {acc_info.get('score', 0)}")
                    print(f"   📊 总积分: {acc_info.get('totalScore', 0)}")
                    print(f"   ✅ 有效积分: {acc_info.get('validScore', 0)}")
                    print()
                
                if 'data' in data and 'dailyRSP' in data['data']:
                    daily_info = data['data']['dailyRSP']
                    print(f"📅 签到信息:")
                    print(f"   💰 每日签到积分: {daily_info.get('score', 0)}")
                    if 'config' in daily_info:
                        for config in daily_info['config']:
                            print(f"   🎁 {config.get('title', '').replace('%s', str(int(config.get('score', 0))))}:  {config.get('msg', '')}")
                    print()
                
                if 'data' in data and 'missions' in data['data']:
                    missions = data['data']['missions']
                    print(f"📝 可用任务 ({len(missions)}个):")
                    for i, mission in enumerate(missions, 1):
                        print(f"   {i}. {mission. get('name', '未知任务')}")
                        print(f"      💰 奖励: {mission.get('score', 0)}积分")
                        print(f"      📄 描述: {mission.get('desc', '无描述')}")
                        print()
                
                return data
                
            except json.JSONDecodeError:
                print("❌ 响应格式错误，无法解析JSON")
                return None
        elif self.login_expired:
            print("❌ 任务列表获取失败：登录状态已过期")
            return None
        return None
    
    def daily_check_in(self):
        """每日签到（仅当天）"""
        current_weekday = datetime.now().weekday() + 1
        
        print("=" * 60)
        print(f"📅 开始当天签到 (星期{current_weekday})")
        print("=" * 60)
        
        payload = {
            "adId": "DAILY_CHECK_IN",
            "addScore": 5,
            "addScoreType": 1,
            "weekday": current_weekday
        }
        
        print(f"📝 今天签到 (weekday={current_weekday})")
        response = self._send_request("score-send", payload=payload)
        
        if response: 
            print(f"   响应: {response. text}")
            try:
                resp_data = response. json()
                if resp_data.get('code') == 0:
                    print("   ✅ 签到成功")
                else:
                    print(f"   ❌ 签到失败: {resp_data.get('msg', '未知错误')}")
            except json. JSONDecodeError: 
                if response.status_code == 200:
                    print("   ✅ 签到成功")
        print()
    
    def watch_videos(self, max_count=5):
        """观看视频获取积分"""
        print("=" * 60)
        print("📺 开始观看视频获取积分")
        print("=" * 60)
        
        success_count = 0
        
        for i in range(1, max_count + 1):
            payload = {
                "adId": "1705776998",
                "addScore": 30,
                "addScoreType": 2,
                "type": 101
            }
            
            print(f"🎬 第{i}次观看视频")
            response = self._send_request("score-send", payload=payload)
            
            if response: 
                print(f"   响应:  {response.text}")
                try: 
                    resp_data = response.json()
                    if resp_data.get('code') == 0:
                        success_count += 1
                        print("   ✅ 观看视频成功")
                    else:
                        print(f"   ❌ 观看视频失败: {resp_data.get('msg', '未知错误')}")
                except json.JSONDecodeError: 
                    if response.status_code == 200:
                        success_count += 1
            
            print("-" * 40)
            
            if i < max_count: 
                print("⏳ 等待5秒...")
                time.sleep(5)
        
        print(f"✅ 观看视频完成，成功次数: {success_count}/{max_count}")
        print()
    
    def run_daily_tasks(self):
        """执行每日任务"""
        print("🌅 执行每日任务")
        print(f"⏰ 执行时间: {datetime. now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        self.get_mission_list()
        self.daily_check_in()
        
        print("⏳ 签到完成，等待10秒后开始观看视频...")
        time.sleep(10)
        
        self.watch_videos(max_count=5)
        print("🎉 每日任务执行完成！")


def run_single_account(authorization, account_index, total_accounts):
    """运行单个账号的任务"""
    print("=" * 80)
    print(f"🎯 账号 {account_index}/{total_accounts} - 开始执行任务")
    print(f"🔐 授权令牌: {authorization[: 10]}...{authorization[-10:]}")
    print("=" * 80)
    
    hui_life = HuiLife798(authorization)
    
    try:
        hui_life.get_mission_list()
        
        if hui_life.login_expired:
            print(f"❌ 账号 {account_index} 登录状态已过期，跳过此账号")
            return False
        
        hui_life.run_daily_tasks()
        print(f"✅ 账号 {account_index} 任务执行完成")
        
    except Exception as e:
        print(f"❌ 账号 {account_index} 执行失败: {e}")
        return False
    
    return True


def main():
    """主函数"""
    print("🚀 慧生活798积分获取脚本启动")
    print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    auth_tokens = get_auth_from_env()
    
    if not auth_tokens:
        print("❌ 未找到有效的授权令牌")
        return
    
    print(f"📱 账号数量: {len(auth_tokens)}")
    print()
    
    success_count = 0
    
    for i, auth_token in enumerate(auth_tokens, 1):
        try: 
            if run_single_account(auth_token, i, len(auth_tokens)):
                success_count += 1
            
            if i < len(auth_tokens):
                print(f"⏳ 账号间隔等待15秒...")
                time.sleep(15)
                print()
                
        except KeyboardInterrupt: 
            print(f"\n\n⚠️  用户中断，已处理 {i-1}/{len(auth_tokens)} 个账号")
            break
        except Exception as e: 
            print(f"❌ 账号 {i} 发生未知错误: {e}")
            continue
    
    print("=" * 80)
    print(f"🎉 所有账号处理完成")
    print(f"📊 成功: {success_count}/{len(auth_tokens)} 个账号")
    print(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == "__main__":
    main()
