#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
慧生活798积分签到脚本
通过抓包获取API接口，实现自动签到功能
"""

import json
import logging
import os
import sys
import time
from datetime import datetime
import requests


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('check_in.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class HuiShenghuo798:
    """慧生活798签到客户端"""
    
    def __init__(self, config_file='config.json'):
        """初始化客户端
        
        Args:
            config_file: 配置文件路径
        """
        self.config = self._load_config(config_file)
        self.session = requests.Session()
        self._setup_session()
        
    def _load_config(self, config_file):
        """加载配置文件
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            dict: 配置信息
        """
        if not os.path.exists(config_file):
            logger.error(f"配置文件不存在: {config_file}")
            logger.info("请复制 config.example.json 为 config.json 并填入正确的配置")
            sys.exit(1)
            
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"配置文件格式错误: {e}")
            sys.exit(1)
    
    def _setup_session(self):
        """设置请求会话的headers"""
        self.session.headers.update({
            'User-Agent': self.config.get('user_agent', 'Mozilla/5.0'),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        
        # 如果配置中有token，添加到headers
        if 'token' in self.config and self.config['token']:
            self.session.headers.update({
                'Authorization': f"Bearer {self.config['token']}"
            })
    
    def check_in(self):
        """执行签到操作
        
        Returns:
            bool: 签到是否成功
        """
        logger.info("开始执行签到...")
        
        try:
            # 从配置文件读取API信息
            api_base = self.config.get('api_base_url', 'https://api.example.com')
            check_in_path = self.config.get('check_in_path', '/checkin')
            url = f"{api_base}{check_in_path}"
            
            data = {
                'phone': self.config.get('phone', ''),
                'timestamp': int(time.time() * 1000)
            }
            
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            # 根据实际API返回格式判断签到是否成功
            if result.get('code') == 0 or result.get('success'):
                logger.info(f"签到成功！{result.get('message', '')}")
                return True
            else:
                logger.warning(f"签到失败: {result.get('message', '未知错误')}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"网络请求失败: {e}")
            return False
        except Exception as e:
            logger.error(f"签到过程发生错误: {e}")
            return False
    
    def get_points(self):
        """查询当前积分
        
        Returns:
            int: 当前积分数，失败返回None
        """
        logger.info("查询当前积分...")
        
        try:
            # 从配置文件读取API信息
            api_base = self.config.get('api_base_url', 'https://api.example.com')
            points_path = self.config.get('points_path', '/points')
            url = f"{api_base}{points_path}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            points = result.get('data', {}).get('points', 0)
            logger.info(f"当前积分: {points}")
            return points
            
        except requests.exceptions.RequestException as e:
            logger.error(f"查询积分失败: {e}")
            return None
        except Exception as e:
            logger.error(f"查询积分过程发生错误: {e}")
            return None


def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("慧生活798积分签到脚本启动")
    logger.info(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)
    
    try:
        # 创建客户端实例
        client = HuiShenghuo798()
        
        # 执行签到
        success = client.check_in()
        
        # 查询积分
        if success:
            time.sleep(1)  # 等待1秒后查询积分
            client.get_points()
        
        logger.info("=" * 50)
        logger.info("脚本执行完成")
        logger.info("=" * 50)
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        logger.info("用户中断执行")
        return 1
    except Exception as e:
        logger.error(f"程序执行出错: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
