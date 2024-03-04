Well this is just a simple bot

To stream all you want

---
## Roadmap

### v0

- Streaming input and output to/from the bot
- No streaming within the bot

```mermaid
sequenceDiagram
    Client-->> Server: Audio
    Client-->> Server: 
    Client-->> Server: 
    Client --x Server: EOU
    Server ->> ASR: Audio
    ASR ->> LLM: Transcript
    LLM ->> TTS: Text
    TTS ->> Server: Audio
    Server-->> Client: Audio
    Server-->> Client: 

```

### v1

- Streaming input and output to/from the bot

> - **Streaming input to ASR and endpointing (~EOU detection)**
> - **Streaming output from TTS**

```mermaid
sequenceDiagram
    Client-->> Server: Audio
    Client-->> Server: 
    Client-->> Server: 
    Server-->> ASR: Audio
    Server-->> ASR: 
    ASR --x Server: EOU
    ASR ->> LLM: Transcript
    LLM ->> TTS: Text
    TTS-->> Server: Audio
    TTS-->> Server: 
    Server-->> Client: Audio
    Server-->> Client: 

```

### v2

- Streaming input and output to/from the bot
- Streaming input to ASR and endpointing (~EOU detection)

> - **Streaming output from LLM** 
> - **Streaming input and output to/from TTS**

```mermaid
sequenceDiagram
    Client-->> Server: Audio
    Client-->> Server: 
    Client-->> Server: 
    Server-->> ASR: Audio
    Server-->> ASR: 
    ASR --x Server: EOU
    ASR ->> LLM: Transcript
    LLM-->> TTS: Text
    LLM-->> TTS: 
    TTS-->> Server: Audio
    TTS-->> Server: 
    Server-->> Client: Audio
    Server-->> Client: 

```

### v3

- Streaming input and output to/from the bot
- Streaming input to ASR and endpointing (~EOU detection)

  > - **Optimised endpointing : partial transcripts are streamed to LLM**
- Streaming output from LLM 
- Streaming input and output to/from TTS

```mermaid
sequenceDiagram
    Client-->> Server: Audio
    Client-->> Server: 
    Client-->> Server: 
    Server-->> ASR: Audio
    ASR --x Server: EOU
    ASR ->> LLM: Partial Transcript
    LLM-->> TTS: Text
    LLM-->> TTS: 
    TTS-->> Server: Audio
    TTS-->> Server: 
    Server-->> Client: Audio
    Server-->> Client: 

```
