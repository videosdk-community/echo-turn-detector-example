from videosdk.agents import Agent, AgentSession, Pipeline, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.openai import OpenAILLM
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.elevenlabs import ElevenLabsTTS
from videosdk.plugins.silero import SileroVAD

from videosdk.agents.inference import TurnV2

class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are VideoSDK's Voice Agent. You are a helpful voice assistant "
                "that can answer questions about the weather. "
                "IMPORTANT: don't generate responses above 2 lines."
            ),
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")  #type: ignore
    
    async def on_exit(self) -> None:
        await self.session.say("Goodbye!") #type: ignore 


async def start_session(context: JobContext):
    agent = MyVoiceAgent()
    
    # Fastest, lowest latency (default)
    turn_detector = TurnV2.echo_small()

    # Higher accuracy
    # turn_detector = TurnV2.echo_large()

    pipeline = Pipeline(
        stt=DeepgramSTT(),
        llm=OpenAILLM(),
        tts=ElevenLabsTTS(),
        vad=SileroVAD(),
        turn_detector=turn_detector
    )
    
    @pipeline.on("turn_state")
    async def on_turn_state(data: dict):
        # data = {"text": str, "state": "Complete" | "Incomplete" |
        #    "Backchannel" | "Wait" }
        print(f"[TURN] state={data['state']} text={data['text']!r}")


    session = AgentSession(
        agent=agent,
        pipeline=pipeline,
    )
    
    
    await session.start(wait_for_participant=True, run_until_shutdown=True)

def make_context() -> JobContext:
    
    room_options = RoomOptions(
        name="Echo Turn Agent",
        playground=True,
    )
    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()
