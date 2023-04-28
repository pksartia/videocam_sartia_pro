from moviepy.editor import *
import itertools

from PIL import ImageFont


def test_video(video, logo,  text, profile, user_name, output_file):
    clip = VideoFileClip(video)
    clip = clip.resize(width=clip.w+30, height=clip.h+180)


# Add a watermark to the video
    watermark = (ImageClip(logo)
                 .set_duration(clip.duration)
                 .set_position(('left', 'top')))
    watermark1 = (ImageClip(profile)
                  .set_duration(clip.duration)
                  .set_position(('right', 'top')))

    # Add a frame to the videoxzxzxzZz
    frame = (ImageClip('public/line_new.png')
             .resize(width=clip.w-1)
             .set_duration(clip.duration)
             .set_position(('center', 'center')))
    user = (TextClip(user_name,
                     font='TiroDevanagariHindi-Regular.ttf',
                     fontsize=60,
                     color='blue',

                     )
            .set_position(('right', 150))
            .set_duration(clip.duration))

    # Create the base text clip
    text = (TextClip(text,
                     font='MANGAL.TTF',
                     fontsize=60,
                     color='white',

                     )
            .set_position(('right', 'bottom'))
            .set_duration(clip.duration))

    # Create a list of text clips with different start times and positions
    text_clips = []
    print('total height', clip.h)
    print("changed height", clip.h-120)
    for i in range(10):
        # Set the start and end times of the text clip
        text_clip = text.set_start(i * 2).set_end((i + 1) * 2)

        # Use itertools.cycle to create an infinite iterator that repeats the x-position
        x_pos = itertools.cycle(range(clip.w, -text_clip.w, -10))
        def x(t): return (next(x_pos), clip.h-120)
        text_clip = text_clip.set_position(x)

        text_clips.append(text_clip)

    # Combine the clips into a single video
    final_clip = CompositeVideoClip(
        [clip] + [watermark, watermark1, user, frame] + text_clips)

    # Write the output video file
    final_clip.write_videofile(output_file)

    


