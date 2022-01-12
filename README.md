# AsyncForward

****
```python
"""
基于asyncio的异步端口转发
"""
from AsyncForward import run

run("127.0.0.1:9000", "127.0.0.1:5000", "DEBUG")
```