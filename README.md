# AsyncForward
****
### 基于asyncio的异步端口转发

```shell
# 转发5000端口的流量到本地redis服务的6379端口
python3 run.py --local 127.0.0.1:5000 --remote 127.0.0.1:6379
```

### Docker
```shell
# 构建当前项目镜像
docker build ./ -t async_forward

# 将容器35000端口流量转发至同一docker网络下redis容器的6379端口
docker run -it --name async-forward -p 35000:5000 async_forward '172.17.0.1:6379'
```