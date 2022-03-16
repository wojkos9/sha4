#!/bin/env python3
from hashlib import sha3_256

msg = "hello 👋 👁️ 👄👁️"
msg = ""
data = msg.encode('utf-8')

hash = sha3_256(data)

print(hash.digest().hex())