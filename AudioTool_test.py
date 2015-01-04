from auana import AudioTool

at = AudioTool.AudioTool()
at.record_play(seconds=2,play=True,file_play_path="C:/Users/b51762/Desktop/Auana-P/sample/10.wav",file_save_path="E:/1.wav")
# at.play("C:/Users/b51762/Desktop/Auana-P/sample/10.wav")
at.close()