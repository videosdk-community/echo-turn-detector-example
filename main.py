from videosdk.agents import Agent, AgentSession,Pipeline, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.silero import SileroVAD
from videosdk.agents.inference import LLM, TTS, STT


from videosdk.agents.inference import TurnV2

class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are VideoSDK's Voice Agent. You are a helpful voice assistant "
                "that can answer questions about the weather. "
                "when ever user asks for the joke tell them this joke : 'Why did the dinosaur cross the road? Because chickens didn't exist yet'"
            ),
            use_base_instructions=True
        )
        


    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")  #type: ignore
    
    async def on_exit(self) -> None:
        await self.session.say("Goodbye!") #type: ignore 


async def start_session(context: JobContext):
    agent = MyVoiceAgent()
    
    # Fastest, lowest latency (default)
    echo_turn_detector = TurnV2.echo_small()

    # Higher accuracy
    # echo_turn_detector = TurnV2.echo_large()

    pipeline =  Pipeline(
        stt=STT.deepgram(),
        llm=LLM.google(),
        tts=TTS.cartesia(),
        vad=SileroVAD(),
        turn_detector=echo_turn_detector,
    )
    
    @pipeline.on("turn_state")
    async def on_turn_state(data: dict):
        # data = {"text": str, "state": "Complete" | "Incomplete" |
        #    "Backchannel" | "Wait" }
        print(f"\n[TURN] state={data['state']} text={data['text']!r}")

    @pipeline.metrics.on("eou")
    def on_eou_metrics(metrics: dict):
        """Fired when TurnDetector matches end-of-utterance."""
        print(
            f"\n[METRICS] EOU Latency: {metrics.get('eou_latency')}ms | "
            f"EOU Wait: {metrics.get('eou_wait_ms')}ms"
        )
        
    @pipeline.on("llm")
    async def on_llm(data: dict):
        text = data.get("text", "")
        print(f"\nLLM generated: {text[:100]}...")


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
