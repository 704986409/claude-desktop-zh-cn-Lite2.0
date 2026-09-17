#!/usr/bin/env python3
import sys

from enhance_zh_cn import main

if __name__ == "__main__":
    sys.argv = [sys.argv[0], "--hardcoded-only", *sys.argv[1:]]
    raise SystemExit(main())
