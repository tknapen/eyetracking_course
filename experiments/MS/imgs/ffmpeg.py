import os, glob
input_file = "fn_input.mkv"
output_cut_format = "fn_output_{language}_{segment_index}.mkv"
output_slow_format = "fn_output_{language}_{segment_index}_ss.mp4"
duration = 120

segment_time_stamps = ["00:5:29", "00:12:15", "00:16:47", "00:25:32", "00:33:36", "00:41:49", "00:51:25", "00:55:46", "01:17:07", "01:21:06", "01:30:52"]

ffmpeg_cut_format = 'ffmpeg -i {input_file} -map 0:a:{lan_index} -map 0:v:0 -ss {segment_time} -t {duration} {op_filename}'
ffmpeg_slow_format = 'ffmpeg -i {input_file} -filter_complex "[0:v]setpts=1.25*PTS[v];[0:a]atempo=0.8[a]" -map "[v]" -map "[a]" {op_filename}'


for segment_index, segment_time in enumerate(segment_time_stamps):
    for lan_index, language in zip([0,1],['EN','IT']):
        op_cut_filename = output_format.format(language=language, segment_index=segment_index)
        op_slow_filename = output_slow_format.format(language=language, segment_index=segment_index)

        this_ffmpeg_cut_cmd = ffmpeg_cut_format.format(
            input_file=input_file,
            lan_index=lan_index,
            segment_time=segment_time,
            duration=duration,
            op_filename=op_cut_filename
        )
        print(this_ffmpeg_cut_cmd)
        os.system(this_ffmpeg_cut_cmd)

        this_ffmpeg_slow_cmd = ffmpeg_slow_format.format(
            input_file=op_cut_filename,
            op_filename=op_slow_filename
        )
        print(this_ffmpeg_slow_cmd)
        os.system(this_ffmpeg_slow_cmd)


ffmpeg_conv_audio_format = 'ffmpeg -i {input_file} -c:v copy -c:a adpcm_ima_wav -ac 2 {op_filename}'


for f in glob.glob('*_ss.mp4'):
    this_audio_conv = ffmpeg_conv_audio_format.format(
        input_file=f,
        op_filename=f.replace('_ss.mp4', '_ss_pcm.avi')
        )
    print(this_audio_conv)
    os.system(this_audio_conv)