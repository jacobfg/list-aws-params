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



http://pre.domain.com.au/_jitc/redirect?image=ghcr.io/jacobfg/list-aws-params:latest&path=secrets/
http://pre.domain.com.au/_jitc/redirect?image=ghcr.io/jacobfg/list-aws-params:latest&path=secrets/cdk-bootstrap


http://pre.domain.com.au/_jitc/redirect?image=docker.sandbox.nonprod.domain.com.au/billing-centre-web:latest&path=secrets/cdk-bootstrap




```bash
sudo bash
yum update
yum install -y docker
usermod -a -G docker ec2-user
newgrp docker
systemctl restart docker
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m) -o /usr/bin/docker-compose && chmod 755 /usr/bin/docker-compose && docker-compose --version
```
