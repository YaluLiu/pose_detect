1. 拍摄视频，假设名为 test.mp4
2. 使用ffmpeg将视频分解为图片,放到名为test的文件夹下
# 创建文件夹
$  mkdir test
# 使用ffmpeg分解视频
$  ffmpeg -i test.mp4 test/%d.jpg
3. 使用tagplayer标注或者半自动标注对图片进行标注
4. 使用标注数据进行训练