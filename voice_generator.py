import asyncio
import edge_tts


async def make_voice(text, voice, output_file):

    communicator = edge_tts.Communicate(
        text,
        voice
    )

    await communicator.save(
        output_file
    )


def generate_voice(
    text,
    voice="ur-PK-AsadNeural",
    output_file="voice.mp3"
):

    asyncio.run(
        make_voice(
            text,
            voice,
            output_file
        )
    )
