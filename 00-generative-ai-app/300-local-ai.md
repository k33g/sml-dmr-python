---
marp: true
theme: default
paginate: true
---
<style>
.dodgerblue {
  color: dodgerblue;
}
</style>
# Run LLMs locally

## **llama.cpp**
> [https://github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

- **Purpose**: C++ implementation for efficient LLM inference <span class="dodgerblue">**on local hardware**</span>
- **Performance**: Optimized for <span class="dodgerblue">**CPU/GPU**</span> with quantization techniques to reduce memory usage
- **Usage**: Low-level tool for running Llama and compatible models <span class="dodgerblue">**without cloud dependencies**</span>

---
# Other tools
#### User-friendly wrappers around llama.cpp with additional features: GUIs, CLI, REST <span class="dodgerblue">**APIs**</span>...
- GPT4All: https://www.nomic.ai/gpt4all
- 🦙 Ollama: https://ollama.com/
- 🐳 <span class="dodgerblue">**Docker Model Runner**</span>: https://docs.docker.com/ai/model-runner/
#### Frameworks, libaries to easily build your own applications
#### ✋ API -> OpenAI API compliant

---
# Models for local use (Advantages)
- **Privacy**: Data stays on your device
- **Control**: Full control over model usage and updates
- **Cost**: No ongoing API fees
- **Offline**: Works without internet connection

---
# Models for local use (Challenges)
- **Hardware**: Requires powerful local hardware (CPU/GPU) 🤔
- **Performance**: May be slower than cloud-based solutions
- **Model Size**: Limited to smaller models that fit local resources


