# AsyncForward
****
### 基于asyncio的异步端口转发

```shell
# 转发5000端口的流量到本地redis服务的6379端口
python3 run.py --local 127.0.0.1:5000 --remote 127.0.0.1:6379
```

### Docker
```shell
docker build ./ -t async_forward
docker run -it --name async-forward async_forward "--remote 172.17.0.1:6379"
```