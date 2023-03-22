# -*- coding:utf-8 -*-
# @Time    : 2022/12/20 17:45
# @Author  : Ray Lam YL

from moviepy.editor import *


# read
def v_sg(clip):  # 读视频信息(片段)  宽，高
    print('【视频】时长：{} w/h：{} fps：{}'.format(clip.duration, clip.size, clip.fps))


def au_sg(clip):  # 读音频时长(片段)
    print('【音频】时长：{} '.format(clip.duration))


# clip

def v_read(v_path, audio=True):  # videofileclip读取本地视频，解决多次运行读取后出句柄错误的问题
    clip = VideoFileClip(v_path, audio=audio)
    if clip != None:
        clip.reader.close()
    else:
        pass
    if clip.audio != None:
        clip.audio.reader.close_proc()
    else:
        pass
    return clip


def v_jie(clip, start, end):  # 截片段（片段，开始，结束时间）
    return clip.subclip(start, end)


def v_speed(clip, beisu):  # 调速度(片段，倍速)
    return clip.fx(vfx.speedx, beisu)


def v_color(clip, lit):  # 调画面颜色(片段，颜色比率) 应该是画面的gbk值分别乘这个率，应理解为颜色鲜度，过小变暗，大于1颜色变鲜明，过大颜色失真
    return clip.fx(vfx.colorx, lit)


def v_resize(clip, whnumorrate):  # 调视频尺寸(片段,等比例缩放比率或宽高元组)
    return clip.resize(whnumorrate)


def v_pos(clip, wh):  # 设位置 (片段，（宽比例，高比例) 0~1
    return clip.set_position(wh, relative=True)


def v_quyu(clip, x1, y1, x2, y2):  # 截取片段特定区域,x1,y1,x2,y2
    return clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)


def v_mir_x(clip):  # 左右颠倒
    return clip.fx(vfx.mirror_x)


def v_mir_y(clip):  # 上下颠倒
    return clip.fx(vfx.mirror_y)


def v_marg(clip, marg):  # 设外边框线宽
    return clip.margin(marg)


def v_rotate(clip, angle):  # 旋转视频（片段，角度） 角度正数是逆时针，负数顺时针
    return clip.rotate(angle)


def v_vol(clip, rate):  # 调音量(片段，音量比率)
    return clip.volumex(rate)


def v_bw(clip):  # 变黑白视频
    return clip.fx(vfx.blackwhite)


def p_clip(piclist, fp):  # 图片连成视频（[图地址1，图地址2.。]或文件夹地址，fps）   图片size要一致
    return ImageSequenceClip(piclist, fps=fp)


def v_scroll(clip, w, h, x_speed, y_speed, x_start,
             y_start):  # 画面滚动，speed可正可负，方向相反，wh为显示区域大小，speed每秒滚动像素，start为从clip哪点开始滚动
    return clip.fx(vfx.scroll, w, h, x_speed, y_speed, x_start, y_start)


def v_move(clip, direction='u', speed=None, size=200):
    # 例：如选u，镜头往下，画面向上滚动，选l，镜头向右，画面向左滚动。如选up,down，size要小于视频的高，选left,right，size要小于视频宽
    # speed如要填数字，当滚动越界，画面会错乱，建议填None自动调整或对clip进行时间裁剪
    if speed != None:
        speed = int(speed)
    elif speed == None and (direction == 'u' or direction == 'd'):
        speed = int((clip.h - size) / clip.duration)
    else:
        speed = int((clip.w - size) / clip.duration)
    print(speed)
    if direction == 'u':
        fl = lambda gf, t: gf(t)[int(speed * t):int(speed * t) + size, :]
    elif direction == 'd':
        fl = lambda gf, t: gf(t)[int(clip.h - size - speed * t):int(clip.h - speed * t), :]
    elif direction == 'r':
        fl = lambda gf, t: gf(t)[:, int(clip.w - size - speed * t):int(clip.w - speed * t)]
    else:
        fl = lambda gf, t: gf(t)[:, int(speed * t):int(speed * t) + size]
    return clip.fl(fl, apply_to=['mask']).set_pos(('center', 'center'))


def v_freeze(clip, frze_time, frze_duration):  # 视频画面冻结，frze_time是截取clip的哪个时点画面，再按frze_duration时间定格延长该画面
    return clip.fx(vfx.freeze, frze_time, frze_duration)


def v_time_mir(clip):  # 视频倒放。如出错误，可能原clip最后一帧无数据，参考：将输入的clip改为clip.subclip(0,clip.duration-0.1) ,此操作十分耗时
    return clip.fx(vfx.time_mirror)


def v_loop(clip, n, dur):  # 循环 次数n ,loop后时长dur 注意音频与视频时长不等报错，可在VideoFileClip时audio=False去除视频
    return clip.fx(vfx.loop, n, dur)


def v_col_danrudanchu(clip, inout='in', dur=2, color=(125, 125, 125)):  # 视频做颜色淡入或淡出 in 为淡入，out为淡出
    if inout == 'in':
        return clip.fx(vfx.fadein, duration=dur, initial_color=color)
    else:
        return clip.fx(vfx.fadeout, duration=dur, final_color=color)


def v_col_change(clip):  # 色彩反相
    return clip.fx(vfx.invert_colors)


def au_loop(audio_clip, dur):
    return afx.audio_loop(audio_clip, duration=dur)


def col_mask(size=(130, 60), color=(255, 0, 0), pos=(50, 100), dur=3,
             start=0):  # 颜色遮罩返回clip，此clip放在v_duidie的clip列表参数最后一个
    mask = ColorClip(size, color).set_position(pos).set_duration(dur).set_start(start)
    return mask


def pic_mask(picture_path, pos=(50, 100), dur=3, start=0):  # 图片遮罩返回clip，可加resize调整大小，此clip放在v_duidie的clip列表参数最后一个
    mask = ImageClip(picture_path).set_position(pos).set_duration(dur).set_start(start)
    return mask


# conbine
def au_duidie(au_list):  # 多音轨堆叠（[au_clip1,au_clip2]）
    return CompositeAudioClip(au_list)


def au_lianjie(au_list):  # 多音轨首尾接续（[au_clip1,au_clip2]）
    return concatenate_audioclips(au_list)


def v_lianjie(clip_list):  # 首尾连接片段（[片段1，片段2，片段3.。。]）
    return concatenate_videoclips(clip_list)  # 如报错，括号内要增加参数method=‘compose’


def v_pingpu(clip_2Dlist):  # 视频平铺（片段二维列表） 可多行，但每列clip数量要一致
    return clips_array(clip_2Dlist)


def v_duidie(v_list):  # 叠加合并视频（[videoclip,textclip,imgclip] 以第一个为背景大小
    return CompositeVideoClip(v_list)


def v_au_hebing(clip,
                au_clip):  # 视加音频(clip,au_clip)  此函数暂不用，因write_videofile生成文件没有声音，网上较多网友反馈同样问题，且网上解决方法都不能解决，应是moviepy本身问
    if clip.duration == au_clip.duration:
        return clip.set_audio(au_clip)
    else:
        print('音视频时长不一致不能合并')


def v_au_hegingff(clip, au_clip, v_path, au_path,
                  hebing_path):  # 因write_videofile生成文件没有声音，网上较多网友反馈同样问题，且网上解决方法都不能解决，应是moviepy本身问题，此函数直接用ffmpeg.exe命令行合并视频音频
    if clip.duration == au_clip.duration:
        os.system('ffmpeg.exe -i {} -i {} -acodec copy -vcodec copy {}'.format(au_path, v_path, hebing_path))
    else:
        print('音视频时长不一致不能合并')


