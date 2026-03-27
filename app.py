import streamlit as st
import pandas as pd
import unicodedata
import re
import base64
import io
import smtplib
import socket
import dns.resolver

st.set_page_config(
    page_title="Email Predictor — RealAdvisors",
    page_icon="📧",
    layout="centered",
)

_D = "bmV0d29yaztuYl9lbWFpbHNfY2xhc3Nlcztlc3RpbWF0aW9uXzFfY2xlO2VzdGltYXRpb25fMV9tb3RpZjtlc3RpbWF0aW9uXzFfcHJvYmFfcGN0O2VzdGltYXRpb25fMl9jbGU7ZXN0aW1hdGlvbl8yX21vdGlmO2VzdGltYXRpb25fMl9wcm9iYV9wY3Q7ZXN0aW1hdGlvbl8zX2NsZTtlc3RpbWF0aW9uXzNfbW90aWY7ZXN0aW1hdGlvbl8zX3Byb2JhX3BjdDtlc3RpbWF0aW9uXzRfY2xlO2VzdGltYXRpb25fNF9tb3RpZjtlc3RpbWF0aW9uXzRfcHJvYmFfcGN0O2VzdGltYXRpb25fNV9jbGU7ZXN0aW1hdGlvbl81X21vdGlmO2VzdGltYXRpb25fNV9wcm9iYV9wY3Q7ZG9tYWluZV8xO2RvbWFpbmVfMV9wcm9iYV9wY3Q7ZG9tYWluZV8yO2RvbWFpbmVfMl9wcm9iYV9wY3Q7ZG9tYWluZV8zO2RvbWFpbmVfM19wcm9iYV9wY3QNCklhZDs0Nzk3NDtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzg5LjA7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzguOTtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzEuMjtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzAuMztpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7MC4xO2lhZGZyYW5jZS5mcjs5NC44O2dtYWlsLmNvbTsyLjA7YnNraW1tb2JpbGllci5jb207MC45DQpTYWZ0aTsyMTQyNztwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzc3LjI7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzE2LjA7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxLjk7cHJlbm9tX25vbV9jb25jYXQ7cHLDqW5vbStub20gY29sbMOpczsxLjU7YWRyZXNzZV9nZW5lcmlxdWU7Y29udGFjdEAgLyBpbmZvQDsxLjI7c2FmdGkuZnI7NzguNDtnbWFpbC5jb207Ni44O2NhcGlmcmFuY2UuZnI7MS4wDQpQcm9wcmnDqXTDqXMgcHJpdsOpZXM7MTA4MzM7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTs3OC42O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsxNS40O2RldXhfaW5pdGlhbGVzX25vbTsyIGluaXRpYWxlcy5ub207My43O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MS4zO3ByZW5vbV9ub21fY29uY2F0O3Byw6lub20rbm9tIGNvbGzDqXM7MC40O3Byb3ByaWV0ZXMtcHJpdmVlcy5jb207OTUuNTtnbWFpbC5jb207MS44O29yYW5nZS5mcjswLjQNCkVmZmljaXR5OzgzOTE7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzgwLjI7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzE0Ljk7cHJlbm9tX25vbV9jb25jYXQ7cHLDqW5vbStub20gY29sbMOpczszLjE7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxLjE7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTswLjU7ZWZmaWNpdHkuY29tOzkzLjY7Z21haWwuY29tOzMuMDt5YWhvby5mcjswLjQNCkNhcGlGcmFuY2U7Nzk4NTtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzg1Ljc7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzExLjk7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxLjA7cHJlbm9tX25vbV9jb25jYXQ7cHLDqW5vbStub20gY29sbMOpczswLjg7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzAuMjtjYXBpZnJhbmNlLmZyOzkxLjM7Z21haWwuY29tOzMuMTt5YWhvby5mcjswLjYNCktlbGxlciBXaWxsaWFtczs2MzA1O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NzguMzthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTUuMztpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzIuMTtpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7MS41O3ByZW5vbV9ub21fY29uY2F0O3Byw6lub20rbm9tIGNvbGzDqXM7MS4xO2t3ZnJhbmNlLmNvbTs3OC40O2dtYWlsLmNvbTs3LjY7Y2VzYXJldGJydXR1cy5jb207Mi4yDQpCc2sgaW1tb2JpbGllcjs0NzEwO2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207NDIuMjtpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7MzMuNjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTcuNjtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzQuMjtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzEuNDtic2tpbW1vYmlsaWVyLmNvbTs4Ni43O2dtYWlsLmNvbTs2LjM7aWFkZnJhbmNlLmZyOzEuMw0KT3B0aW1ob21lOzQ2OTA7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs1OC43O3ByZW5vbV90aXJldF9ub207cHLDqW5vbS1ub207MjUuMTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTQuODtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzAuNjtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzAuMztvcHRpbWhvbWUuY29tOzkyLjU7Z21haWwuY29tOzMuNztvcmFuZ2UuZnI7MC43DQpNZWdhZ2VuY2U7NDE1MDtwcmVub21fdGlyZXRfbm9tO3Byw6lub20tbm9tOzQ1LjI7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs0MS4yO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsxMS41O3ByZW5vbV9ub21fY29uY2F0O3Byw6lub20rbm9tIGNvbGzDqXM7MS4wO2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207MC43O21lZ2FnZW5jZS5jb207OTAuODtnbWFpbC5jb207NS4xO2hvdG1haWwuZnI7MC41DQpBdXRyZTsyMjU0O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTszOS44O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MzAuNDtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzEzLjU7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzYuNztwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzQuOTtnbWFpbC5jb207MzAuMDtic2tpbW1vYmlsaWVyLmNvbTs4LjE7aWFkZnJhbmNlLmZyOzYuNw0KTGVzIFBvcnRlcyBDbMOpczsxODU4O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NjguNDthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTMuMDthZHJlc3NlX2dlbmVyaXF1ZTtjb250YWN0QCAvIGluZm9AOzYuODtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzQuMztwcmVub21fc2V1bDtwcsOpbm9tIHNldWw7My4yO2ltbW9iaWxpZXIuZW1haWw7NzUuOTtnbWFpbC5jb207Ni4yO21hYXAtaW1tb2JpbGllci5mcjsxLjANCkxhIEZvdXJtaTsxNzk4O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207ODQuOTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTMuODtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzAuNztpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzAuMztwcmVub21fc2V1bDtwcsOpbm9tIHNldWw7MC4yO2xhZm91cm1pLWltbW8uY29tOzgyLjk7bGZpbW1vLmZyOzguNjtnbWFpbC5jb207My43DQozRyBJbW1vOzE3MTg7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs1NC45O2luaXRpYWxlX3BsdXNfbm9tO2luaXRpYWxlTm9tIChzYW5zIHPDqXBhcmF0ZXVyKTszMi42O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs5Ljk7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxLjQ7bm9tX3NldWw7bm9tIHNldWw7MC4zOzNnaW1tb2JpbGllci5jb207OTUuMjtnbWFpbC5jb207Mi4yO2pjLWltbW9iaWxpZXIuZnI7MC4zDQpFeHAgRnJhbmNlOzE2MDc7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs4MS41O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsxMy42O3ByZW5vbV9zZXVsO3Byw6lub20gc2V1bDsyLjc7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTswLjY7cHJlbm9tX25vbV9jb25jYXQ7cHLDqW5vbStub20gY29sbMOpczswLjU7ZXhwZnJhbmNlLmZyOzg3Ljc7bHV4dXJ5YnlibHVlLmNvbTs0Ljc7Z21haWwuY29tOzQuMA0KSWthbWk7ODQyO2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207ODcuMTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTEuODthZHJlc3NlX2dlbmVyaXF1ZTtjb250YWN0QCAvIGluZm9AOzAuNTtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzAuNDtkZXV4X2luaXRpYWxlc19ub207MiBpbml0aWFsZXMubm9tOzAuNDtpa2FtaS5mcjs5Ni4wO2dtYWlsLmNvbTsyLjQ7b3JwaS5jb207MC40DQpFeHBlcnRpbW87MTk0O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs2Mi45O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTQuOTthZHJlc3NlX2dlbmVyaXF1ZTtjb250YWN0QCAvIGluZm9AOzkuMztwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzYuNztwcmVub21fc2V1bDtwcsOpbm9tIHNldWw7NC42O2dtYWlsLmNvbTs1MC4wO2V4cGVydGltby5jb207MTkuNjtvdXRsb29rLmZyOzMuNg0KRHIgSG91c2UgSW1tbzsxNTE7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTszOS4xO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MjUuODthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MjUuMjtwcmVub21fc2V1bDtwcsOpbm9tIHNldWw7NC4wO3ByZW5vbV91bmRlcnNjb3JlX25vbTtwcsOpbm9tX25vbTsyLjA7ZHJob3VzZS1pbW1vLmNvbTs0NC40O2RyaG91c2UuaW1tbzsyMC41O2dtYWlsLmNvbTsxMS4zDQpEYW5zIHVuZSBhZ2VuY2U7MTM3O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs1MC40O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MjEuOTtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzguMDtpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7OC4wO3ByZW5vbV9zZXVsO3Byw6lub20gc2V1bDs3LjM7Z21haWwuY29tOzMzLjY7aG90bWFpbC5mcjs0LjQ7YWdlbmNlbmljYXJkLmZyOzIuOQ0KTGxveWQgJiBEYXZpczsxMDA7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs1Ny4wO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs0MC4wO2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207My4wOzs7Ozs7O2xsb3lkLWRhdmlzLmNvbTs5MS4wO2dtYWlsLmNvbTs5LjA7Ow0KTGliZXJrZXlzOzk0O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NzguNzthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MjEuMzs7Ozs7Ozs7OztsaWJlcmtleXMuY29tOzkzLjY7Z21haWwuY29tOzUuMztjYXBpZnJhbmNlLmZyOzEuMQ0KQWJyaWN1bHRldXJzOzkxO3ByZW5vbV9zZXVsO3Byw6lub20gc2V1bDs1Ny4xO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs0Mi45Ozs7Ozs7Ozs7O2FicmljdWx0ZXVycy5jb207OTUuNjtnbWFpbC5jb207My4zO2xlc2FicmljdWx0ZXVycy5jb207MS4xDQpXZWVsb2RnZTs4Nztpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7NTguNjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MjMuMDtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzQuNjthZHJlc3NlX2dlbmVyaXF1ZTtjb250YWN0QCAvIGluZm9AOzMuNDtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzMuNDt3ZS1sb2dlLmNvbTs3NS45O3dlZWxvZGdlLmZyOzguMDtnbWFpbC5jb207NC42DQpNZWlsbGV1cnNCaWVuczs4Njtpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7NDYuNTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MzkuNTtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzcuMDtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzMuNTtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzMuNTttZWlsbGV1cnNiaWVucy5jb207NjAuNTtnbWFpbC5jb207MzIuNjtob3RtYWlsLmZyOzMuNQ0KTm9vdmltbzs3NDtpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7NzQuMzthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTIuMjtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzUuNDtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzQuMTtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzQuMTtub292aW1vLmZyOzkwLjU7ZHJob3VzZS5pbW1vOzUuNDtnbWFpbC5jb207NC4xDQpDZW50dXJ5IDIxOzY4O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs1MS41O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MzkuNztwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzguODs7Ozs7OztjZW50dXJ5MjEuZnI7NTQuNDtnbWFpbC5jb207MjkuNDtsaXZlLmZyOzQuNA0KRW5kaWUgRnJhbmNlOzY0O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NjUuNjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MzQuNDs7Ozs7Ozs7OztlbmRpZS5mcjs3MC4zO2dtYWlsLmNvbTsxOC44O291dGxvb2suZnI7NC43DQpXZSBJbnZlc3QgRnJhbmNlOzYzO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207OTAuNTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7OS41Ozs7Ozs7Ozs7O3dlaW52ZXN0LmZyOzk1LjI7aWFkZnJhbmNlLmZyOzQuODs7DQpJbW1vRm9yZmFpdDs2MDtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzg1LjA7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzE1LjA7Ozs7Ozs7Ozs7aW1tb2ZvcmZhaXQuZnI7OTUuMDtvcmFuZ2UuZnI7NS4wOzsNCkJMIEFnZW50cyBJbW1vYmlsaWVyczs1MTtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzY2Ljc7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzE1Ljc7cHJlbm9tX25vbV9jb25jYXQ7cHLDqW5vbStub20gY29sbMOpczsxMS44O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NS45Ozs7O2JsLWFnZW50cy5mcjs3OC40O2dtYWlsLmNvbTsxMS44O3dlaW52ZXN0LmZyOzUuOQ0KUmVtYXg7NTE7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs4Mi40O2luaXRpYWxlX3BsdXNfbm9tO2luaXRpYWxlTm9tIChzYW5zIHPDqXBhcmF0ZXVyKTs5Ljg7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzcuODs7Ozs7OztyZW1heC5mcjs3OC40O2dtYWlsLmNvbTsxMS44O2ltbW9mcm9udGllcmUuY29tOzkuOA0KS2V5bWV4OzUxO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NzYuNTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MjEuNjtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzIuMDs7Ozs7OztrZXltZXguZnI7NjYuNztrZXltZXhpbW1vLmZyOzE5LjY7Z21haWwuY29tOzUuOQ0KQXhvOzQ5O2luaXRpYWxlX3BsdXNfbm9tO2luaXRpYWxlTm9tIChzYW5zIHPDqXBhcmF0ZXVyKTs2My4zO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsyOC42O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207OC4yOzs7Ozs7O2F4by5pbW1vOzQwLjg7YXhvLWFjdGlmcy5mcjsyNi41O2dtYWlsLmNvbTsxMi4yDQpJbW1vIFJlc2VhdTs0Nztpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzcwLjI7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzE3LjA7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxMi44Ozs7Ozs7O2ltbW8tcmVzZWF1LmNvbTs3Mi4zO2lhZGZyYW5jZS5mcjs2LjQ7Z21haWwuY29tOzYuNA0KQ2FzYXZvOzQ2O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207ODQuODthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTUuMjs7Ozs7Ozs7OztjYXNhdm8uY29tOzczLjk7cHJvcHJpb28uZnI7MTMuMDtnbWFpbC5jb207Ni41DQpTZXh0YW50OzM2O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207ODguOTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTEuMTs7Ozs7Ozs7OztzZXh0YW50ZnJhbmNlLmZyOzgwLjY7aG90bWFpbC5jb207OC4zO3NleHRhbnQuZnI7OC4zDQpMR00gSW1tb2JpbGllcjsyOTtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzU1LjI7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzI0LjE7cHJlbm9tX3NldWw7cHLDqW5vbSBzZXVsOzEwLjM7cHJlbm9tX25vbV9jb25jYXQ7cHLDqW5vbStub20gY29sbMOpczsxMC4zOzs7O2xnbS1pbW1vYmlsaWVyLmZyOzU1LjI7Z21haWwuY29tOzM0LjU7YXVyb3JhaG9ydGkuZnI7MTAuMw0KSW1tb3Jlc2VhdTsyNTtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzcyLjA7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzI4LjA7Ozs7Ozs7Ozs7aW1tby1yZXNlYXUuY29tOzg0LjA7aG90bWFpbC5mcjsxNi4wOzsNCk9ycGk7MjE7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzI4LjY7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzI4LjY7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsyOC42O2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207MTQuMzs7OztvcnBpLmNvbTs3MS40O29yYW5nZS5mcjsxNC4zO2dtYWlsLmNvbTsxNC4zDQpFY290cmFuc2FjOzIwO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTAwLjA7Ozs7Ozs7Ozs7Ozs7ZWNvdHJhbnNhYy5mcjsxMDAuMDs7OzsNCkxhZm9yw6p0OzIwO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs3NS4wO2luaXRpYWxlX3BsdXNfbm9tO2luaXRpYWxlTm9tIChzYW5zIHPDqXBhcmF0ZXVyKTsyMC4wO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NS4wOzs7Ozs7O2xhZm9yZXQuY29tOzgwLjA7Y2VnZXRlbC5uZXQ7MTUuMDtpYWRmcmFuY2UuZnI7NS4wDQpXZSBJbnZlc3Q7MjA7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs2MC4wO2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207MjAuMDtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzE1LjA7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzUuMDs7Ozt3ZWludmVzdC5mcjs0NS4wO2JsLWFnZW50cy5mcjsyMC4wO2lhZGZyYW5jZS5mcjsxNS4wDQpBZ2VudE1hbmRhdGFpcmUuZnI7MTk7cHJlbm9tX25vbV9jb25jYXQ7cHLDqW5vbStub20gY29sbMOpczs2OC40O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsxNS44O2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7MTUuODs7Ozs7OzthZ2VudG1hbmRhdGFpcmUuZnI7ODQuMjtnbWFpbC5jb207MTUuODs7DQpZb3VsaXZlIGltbW9iaWxpZXI7MTk7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs2My4yO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTszNi44Ozs7Ozs7Ozs7O3lvdWxpdmUtaW1tb2JpbGllci5mcjs2My4yO2NhcGlmcmFuY2UuZnI7MTUuODtvdXRsb29rLmZyOzE1LjgNCkVyYTsxNztwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzEwMC4wOzs7Ozs7Ozs7Ozs7O2VyYWltbW8uZnI7MTAwLjA7Ozs7DQpSw6lzZWF1IEhCOzE2O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NDMuODthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MzcuNTtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzE4Ljg7Ozs7Ozs7Z21haWwuY29tOzU2LjI7cmVzZWF1aGIuZnI7NDMuODs7DQpDMmk7MTU7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzYwLjA7bm9tX3NldWw7bm9tIHNldWw7MjAuMDtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzIwLjA7Ozs7Ozs7c2ZyLmZyOzIwLjA7eWFob28uZnI7MjAuMDtncm91cGUtYzJpLmNvbTsyMC4wDQpTd2l4aW07MTQ7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzUwLjA7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTs1MC4wOzs7Ozs7Ozs7O2dtYWlsLmNvbTs1MC4wO3N3aXhpbS5jb207NTAuMDs7DQpOZXN0ZW5uOzEzO2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207OTIuMzthZHJlc3NlX2dlbmVyaXF1ZTtjb250YWN0QCAvIGluZm9AOzcuNzs7Ozs7Ozs7OztuZXN0ZW5uLmNvbTsxMDAuMDs7OzsNCkxlZGlsIGltbW87MTI7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxMDAuMDs7Ozs7Ozs7Ozs7OztsZWRpbC5pbW1vOzc1LjA7Z21haWwuY29tOzI1LjA7Ow0KVGVhbWZpOzEyO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NzUuMDthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MjUuMDs7Ozs7Ozs7Ozt0ZWFtZmkuZnI7NzUuMDtnbWFpbC5jb207MjUuMDs7DQpTdMOpcGhhbmUgUGxhemEgSW1tbzsxMjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7NTAuMDtpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7NTAuMDs7Ozs7Ozs7OztzdGVwaGFuZXBsYXphaW1tb2JpbGllci5jb207NzUuMDtnbWFpbC5jb207MjUuMDs7DQpUb3dlciBpbW1vYmlsaWVyOzEyO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NzUuMDthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MjUuMDs7Ozs7Ozs7OztnbWFpbC5jb207NzUuMDt0b3dlci1pbW1vYmlsaWVyLmZyOzI1LjA7Ow0KVGhlIERvb3IgTWFuOzEyO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTAwLjA7Ozs7Ozs7Ozs7Ozs7dGRtLmltbW87MTAwLjA7Ozs7DQpJbW9jb25zZWlsOzEwO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs0MC4wO2RldXhfaW5pdGlhbGVzX25vbTsyIGluaXRpYWxlcy5ub207MzAuMDtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzMwLjA7Ozs7Ozs7aW1vY29uc2VpbC5jb207NjAuMDtmcmllbmRseS1pbW1vLmZyOzMwLjA7Z21haWwuY29tOzEwLjANCkZvbmNpYTsxMDtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzcwLjA7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzMwLjA7Ozs7Ozs7Ozs7Z21haWwuY29tOzYwLjA7Zm9uY2lhLmNvbTs0MC4wOzsNCkJvbmFwYXJ0ZTs5O2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207MTAwLjA7Ozs7Ozs7Ozs7Ozs7Ym9uYXBhcnRlLWFydGRldml2cmUuY29tOzEwMC4wOzs7Ow0KV2lua2V5Ozk7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTs2Ni43O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MzMuMzs7Ozs7Ozs7Ozt3aW5rZXkuZnI7NjYuNztnbWFpbC5jb207MzMuMzs7DQpBZ2VuY2UgaW1tbzs5O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MzMuMztpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzMzLjM7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzMzLjM7Ozs7Ozs7aWNsb3VkLmNvbTszMy4zO2FnZW5jZS5pbW1vOzMzLjM7Z21haWwuY29tOzMzLjMNCk5lb3MtSW1tbzs4O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NzUuMDthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MjUuMDs7Ozs7Ozs7OztuZW9zLWltbW8uY29tOzYyLjU7Z21haWwuY29tOzI1LjA7aG90bWFpbC5jb207MTIuNQ0KQWtvbWk7NjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7NTAuMDtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzUwLjA7Ozs7Ozs7Ozs7YWtvbWkuZnI7NTAuMDtnbWFpbC5jb207NTAuMDs7DQpDYXNhZGljaTs2O2luaXRpYWxlX3BsdXNfbm9tO2luaXRpYWxlTm9tIChzYW5zIHPDqXBhcmF0ZXVyKTs1MC4wO2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7NTAuMDs7Ozs7Ozs7OztjYXNhZGljaS5mcjs1MC4wO2NocmlzdGlhbmVzc2UuZnI7NTAuMDs7DQpTb2xpZCBJbW1vOzY7cHJlbm9tX25vbV9jb25jYXQ7cHLDqW5vbStub20gY29sbMOpczs1MC4wO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NTAuMDs7Ozs7Ozs7Oztzb2xpZC1pbW1vLmNvbTsxMDAuMDs7OzsNCkdsb2JhbCBJbW1vYmlsaWVyOzY7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzUwLjA7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs1MC4wOzs7Ozs7Ozs7O2dtYWlsLmNvbTs1MC4wO2ZyZWUuZnI7NTAuMDs7DQpQaWV0cmFwb2xpczs2O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs1MC4wO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NTAuMDs7Ozs7Ozs7OztwaWV0cmFwb2xpcy5mcjs1MC4wO2dtYWlsLmNvbTs1MC4wOzsNCk5hb3MgSW1tb2JpbGllcjs2O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTAwLjA7Ozs7Ozs7Ozs7Ozs7bmFvc2ltbW9iaWxpZXIuY29tOzUwLjA7Z21haWwuY29tOzUwLjA7Ow0KTCdhZ2VudCBpbW1vYmlsaWVyOzY7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzUwLjA7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs1MC4wOzs7Ozs7Ozs7O2dtYWlsLmNvbTsxMDAuMDs7OzsNCkZyYW5jZSBQcm9wcmlvOzY7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzUwLjA7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzUwLjA7Ozs7Ozs7Ozs7ZnJhbmNlcHJvcHJpby5jb207MTAwLjA7Ozs7DQpJbW1vam95OzY7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzEwMC4wOzs7Ozs7Ozs7Ozs7O2dtYWlsLmNvbTs1MC4wO2ltbW9qb3kuY29tOzUwLjA7Ow0KSHVtYW47NjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTAwLjA7Ozs7Ozs7Ozs7Ozs7aG90bWFpbC5jb207NTAuMDtob3RtYWlsLmZyOzUwLjA7Ow0KTGlsaWhvbWU7NjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7NTAuMDtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzUwLjA7Ozs7Ozs7Ozs7Y2FybWVuLWltbW9iaWxpZXIuY29tOzUwLjA7Z21haWwuY29tOzUwLjA7Ow0KTGVnZ2V0dCBJbW1vYmlsaWVyOzY7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxMDAuMDs7Ozs7Ozs7Ozs7OztsZWdnZXR0LmZyOzUwLjA7aG90bWFpbC5jb207NTAuMDs7DQpNYSBtYWlzb24gaWTDqWFsZTs2O2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207MTAwLjA7Ozs7Ozs7Ozs7Ozs7bWFtYWlzb25pZGVhbGUuaW1tbzs4My4zO2xhbWFpc29uaWRlYWxlLmltbW87MTYuNzs7DQpIb21raTs0O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NzUuMDthZHJlc3NlX2dlbmVyaXF1ZTtjb250YWN0QCAvIGluZm9AOzI1LjA7Ozs7Ozs7Ozs7aG9ta2ktaW1tb2JpbGllci5jb207NzUuMDtnbWFpbC5jb207MjUuMDs7DQpBViBUcmFuc2FjdGlvbnM7MztwcmVub21fc2V1bDtwcsOpbm9tIHNldWw7MTAwLjA7Ozs7Ozs7Ozs7Ozs7cHJlc3RpZ2VpbW1vYmlsaWVyLm5ldDsxMDAuMDs7OzsNCkNhcm1lbjszO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsxMDAuMDs7Ozs7Ozs7Ozs7Ozt5YWhvby5mcjsxMDAuMDs7OzsNCkNpZi1pbW1vOzM7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxMDAuMDs7Ozs7Ozs7Ozs7OztjaWYtaW1tby5jb207MTAwLjA7Ozs7DQpEb21pbmk7Mztpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7MTAwLjA7Ozs7Ozs7Ozs7Ozs7Z21haWwuY29tOzEwMC4wOzs7Ow0KQWR2aWNpbTszO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTAwLjA7Ozs7Ozs7Ozs7Ozs7YWR2aWNpbS5jb207MTAwLjA7Ozs7DQpBIGxhIGx1Y2FybmU7MzthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTAwLjA7Ozs7Ozs7Ozs7Ozs7Z21haWwuY29tOzEwMC4wOzs7Ow0KQUdJOTI7MzthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTAwLjA7Ozs7Ozs7Ozs7Ozs7b3V0bG9vay5mcjsxMDAuMDs7OzsNCkFsbG93YTszO3ByZW5vbV9ub21fY29uY2F0O3Byw6lub20rbm9tIGNvbGzDqXM7MTAwLjA7Ozs7Ozs7Ozs7Ozs7Z21haWwuY29tOzEwMC4wOzs7Ow0KRXRoaWtraW1tbzszO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTAwLjA7Ozs7Ozs7Ozs7Ozs7ZXRoaWtrLWltbW8uZnI7MTAwLjA7Ozs7DQpMZXMgcHJvZmVzc2lvbm5lbHMgZGUgbCdpbW1vYmlsaWVyOzM7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxMDAuMDs7Ozs7Ozs7Ozs7OztsZXMtcHJvZmVzc2lvbm5lbHMuaW1tbzsxMDAuMDs7OzsNCkwnQWRyZXNzZTszO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTAwLjA7Ozs7Ozs7Ozs7Ozs7bGFkcmVzc2UuY29tOzEwMC4wOzs7Ow0KTCdBcnQgMiBWZW5kcmU7MztwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzEwMC4wOzs7Ozs7Ozs7Ozs7O2xhcnQydmVuZHJlaW1tb2JpbGllci5jb207MTAwLjA7Ozs7DQpMJ2ltbW9iaWxpZXIgSHVtYWluOzM7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxMDAuMDs7Ozs7Ozs7Ozs7OztsaW1tb2JpbGllcmh1bWFpbi5jb207MTAwLjA7Ozs7DQpIVCZWZW5kcmUuY29tOzM7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxMDAuMDs7Ozs7Ozs7Ozs7OztodGV0dmVuZHJlLmNvbTsxMDAuMDs7OzsNCklta2l6OzM7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzEwMC4wOzs7Ozs7Ozs7Ozs7O2lta2l6LmNvbTsxMDAuMDs7OzsNCkltbW8gZGUgRnJhbmNlOzM7cHJlbm9tX3NldWw7cHLDqW5vbSBzZXVsOzEwMC4wOzs7Ozs7Ozs7Ozs7O2pjZ2ltbW8uY29tOzEwMC4wOzs7Ow0KTGlmZWhvbWU7MzthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTAwLjA7Ozs7Ozs7Ozs7Ozs7Z21haWwuY29tOzEwMC4wOzs7Ow0KT3rDqW8gSW1tbzszO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTAwLjA7Ozs7Ozs7Ozs7Ozs7bGl2ZS5mcjsxMDAuMDs7OzsNCk1laWxsZXVyIENvbnNlaWw7MztwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzEwMC4wOzs7Ozs7Ozs7Ozs7O2xpdmUuZnI7MTAwLjA7Ozs7DQpOb3RpYSBJbW1vYmlsaWVyOzM7YWRyZXNzZV9nZW5lcmlxdWU7Y29udGFjdEAgLyBpbmZvQDsxMDAuMDs7Ozs7Ozs7Ozs7Oztub3RpYWltbW9iaWxpZXIuZnI7MTAwLjA7Ozs7DQpQcm92aW1vOzM7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxMDAuMDs7Ozs7Ozs7Ozs7Oztwcm92aW1vLmZyOzEwMC4wOzs7Ow0KU21hcnQgUHJvcHJpbzszO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTAwLjA7Ozs7Ozs7Ozs7Ozs7c21hcnRwcm9wcmlvLmNvbTsxMDAuMDs7OzsNClN3ZXZlbiBJbW1vOzM7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxMDAuMDs7Ozs7Ozs7Ozs7Oztzd2V2ZW4taW1tby5mcjsxMDAuMDs7OzsNCldlIExvZ2U7MzthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTAwLjA7Ozs7Ozs7Ozs7Ozs7Z21haWwuY29tOzEwMC4wOzs7Ow0K"

# ── Data ──────────────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    raw = base64.b64decode(_D)
    df = pd.read_csv(io.BytesIO(raw), sep=";", dtype=str)
    for col in df.columns:
        if "proba_pct" in col:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    return df

# ── Email deliverability check ───────────────────────────────────────────────
# Architecture :
#   1. get_domain_type(domain)   → caché 30j par domaine
#        - MX lookup
#        - probe catchall (adresse fake)
#        → "no_mx" | "catchall" | "strict" | "blocked"
#   2. check_mailbox(email, mx)  → caché 24h par adresse (seulement si strict)
#        - RCPT TO sur l'adresse réelle
#        → "exists" | "rejected" | "inconclusive"

@st.cache_data(ttl=30 * 24 * 3600)   # 30 jours — 1 test par domaine par mois
def get_domain_type(domain: str) -> dict:
    """
    Vérifie le domaine une fois par mois.
    Retourne {"type": ..., "mx": ...}
    type : "no_mx" | "catchall" | "strict" | "blocked"
    """
    # 1. MX lookup
    try:
        records = dns.resolver.resolve(domain, "MX", lifetime=5)
        mx = str(sorted(records, key=lambda r: r.preference)[0].exchange).rstrip(".")
    except Exception:
        return {"type": "no_mx", "mx": None}

    # 2. Probe catchall avec adresse manifestement fausse
    try:
        with smtplib.SMTP(timeout=6) as smtp:
            smtp.connect(mx, 25)
            smtp.helo("verifier.local")
            smtp.mail("probe@verifier.local")
            fake = f"zzznobody99xyzxyz99@{domain}"
            code, _ = smtp.rcpt(fake)
            if code == 250:
                return {"type": "catchall", "mx": mx}
            else:
                return {"type": "strict", "mx": mx}
    except Exception:
        return {"type": "blocked", "mx": mx}


@st.cache_data(ttl=24 * 3600)   # 24h — cache par boite spécifique
def check_mailbox(email: str, mx: str) -> str:
    """
    RCPT TO sur l'adresse réelle (seulement pour domaines strict).
    Retourne "exists" | "rejected" | "inconclusive"
    """
    try:
        with smtplib.SMTP(timeout=6) as smtp:
            smtp.connect(mx, 25)
            smtp.helo("verifier.local")
            smtp.mail("probe@verifier.local")
            code, _ = smtp.rcpt(email)
            if code == 250:
                return "exists"
            elif code in (550, 551, 553):
                return "rejected"
            return "inconclusive"
    except Exception:
        return "inconclusive"


def verify_email(email: str) -> dict:
    """
    Pipeline complet :
      format → domaine (MX + catchall, caché 30j) → boite (SMTP, caché 24h si strict)
    """
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return {"status": "invalid_format", "label": "Format invalide", "icon": "🔴"}

    domain = email.split("@")[1]
    domain_info = get_domain_type(domain)
    dtype = domain_info["type"]
    mx    = domain_info["mx"]

    if dtype == "no_mx":
        return {"status": "no_mx",    "label": "Domaine inexistant (pas de MX)", "icon": "🔴"}

    if dtype == "catchall":
        return {"status": "catchall", "label": f"Catchall — domaine actif, boite non verifiable", "icon": "🟡"}

    if dtype == "blocked":
        return {"status": "blocked",  "label": f"Domaine actif — serveur bloque les verifications", "icon": "🟡"}

    # strict → on teste la boite
    result = check_mailbox(email, mx)
    if result == "exists":
        return {"status": "exists",   "label": "Boite mail existante", "icon": "🟢"}
    if result == "rejected":
        return {"status": "rejected", "label": "Boite mail inexistante", "icon": "🔴"}
    return {"status": "inconclusive", "label": "Serveur strict mais reponse ambigue", "icon": "🟡"}


# ── Name normalisation ────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Lowercase, remove accents, replace apostrophes with hyphen, strip other non-alphanum chars."""
    # remove accents
    nfkd = unicodedata.normalize("NFD", text)
    no_accent = "".join(c for c in nfkd if unicodedata.category(c) != "Mn")
    # lowercase
    s = no_accent.lower()
    # apostrophe → hyphen
    s = s.replace("'", "-").replace("'", "-")
    # keep only a-z 0-9 and hyphen
    s = re.sub(r"[^a-z0-9-]", "", s)
    # collapse multiple hyphens
    s = re.sub(r"-+", "-", s).strip("-")
    return s

# ── Email local-part generation ───────────────────────────────────────────────

MOTIF_LABELS = {
    "prenom_point_nom":      "prénom.nom",
    "initiale_point_nom":    "initiale.nom",
    "deux_initiales_nom":    "2initiales.nom",
    "initiale_plus_nom":     "initialeNom (sans séparateur)",
    "prenom_tiret_nom":      "prénom-nom",
    "prenom_nom_concat":     "prénom+nom collés",
    "prenom_underscore_nom": "prénom_nom",
    "nom_point_prenom":      "nom.prénom",
    "prenom_seul":           "prénom seul",
    "nom_seul":              "nom seul",
    "adresse_generique":     "contact@ / info@",
    "alias_pur":             "alias / perso (imprévisible)",
}

def generate_local(motif: str, prenom: str, nom: str) -> list[str]:
    p = normalize(prenom)
    n = normalize(nom)
    # strip hyphens for concat patterns only
    p_alpha = re.sub(r"-", "", p)
    n_alpha = re.sub(r"-", "", n)

    if motif == "prenom_point_nom":
        return [f"{p}.{n}"] if p and n else []
    if motif == "initiale_point_nom":
        return [f"{p[0]}.{n}"] if p and n else []
    if motif == "deux_initiales_nom":
        # try 2-char prefix (handles compound first names like Anne-Charlotte → ac)
        prefix = p_alpha[:2] if len(p_alpha) >= 2 else p_alpha
        return [f"{prefix}.{n}"] if prefix and n else []
    if motif == "initiale_plus_nom":
        return [f"{p[0]}{n_alpha}"] if p and n else []
    if motif == "prenom_tiret_nom":
        return [f"{p}-{n}"] if p and n else []
    if motif == "prenom_nom_concat":
        return [f"{p_alpha}{n_alpha}"] if p and n else []
    if motif == "prenom_underscore_nom":
        return [f"{p}_{n}"] if p and n else []
    if motif == "nom_point_prenom":
        return [f"{n}.{p}"] if p and n else []
    if motif == "prenom_seul":
        return [p] if p else []
    if motif == "nom_seul":
        return [n] if n else []
    if motif == "adresse_generique":
        return ["contact", "info"]
    return []  # alias_pur — imprévisible

# ── Which inputs are needed for a given set of motifs ─────────────────────────

_NEEDS_P = {"prenom_point_nom", "initiale_point_nom", "deux_initiales_nom",
            "initiale_plus_nom", "prenom_tiret_nom", "prenom_nom_concat",
            "prenom_underscore_nom", "nom_point_prenom", "prenom_seul"}
_NEEDS_N = {"prenom_point_nom", "initiale_point_nom", "deux_initiales_nom",
            "initiale_plus_nom", "prenom_tiret_nom", "prenom_nom_concat",
            "prenom_underscore_nom", "nom_point_prenom", "nom_seul"}

def needs_inputs(motifs: list[str]) -> tuple[bool, bool]:
    return any(m in _NEEDS_P for m in motifs), any(m in _NEEDS_N for m in motifs)

# ── UI ────────────────────────────────────────────────────────────────────────

st.title("📧 Email Predictor par Réseau")
st.caption("Génère les adresses email les plus probables d'un agent selon son réseau.")

df = load_data()
networks = df["network"].tolist()

col1, col2 = st.columns([2, 1])
with col1:
    selected_network = st.selectbox("Réseau immobilier", networks)
with col2:
    st.metric("Emails analysés", f"{int(df.loc[df['network'] == selected_network, 'nb_emails_classes'].values[0]):,}".replace(",", " "))

row = df[df["network"] == selected_network].iloc[0]

# Parse motifs and domains
motifs_data = []
for i in [1, 2, 3, 4, 5]:
    cle = row.get(f"estimation_{i}_cle", "")
    lib = row.get(f"estimation_{i}_motif", "")
    proba = float(row.get(f"estimation_{i}_proba_pct", 0.0) or 0.0)
    if pd.notna(cle) and cle and proba > 0:
        motifs_data.append({"cle": cle, "libelle": lib, "proba": proba})

domains_data = []
for i in [1, 2, 3]:
    dom = row.get(f"domaine_{i}", "")
    proba = float(row.get(f"domaine_{i}_proba_pct", 0.0) or 0.0)
    if pd.notna(dom) and dom and proba > 0:
        domains_data.append({"domain": dom, "proba": proba})

# Compute predictability score
autre_pct = sum(m["proba"] for m in motifs_data if m["cle"] == "alias_pur")
predictable_pct = 100.0 - autre_pct

# Predictability banner — shown immediately after network selection
if predictable_pct >= 60:
    st.success(
        f"✅ **Réseau bien structuré** — {predictable_pct:.0f}% des emails suivent un format standard prévisible. "
        f"La génération automatique sera fiable."
    )
elif predictable_pct >= 25:
    st.warning(
        f"⚠️ **Réseau partiellement prévisible** — seulement **{predictable_pct:.0f}%** des emails suivent un format standard. "
        f"Les **{autre_pct:.0f}%** restants sont des alias personnels ou adresses atypiques : "
        f"pour ces contacts, il faudra chercher l'email manuellement (LinkedIn, site web…)."
    )
else:
    st.error(
        f"🚫 **Réseau très peu prévisible** — **{autre_pct:.0f}%** des emails de ce réseau sont des alias personnels, "
        f"adresses perso (gmail, hotmail…) ou formats non-standards. "
        f"Seulement **{predictable_pct:.0f}%** suivent une logique prénom/nom. "
        f"La génération automatique sera très limitée — préférez une recherche manuelle."
    )

# Pattern detail expander
with st.expander("📊 Détail des patterns de ce réseau", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Format de l'adresse locale (partie avant @)**")
        for m in motifs_data:
            bar = int(m["proba"] / 5)
            if m["cle"] == "alias_pur":
                icon = "🔴"
                note = " *(imprévisible)*"
            else:
                icon = "🟢"
                note = ""
            st.markdown(
                f"{icon} `{m['libelle']}`{note} — **{m['proba']:.1f}%**  "
                f"{'▓' * bar}{'░' * (20 - bar)}"
            )
    with c2:
        st.markdown("**Domaine (partie après @)**")
        for d in domains_data:
            bar = int(d["proba"] / 5)
            st.markdown(f"`{d['domain']}` — **{d['proba']:.1f}%**  {'▓' * bar}{'░' * (20 - bar)}")

# Determine required inputs
motif_keys = [m["cle"] for m in motifs_data]
need_prenom, need_nom = needs_inputs(motif_keys)

st.divider()
st.subheader("Informations de l'agent")

input_col1, input_col2 = st.columns(2)
prenom, nom = "", ""

if need_prenom:
    with input_col1:
        prenom = st.text_input("Prénom", placeholder="ex. Marie")
if need_nom:
    with input_col2:
        nom = st.text_input("Nom", placeholder="ex. Dupont")

if not need_prenom and not need_nom:
    st.error(
        "🚫 Ce réseau utilise **uniquement** des alias personnels ou adresses non-standards. "
        "Aucune génération automatique n'est possible — il faut trouver l'email manuellement."
    )

# Generate button
st.divider()
generate = st.button("🔍 Générer les emails", type="primary", use_container_width=True)

if generate:
    if need_prenom and not prenom.strip():
        st.warning("Merci de saisir le prénom.")
        st.stop()
    if need_nom and not nom.strip():
        st.warning("Merci de saisir le nom.")
        st.stop()

    results = []
    unpredictable_proba = 0.0

    for motif in motifs_data:
        cle = motif["cle"]
        m_proba = motif["proba"]

        if cle == "alias_pur":
            unpredictable_proba += m_proba
            continue

        locals_list = generate_local(cle, prenom.strip(), nom.strip())
        if not locals_list:
            continue

        for local in locals_list:
            for dom in domains_data:
                # combined probability: motif_proba * domain_proba / 100
                combined = round(m_proba * dom["proba"] / 100, 1)
                results.append({
                    "Email": f"{local}@{dom['domain']}",
                    "Format": MOTIF_LABELS.get(cle, cle),
                    "Domaine": dom["domain"],
                    "Proba (%)": combined,
                })

    if not results:
        st.warning("Aucun email prédictible pour ce réseau avec ces informations.")
    else:
        results_df = (
            pd.DataFrame(results)
            .sort_values("Proba (%)", ascending=False)
            .drop_duplicates(subset=["Email"])
            .reset_index(drop=True)
        )
        results_df.index = results_df.index + 1

        st.subheader(f"Emails générés pour **{prenom.strip()} {nom.strip()}**")

        # Display with coloured probability
        for _, r in results_df.iterrows():
            pct = r["Proba (%)"]
            if pct >= 50:
                colour = "🟢"
            elif pct >= 15:
                colour = "🟡"
            else:
                colour = "🔴"

            col_a, col_b, col_c = st.columns([4, 2, 1])
            with col_a:
                st.code(r["Email"], language=None)
            with col_b:
                st.markdown(f"*{r['Format']}*")
            with col_c:
                st.markdown(f"{colour} **{pct:.1f}%**")

        if unpredictable_proba >= 70:
            st.error(
                f"🚫 **Attention** : {unpredictable_proba:.0f}% des agents de ce réseau n'utilisent **pas** "
                f"un format standard — les emails ci-dessus ne couvrent que les {100 - unpredictable_proba:.0f}% restants. "
                f"Pour la majorité des contacts de ce réseau, chercher l'email manuellement (LinkedIn, site réseau…)."
            )
        elif unpredictable_proba >= 25:
            st.warning(
                f"⚠️ **{unpredictable_proba:.0f}%** des agents de ce réseau utilisent un alias personnel "
                f"ou une adresse non-standard — ces cas ne sont pas couverts par les emails générés ci-dessus."
            )

        # Deliverability check
        st.divider()
        if st.button("Verifier la delivrabilite des emails generes", use_container_width=True):
            st.caption(
                "MX = le domaine a un serveur mail. "
                "SMTP = la boite existe (non fiable sur les serveurs catchall)."
            )
            for _, r in results_df.iterrows():
                result = verify_email(r["Email"])
                col_email_v, col_status = st.columns([4, 3])
                with col_email_v:
                    st.code(r["Email"], language=None)
                with col_status:
                    st.markdown(f"{result['icon']} {result['label']}")

        # CSV download
        st.download_button(
            label="⬇️ Télécharger en CSV",
            data=results_df.to_csv(index=False, sep=";").encode("utf-8-sig"),
            file_name=f"emails_{normalize(prenom)}_{normalize(nom)}_{selected_network.lower().replace(' ', '_')}.csv",
            mime="text/csv",
        )
