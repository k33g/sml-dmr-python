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

# Agentic Compose

> Effortless configuration of AI models in containerized applications

- Models definition in the Compose file
- Work with Docker Model Runner
- Attachment of one or more models to a service

---
# How to define models

- You can define a list of models
- Model definition:
  - name
  - model: OCI artifact name of your model
  - Context size: maximum token context size for the model
  - Runtime flags: flags passed to the inference runtime such as temperature, verbose mode...

---
# Attach models to services

- `model` attribute of the service definition
- `model_var`, `endpoint_var`: customized environment variables

> By default, Compose send variables with names `[SERVICE]_MODEL` & `[SERVICE]_URL` to containers
