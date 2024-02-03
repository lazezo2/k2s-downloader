"""
360p: 640 x 360 pixels
460p: 816 x 460 pixels
160 120
320 240
480 360
640 360
816 460
"""
import os 
import sys

# Check if a URL is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python video_converter.py <file_id>")
    sys.exit(1)

# Get the URL from the command-line argument
file_id = sys.argv[1]


video_name = "/content/10.mp4"
#v_input = "/content/k2s-downloader/4363.mp4"
v_input = f"/content/k2s-downloader/{file_id}.mp4"
print(v_input)

#v_input = "/content/k2s-downloader/repaired_file.mp4"
#video_name = os.path.basename(v_input)
# Get the video name without the extension from the path
video_name_without_ext = os.path.splitext(os.path.basename(v_input))[0]

# Specify the directory name
directory_name = "1"
# Create the directory
if not os.path.isdir(f"/content/{directory_name}"):
   #os.makedirs(directory_name, exist_ok=True)
   os.makedirs(f"/content/{directory_name}")

#v_output =f"/content/{directory_name}/{video_name_without_ext}.mp4"
#a_output = f"/content/{directory_name}/{video_name_without_ext}.mp3"

v_output =f"/content/{directory_name}/{file_id}.mp4"
a_output = f"/content/{directory_name}/{file_id}.mp3"

#v_output = "2.mp4"
print(v_output)


video_low_quality = 0
video_high_quality = 1
sound_enable = 1


# [160 120] [320 240] [480 360] [640 360] [816 460]
# [160 120] [320 240] [480 360] [640 360] [816 460]
#320 180

# high qality
width=480
height=360
video_bitrate=30
audio_bitrate=50000
# video size in kb, not used
video_q=1500
#width=288
#height=512

#sound mp3 bitrate
mp3_q="30k"

#low quality video with no sound
width2=160
height2=120
video_bitrate2=30
audio_bitrate2=30000


start_t = "00:00:03"
end_t = "00:00:09"
start_t1 = "00:00:19"
end_t1 = "00:00:20"
to_end_of_video =0


#find duration
parts = start_t.split(":")
x1 = parts[2]
#print(x1)
parts1 = end_t.split(":")
y1 = parts1[2]
#print(y1)
z=int(y1)-int(x1)
#print(z)
if z < 10:
   duration = "00:00:0{}".format(z)
if z > 9:
   duration = "00:00:{}".format(z)
#print(duration)


def trim_low_join_no_sound(input_path, output_path, start=30, end=60):
    import os
    import ffmpeg
    input_stream = ffmpeg.input(input_path)

    vid = (
        input_stream.video
        .trim(start=start_t, end=end_t)
        .setpts('PTS-STARTPTS')
        #.filter('fps', fps=video_bitrate2)
        .filter('scale', width2, height2)
    )
    vid1 = (
        input_stream.video
        .trim(start=start_t1, end=end_t1)
        .setpts('PTS-STARTPTS')
        #.filter('fps', fps=video_bitrate2)
        .filter('scale', width2, height2)
    )

    #joined = ffmpeg.concat(vid, aud, vid1, aud1, v=1, a=1, vcodec='libx265', preset='fast', pix_fmt='yuv420p',map="0:a", acodec='libmp3lame', **{'c:a': 'aac', 'b:a': audio_bitrate2}).node
    #joined = ffmpeg.concat(vid, aud, vid1, aud1, v=1, a=1).node
    joined = ffmpeg.concat(vid, vid1,v=1).node

    '''
    #output = ffmpeg.output(joined[0], joined[1], output_path)
    #without sound
    output = ffmpeg.output(vid, output_path)
    #output = ffmpeg.output(vid, aud, output_path)

    output = ffmpeg.output(vid, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p')
    '''
    #output = ffmpeg.output(vid1, aud1,vid, aud, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p')

    #output.run()
    v3 = joined[0]
    #a3 = joined[1].filter('volume', 0.8)
    #a3 = joined[1]
    #out = ffmpeg.output(v3, a3, 'out1.mp4')
    out = ffmpeg.output(v3, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p')
    #out = ffmpeg.output(v3, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p', **{'ss':'00:00:00', 'to':duration3})
    out.run()

def trim_low_join_sound(input_path, output_path, start=30, end=60):
    import os
    import ffmpeg
    input_stream = ffmpeg.input(input_path)

    vid = (
        input_stream.video
        .trim(start=start_t, end=end_t)
        .setpts('PTS-STARTPTS')
        #.filter('fps', fps=video_bitrate2)
        .filter('scale', width2, height2)
    )
    aud = (
        input_stream.audio
        .filter_('atrim', start=start_t, end=end_t)
        .filter_('asetpts', 'PTS-STARTPTS')
    )
    vid1 = (
        input_stream.video
        .trim(start=start_t1, end=end_t1)
        .setpts('PTS-STARTPTS')
        #.filter('fps', fps=video_bitrate2)
        .filter('scale', width2, height2)
    )
    aud1 = (
        input_stream.audio
        .filter_('atrim', start=start_t1, end=end_t1)
        .filter_('asetpts', 'PTS-STARTPTS')
    )

    #joined = ffmpeg.concat(vid, aud, vid1, aud1, v=1, a=1, vcodec='libx265', preset='fast', pix_fmt='yuv420p',map="0:a", acodec='libmp3lame', **{'c:a': 'aac', 'b:a': audio_bitrate2}).node
    joined = ffmpeg.concat(vid, aud, vid1, aud1, v=1, a=1).node
    #joined = ffmpeg.concat(vid, vid1,v=1).node

    '''
    #output = ffmpeg.output(joined[0], joined[1], output_path)
    #without sound
    output = ffmpeg.output(vid, output_path)
    #output = ffmpeg.output(vid, aud, output_path)

    output = ffmpeg.output(vid, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p')
    '''
    #output = ffmpeg.output(vid1, aud1,vid, aud, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p')

    #output.run()
    v3 = joined[0]
    #a3 = joined[1].filter('volume', 0.8)
    #a3 = joined[1]
    #out = ffmpeg.output(v3, a3, 'out1.mp4')
    out = ffmpeg.output(v3, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p', **{'c:a': 'aac', 'b:a': audio_bitrate2})
    #out = ffmpeg.output(v3, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p', **{'c:a': 'aac', 'b:a': audio_bitrate2, 'ss':'00:00:00', 'to':duration3})

    out.run()


def trim_high_join_no_sound(input_path, output_path, start=30, end=60):
    import os
    import ffmpeg
    input_stream = ffmpeg.input(input_path)

    vid = (
        input_stream.video
        .trim(start=start_t, end=end_t)
        .setpts('PTS-STARTPTS')
        #.filter('fps', fps=video_bitrate)
        .filter('scale', width, height)
    )
    vid1 = (
        input_stream.video
        .trim(start=start_t1, end=end_t1)
        .setpts('PTS-STARTPTS')
        #.filter('fps', fps=video_bitrate)
        .filter('scale', width, height)
    )

    #joined = ffmpeg.concat(vid, aud, vid1, aud1, v=1, a=1, vcodec='libx265', preset='fast', pix_fmt='yuv420p',map="0:a", acodec='libmp3lame', **{'c:a': 'aac', 'b:a': audio_bitrate2}).node
    #joined = ffmpeg.concat(vid, aud, vid1, aud1, v=1, a=1).node
    joined = ffmpeg.concat(vid, vid1,v=1).node

    '''
    #output = ffmpeg.output(joined[0], joined[1], output_path)
    #without sound
    output = ffmpeg.output(vid, output_path)
    #output = ffmpeg.output(vid, aud, output_path)

    output = ffmpeg.output(vid, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p')
    '''
    #output = ffmpeg.output(vid1, aud1,vid, aud, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p')

    #output.run()
    v3 = joined[0]
    #a3 = joined[1].filter('volume', 0.8)
    #a3 = joined[1]
    #out = ffmpeg.output(v3, a3, 'out1.mp4')
    out = ffmpeg.output(v3, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p')
    #out = ffmpeg.output(v3, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p', **{'ss':'00:00:00', 'to':duration3})
    out.run()

def trim_high_join_sound(input_path, output_path, start=30, end=60):
    import os
    import ffmpeg
    input_stream = ffmpeg.input(input_path)

    vid = (
        input_stream.video
        .trim(start=start_t, end=end_t)
        .setpts('PTS-STARTPTS')
        #.filter('fps', fps=video_bitrate)
        .filter('scale', width, height)
    )
    aud = (
        input_stream.audio
        .filter_('atrim', start=start_t, end=end_t)
        .filter_('asetpts', 'PTS-STARTPTS')
    )
    vid1 = (
        input_stream.video
        .trim(start=start_t1, end=end_t1)
        .setpts('PTS-STARTPTS')
        #.filter('fps', fps=video_bitrate)
        .filter('scale', width, height)
    )
    aud1 = (
        input_stream.audio
        .filter_('atrim', start=start_t1, end=end_t1)
        .filter_('asetpts', 'PTS-STARTPTS')
    )

    #joined = ffmpeg.concat(vid, aud, vid1, aud1, v=1, a=1, vcodec='libx265', preset='fast', pix_fmt='yuv420p',map="0:a", acodec='libmp3lame', **{'c:a': 'aac', 'b:a': audio_bitrate2}).node
    joined = ffmpeg.concat(vid, aud, vid1, aud1, v=1, a=1).node
    #joined = ffmpeg.concat(vid, vid1,v=1).node

    '''
    #output = ffmpeg.output(joined[0], joined[1], output_path)
    #without sound
    output = ffmpeg.output(vid, output_path)
    #output = ffmpeg.output(vid, aud, output_path)

    output = ffmpeg.output(vid, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p')
    '''
    #output = ffmpeg.output(vid1, aud1,vid, aud, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p')

    #output.run()
    v3 = joined[0]
    #a3 = joined[1].filter('volume', 0.8)
    #a3 = joined[1]
    #out = ffmpeg.output(v3, a3, 'out1.mp4')
    out = ffmpeg.output(v3, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p', **{'c:a': 'aac', 'b:a': audio_bitrate})
    #out = ffmpeg.output(v3, output_path, vcodec='libx265', preset='fast', pix_fmt='yuv420p', **{'c:a': 'aac', 'b:a': audio_bitrate, 'ss':'00:00:00', 'to':duration3})
    out.run()


import os, ffmpeg

if not os.path.isfile(v_output):
   if video_high_quality==1 and sound_enable==1:

             # chat gpt optimised
             input_stream = ffmpeg.input(v_input)

             vid = (
                 input_stream.video
                 .filter('fps', fps=video_bitrate)
                 .filter('scale', width, height)
             )

             aud = (
                 input_stream.audio
             )

             output = ffmpeg.output(
                 vid, aud, v_output,
                 vcodec='libx265', preset='ultrafast', pix_fmt='yuv420p',
                 **{'c:a': 'aac', 'b:a': audio_bitrate}
             )

             output.run()

   if video_high_quality==1 and sound_enable==0:

             # chat gpt optimised
             input_stream = ffmpeg.input(v_input)

             vid = (
                 input_stream.video
                 .filter('fps', fps=video_bitrate)
                 .filter('scale', width, height)
             )

             # Set the audio stream to None to exclude it from the output
             aud = None

             output = ffmpeg.output(
                 vid, aud, v_output,
                 vcodec='libx265', preset='ultrafast', pix_fmt='yuv420p',
                 **{'c:a': 'aac', 'b:a': audio_bitrate}
             )

             output.run()

   if video_low_quality==1 and sound_enable==1:

             # chat gpt optimised
             input_stream = ffmpeg.input(v_input)

             vid = (
                 input_stream.video
                 .filter('fps', fps=video_bitrate2)
                 .filter('scale', width2, height2)
             )

             aud = (
                 input_stream.audio
             )

             output = ffmpeg.output(
                 vid, aud, v_output,
                 vcodec='libx265', preset='ultrafast', pix_fmt='yuv420p',
                 **{'c:a': 'aac', 'b:a': audio_bitrate2}
             )

             output.run()

   if video_low_quality==1 and sound_enable==0:

             # chat gpt optimised
             input_stream = ffmpeg.input(v_input)

             vid = (
                 input_stream.video
                 .filter('fps', fps=video_bitrate2)
                 .filter('scale', width2, height2)
             )

             aud = None

             output = ffmpeg.output(
                 vid, aud, v_output,
                 vcodec='libx265', preset='ultrafast', pix_fmt='yuv420p',
                 **{'c:a': 'aac', 'b:a': audio_bitrate2}
             )

             output.run()

   if video_low_quality==2 and sound_enable==0:

             # chat gpt optimised
             input_stream = ffmpeg.input(v_input)

             vid = (
                 input_stream.video
                 .filter('fps', fps=video_bitrate2)
                 .filter('scale', width2, height2)
             )

             # Set the audio stream to None to exclude it from the output
             aud = None

             output = ffmpeg.output(
                 vid, aud, v_output,
                 vcodec='libx265', preset='ultrafast', pix_fmt='yuv420p',
                 **{'ss': start_t, 't': duration}
             )

             output.run()

   if video_low_quality==2 and sound_enable==1:

             # chat gpt optimised
             input_stream = ffmpeg.input(v_input)

             vid = (
                 input_stream.video
                 .filter('fps', fps=video_bitrate2)
                 .filter('scale', width2, height2)
             )

             aud = (
                 input_stream.audio
             )

             output = ffmpeg.output(vid, aud, v_output, vcodec='libx265', preset='ultrafast', pix_fmt='yuv420p', **{'c:a': 'aac', 'b:a': audio_bitrate2, 'ss':start_t, 't':duration})
             output.run()

   if video_high_quality==2 and sound_enable==0:

             # chat gpt optimised
             input_stream = ffmpeg.input(v_input)

             vid = (
                 input_stream.video
                 .filter('fps', fps=video_bitrate)
                 .filter('scale', width, height)
             )

             # Set the audio stream to None to exclude it from the output
             aud = None

             output = ffmpeg.output(
                 vid, aud, v_output,
                 vcodec='libx265', preset='ultrafast', pix_fmt='yuv420p',
                 **{'c:a': 'aac', 'b:a': audio_bitrate, 'ss':start_t, 't':duration}
             )

             output.run()

   if video_high_quality==2 and sound_enable==1:

             # chat gpt optimised
             input_stream = ffmpeg.input(v_input)

             vid = (
                 input_stream.video
                 .filter('fps', fps=video_bitrate)
                 .filter('scale', width, height)
             )

             aud = (
                 input_stream.audio
             )

             output = ffmpeg.output(
                 vid, aud, v_output,
                 vcodec='libx265', preset='ultrafast', pix_fmt='yuv420p',
                 **{'c:a': 'aac', 'b:a': audio_bitrate, 'ss':start_t, 't':duration}
             )

             output.run()


   if video_low_quality==3 and sound_enable==0:
        trim_low_join_no_sound(v_input,v_output,start_t,end_t)
   if video_low_quality==3 and sound_enable==1:
        trim_low_join_sound(v_input,v_output,start_t,end_t)
   if video_high_quality==3 and sound_enable==0:
        trim_high_join_no_sound(v_input,v_output,start_t,end_t)
   if video_high_quality==3 and sound_enable==1:
        trim_high_join_sound(v_input,v_output,start_t,end_t)

if video_low_quality==0 and video_high_quality==0 and sound_enable==1:
             if not os.path.isfile(a_output):
              # chat gpt optimised
              (
                  ffmpeg
                  .input(v_input)
                  .output(a_output, **{'ab': mp3_q}, **{'y': None})
                  .overwrite_output()
                  .run()
              )

if os.path.isfile(v_output):
   print(f"file allready exist: {v_output}")
if os.path.isfile(a_output):
   print(f"file allready exist: {a_output}")