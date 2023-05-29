# README.md

Build and run

```bash
export PLATFORM=linux/amd64,linux/arm64
export GITHUB_TOKEN=...
echo $GITHUB_TOKEN | docker login ghcr.io -u jacobfg --password-stdin
docker buildx build --progress=plain --platform $PLATFORM --push -t ghcr.io/jacobfg/list-aws-params:latest .
#--no-cache
docker-compose up
```

Test

```bash
curl http://localhost:8000/secrets/Production|jq .
```
