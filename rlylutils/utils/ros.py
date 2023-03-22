# -*- coding:utf-8 -*-
# @Time    : 2023/3/22 11:19
# @Author  : Ray Lam YL

all=['Ros']

class Ros:
    def __init__(self):
        ...

    @staticmethod
    def show_step():
        print('-'*30)
        print('sudo vi /opt/ros/noetic/rosdistro/rosdep/sources.list.d/20-default.list')
        print('''
yaml file:///opt/ros/noetic/rosdistro/rosdep/osx-homebrew.yaml osx
yaml file:///opt/ros/noetic/rosdistro/rosdep/base.yaml
yaml file:///opt/ros/noetic/rosdistro/rosdep/python.yaml
yaml file:///opt/ros/noetic/rosdistro/rosdep/ruby.yaml
gbpdistro file:///opt/ros/noetic/rosdistro/releases/fuerte.yaml fuerte
        ''')
        print('-'*30)

        print('sudo vi /usr/lib/python3/dist-packages/rosdep2/gbpdistro_support.py')
        print("改：FUERTE_GBPDISTRO_URL = 'file:///opt/ros/noetic/rosdistro/releases/fuerte.yaml'")

        print('sudo vi /usr/lib/python3/dist-packages/rosdep2/rep3.py')
        print("改：REP3_TARGETS_URL = 'file:///opt/ros/noetic/rosdistro/releases/targets.yaml'")

        print('sudo vi /usr/lib/python3/dist-packages/rosdistro/__init__.py')
        print("改：DEFAULT_INDEX_URL = 'file:///opt/ros/noetic/rosdistro/index-v4.yaml'")

        print('-' * 30)
        print('sudo mkdir -p /etc/ros/rosdep/sources.list.d')
        print('sudo vi /etc/ros/rosdep/sources.list.d/20-default.list')
        print('''
yaml file:///opt/ros/noetic/rosdistro/rosdep/osx-homebrew.yaml osx
yaml file:///opt/ros/noetic/rosdistro/rosdep/base.yaml
yaml file:///opt/ros/noetic/rosdistro/rosdep/python.yaml
yaml file:///opt/ros/noetic/rosdistro/rosdep/ruby.yaml
gbpdistro file:///opt/ros/noetic/rosdistro/releases/fuerte.yaml fuerte
                ''')
        print('-' * 30)

