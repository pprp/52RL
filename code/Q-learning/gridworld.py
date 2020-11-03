#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-

import gym
import turtle
import numpy as np

# turtle tutorial : https://docs.python.org/3.3/library/turtle.html


def GridWorld(gridmap=None, is_slippery=False):
    if gridmap is None:
        gridmap = ['SFFF', 'FHFH', 'FFFH', 'HFFG']
    env = gym.make("FrozenLake-v0", desc=gridmap, is_slippery=False)
    env = FrozenLakeWapper(env)
    return env

# 创造自己的环境，牛
class FrozenLakeWapper(gym.Wrapper):
    def __init__(self, env):
        gym.Wrapper.__init__(self, env)
        self.max_y = env.desc.shape[0]
        self.max_x = env.desc.shape[1]
        self.t = None
        self.unit = 80 # 控制间隔

    def draw_box(self, x, y, fillcolor='', line_color='gray'):
        # 画一个正方形
        self.t.up() # pull the pen up 不绘制任何图形
        self.t.goto(x * self.unit, y * self.unit) # 去到固定位置
        self.t.color(line_color) # 上色第一个是pencolor第二个是linecolor
        self.t.fillcolor(fillcolor) # 填充色
        self.t.setheading(90) # 设置方向
        self.t.down() #下笔如有神
        
        self.t.begin_fill()
        for _ in range(4):
            self.t.forward(self.unit)
            self.t.speed(0)
            self.t.right(90)
        self.t.end_fill()

    def move_player(self, x, y):
        self.t.up()
        self.t.setheading(90) # 设置朝向
        self.t.fillcolor('red')
        self.t.goto((x + 0.5) * self.unit, (y + 0.5) * self.unit) 
        # 绘制小乌龟

    def render(self):
        if self.t == None:
            # 第一次，进行创建
            self.t = turtle.Turtle()
            self.wn = turtle.Screen()

            self.wn.setup(self.unit * self.max_x + 100,
                          self.unit * self.max_y + 100)
            
            # 设置初始坐标系
            self.wn.setworldcoordinates(0, 0, self.unit * self.max_x,
                                        self.unit * self.max_y)
            self.t.shape('circle')
            self.t.width(1)
            self.t.speed(0) 
            # 0： fastest 10: fast 
            # 6: normal slow:3 slowest: 1
            self.t.color('gray')

            for i in range(self.desc.shape[0]):
                for j in range(self.desc.shape[1]):
                    x = j
                    y = self.max_y - 1 - i
                    if self.desc[i][j] == b'S':  # Start
                        self.draw_box(x, y, 'white')
                    elif self.desc[i][j] == b'F':  # Frozen ice
                        self.draw_box(x, y, 'white')
                    elif self.desc[i][j] == b'G':  # Goal
                        self.draw_box(x, y, 'yellow')
                    elif self.desc[i][j] == b'H':  # Hole
                        self.draw_box(x, y, 'black')
                    else:
                        self.draw_box(x, y, 'white')
            self.t.shape('turtle')

        x_pos = self.s % self.max_x
        y_pos = self.max_y - 1 - int(self.s / self.max_x)
        # 移动到开始地点
        self.move_player(x_pos, y_pos)



if __name__ == '__main__':
    # 环境1：FrozenLake, 可以配置冰面是否是滑的
    # 0 left, 1 down, 2 right, 3 up
    # env = gym.make("FrozenLake-v0", is_slippery=False)
    # env = FrozenLakeWapper(env)

    # 环境2：CliffWalking, 悬崖环境
    # env = gym.make("CliffWalking-v0")  # 0 up, 1 right, 2 down, 3 left
    # env = CliffWalkingWapper(env)

    # 环境3：自定义格子世界，可以配置地图, S为出发点Start, F为平地Floor, H为洞Hole, G为出口目标Goal
    gridmap = [
            'SFFFFF',
            'FHFFFF',
            'FFFFFF',
            'HFGFFF' ]
    env = GridWorld(gridmap)

    env.reset()
    for step in range(10):
        action = np.random.randint(0, 4)
        obs, reward, done, info = env.step(action)
        print('step {}: action {}, obs {}, reward {}, done {}, info {}'.format(\
                step, action, obs, reward, done, info))
        # env.render() # 渲染一帧图像