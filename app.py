import streamlit as st
import streamlit.components.v1 as components
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
    layout="wide",
)

_D = "77u/bmV0d29yaztuYl9lbWFpbHNfY2xhc3Nlcztlc3RpbWF0aW9uXzFfY2xlO2VzdGltYXRpb25fMV9tb3RpZjtlc3RpbWF0aW9uXzFfcHJvYmFfcGN0O2VzdGltYXRpb25fMl9jbGU7ZXN0aW1hdGlvbl8yX21vdGlmO2VzdGltYXRpb25fMl9wcm9iYV9wY3Q7ZG9tYWluZV8xO2RvbWFpbmVfMV9wcm9iYV9wY3Q7ZXN0aW1hdGlvbl8zX2NsZTtlc3RpbWF0aW9uXzNfbW90aWY7ZXN0aW1hdGlvbl8zX3Byb2JhX3BjdDtlc3RpbWF0aW9uXzRfY2xlO2VzdGltYXRpb25fNF9tb3RpZjtlc3RpbWF0aW9uXzRfcHJvYmFfcGN0O2VzdGltYXRpb25fNV9jbGU7ZXN0aW1hdGlvbl81X21vdGlmO2VzdGltYXRpb25fNV9wcm9iYV9wY3Q7ZG9tYWluZV8yO2RvbWFpbmVfMl9wcm9iYV9wY3Q7ZG9tYWluZV8zO2RvbWFpbmVfM19wcm9iYV9wY3QNCklhZDsxMjkxNDU7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs4Ny45O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs5Ljc7aWFkZnJhbmNlLmZyOzk0LjU7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxLjI7bm9tX3BvaW50X3ByZW5vbTtub20ucHLDqW5vbTswLjY7cHJlbm9tX25vbV9jb25jYXQ7cHLDqW5vbStub20gY29sbMOpczswLjI7Z21haWwuY29tOzIuMTtic2tpbW1vYmlsaWVyLmNvbTswLjkNClNhZnRpOzU4NzYyO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NzMuNzthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTguNTtzYWZ0aS5mcjs3Ni45O2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207Mi4xO2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7MS42O3ByZW5vbV9ub21fY29uY2F0O3Byw6lub20rbm9tIGNvbGzDqXM7MS4yO2dtYWlsLmNvbTs3LjA7Y2FwaWZyYW5jZS5mcjsxLjANCkF1dHJlOzMzNDAxO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs0Mi4zO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTcuODtnbWFpbC5jb207MTkuNDthZHJlc3NlX2dlbmVyaXF1ZTtjb250YWN0QCAvIGluZm9AOzExLjM7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTs5LjQ7cHJlbm9tX3NldWw7cHLDqW5vbSBzZXVsOzcuNDtvcmFuZ2UuZnI7My42O2Jza2ltbW9iaWxpZXIuY29tOzEuOQ0KUHJvcHJpw6l0w6lzIHByaXbDqWVzOzI5Mjc4O2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207NzcuNjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTYuNTtwcm9wcmlldGVzLXByaXZlZXMuY29tOzk1LjI7ZGV1eF9pbml0aWFsZXNfbm9tOzJpbml0aWFsZXMubm9tOzMuNjtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzEuMjtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzAuNDtnbWFpbC5jb207MS44O29yYW5nZS5mcjswLjQNCkVmZmljaXR5OzIyNzAxO2luaXRpYWxlX3BsdXNfbm9tO2luaXRpYWxlTm9tIChzYW5zIHPDqXBhcmF0ZXVyKTs3OS40O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsxNi4wO2VmZmljaXR5LmNvbTs5My4yO3ByZW5vbV9ub21fY29uY2F0O3Byw6lub20rbm9tIGNvbGzDqXM7Mi44O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MS4wO2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207MC41O2dtYWlsLmNvbTszLjE7b3JhbmdlLmZyOzAuNA0KQ2FwaUZyYW5jZTsyMTQ1MTtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzg0LjY7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzEzLjA7Y2FwaWZyYW5jZS5mcjs5MC45O2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207MS4wO3ByZW5vbV9ub21fY29uY2F0O3Byw6lub20rbm9tIGNvbGzDqXM7MC41O2luaXRpYWxlX3BsdXNfbm9tO2luaXRpYWxlTm9tIChzYW5zIHPDqXBhcmF0ZXVyKTswLjM7Z21haWwuY29tOzMuMjt5YWhvby5mcjswLjYNCktlbGxlciBXaWxsaWFtczsxNzQ2MTtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzc1LjA7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzE4LjE7a3dmcmFuY2UuY29tOzc2LjU7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsyLjI7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzEuNDtwcmVub21fc2V1bDtwcsOpbm9tIHNldWw7MS4xO2dtYWlsLmNvbTs3Ljk7Y2VzYXJldGJydXR1cy5jb207Mi4xDQpCc2sgaW1tb2JpbGllcjsxMjc3NTtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzQyLjA7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzMyLjg7YnNraW1tb2JpbGllci5jb207ODYuMjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTguODtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzMuOTtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzEuMTtnbWFpbC5jb207Ni40O2lhZGZyYW5jZS5mcjsxLjMNCk9wdGltaG9tZTsxMjY1NztwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzU3LjA7cHJlbm9tX3RpcmV0X25vbTtwcsOpbm9tLW5vbTsyNC42O29wdGltaG9tZS5jb207OTIuNDthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTcuMDtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzAuNTtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzAuMztnbWFpbC5jb207My43O29yYW5nZS5mcjswLjYNCk1lZ2FnZW5jZTsxMTE4NTtwcmVub21fdGlyZXRfbm9tO3Byw6lub20tbm9tOzQ0LjM7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs0MC40O21lZ2FnZW5jZS5jb207OTAuNDthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTMuMTtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzAuODtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzAuNztnbWFpbC5jb207NS4zO2hvdG1haWwuZnI7MC41DQpPcnBpOzY4MjY7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzcxLjA7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzEyLjE7b3JwaS5jb207OTIuNjtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzUuMztpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzMuNDtub21fc2V1bDtub20gc2V1bDsyLjM7Z21haWwuY29tOzIuNjt3YW5hZG9vLmZyOzAuNg0KTGVzIFBvcnRlcyBDbMOpczs0OTk4O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NjguMTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTIuNDtpbW1vYmlsaWVyLmVtYWlsOzc1Ljc7YWRyZXNzZV9nZW5lcmlxdWU7Y29udGFjdEAgLyBpbmZvQDs2Ljg7cHJlbm9tX3NldWw7cHLDqW5vbSBzZXVsOzQuMztpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzQuMjtnbWFpbC5jb207Ni4zO21hYXAtaW1tb2JpbGllci5mcjsxLjANCkxhIEZvdXJtaTs0ODU0O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207ODMuMDthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTUuNDtsYWZvdXJtaS1pbW1vLmNvbTs4MS4yO2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207MC42O3ByZW5vbV9ub21fY29uY2F0O3Byw6lub20rbm9tIGNvbGzDqXM7MC4zO2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7MC4zO2xmaW1tby5mcjs5LjA7Z21haWwuY29tOzQuNA0KM0cgSW1tbzs0NjA4O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NTMuOTtpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7MzIuNTszZ2ltbW9iaWxpZXIuY29tOzk1LjA7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzEwLjU7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxLjQ7bm9tX3BvaW50X3ByZW5vbTtub20ucHLDqW5vbTswLjU7Z21haWwuY29tOzIuMjtqYy1pbW1vYmlsaWVyLmZyOzAuMw0KRXhwIEZyYW5jZTs0Mzg5O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NzYuNzthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTcuODtleHBmcmFuY2UuZnI7ODcuNDtwcmVub21fc2V1bDtwcsOpbm9tIHNldWw7My4xO2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7MC43O2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207MC42O2x1eHVyeWJ5Ymx1ZS5jb207NC42O2dtYWlsLmNvbTs0LjINCkNlbnR1cnkgMjE7MjU2MTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7NTguNztwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzMwLjA7Y2VudHVyeTIxLmZyOzcxLjM7cHJlbm9tX25vbV9jb25jYXQ7cHLDqW5vbStub20gY29sbMOpczszLjA7bm9tX3BvaW50X3ByZW5vbTtub20ucHLDqW5vbTsyLjg7YWRyZXNzZV9nZW5lcmlxdWU7Y29udGFjdEAgLyBpbmZvQDsxLjk7Y2VudHVyeTIxZnJhbmNlLmZyOzEzLjA7Z21haWwuY29tOzcuNA0KSWthbWk7MjI2Nztpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzg2LjY7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzEyLjI7aWthbWkuZnI7OTUuNzthZHJlc3NlX2dlbmVyaXF1ZTtjb250YWN0QCAvIGluZm9AOzAuNTtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzAuNDtkZXV4X2luaXRpYWxlc19ub207MmluaXRpYWxlcy5ub207MC40O2dtYWlsLmNvbTsyLjM7b3JwaS5jb207MC40DQpMYWZvcsOqdDsyMDYwO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs0Ny41O2luaXRpYWxlX3BsdXNfbm9tO2luaXRpYWxlTm9tIChzYW5zIHPDqXBhcmF0ZXVyKTs0MC42O2xhZm9yZXQuY29tOzkwLjU7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTs1Ljk7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTszLjk7cHJlbm9tX3NldWw7cHLDqW5vbSBzZXVsOzAuOTtnbWFpbC5jb207NC4wO2hvdG1haWwuZnI7MC43DQpOZXN0ZW5uOzE5MTY7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzQ4LjY7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTs0NS4wO25lc3Rlbm4uY29tOzg5LjA7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs0LjE7cHJlbm9tX3NldWw7cHLDqW5vbSBzZXVsOzAuNztpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7MC42O2dtYWlsLmNvbTszLjc7c29sdmltby5jb207MC44DQpFcmE7MTgxMTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7NjAuMTtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzI4LjQ7ZXJhaW1tby5mcjszNy40O2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7Mi44O25vbV9wb2ludF9wcmVub207bm9tLnByw6lub207Mi4zO2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207Mi4xO2VyYWZyYW5jZS5jb207MjkuODtnbWFpbC5jb207MTEuNQ0KR3V5IEhvcXVldDsxNzUwO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs1OS41O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTkuMTtndXlob3F1ZXQuY29tOzc5LjQ7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxMy4yO25vbV9zZXVsO25vbSBzZXVsOzMuODthZHJlc3NlX2dlbmVyaXF1ZTtjb250YWN0QCAvIGluZm9AOzIuMztnbWFpbC5jb207Ni45O2d1eS1ob3F1ZXQuZnI7MS43DQpMJ0FkcmVzc2U7MTQxMzthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7NDQuODtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzQ0LjA7bGFkcmVzc2UuY29tOzYwLjI7YWRyZXNzZV9nZW5lcmlxdWU7Y29udGFjdEAgLyBpbmZvQDszLjk7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzMuOTtwcmVub21fc2V1bDtwcsOpbm9tIHNldWw7MS4xO2xhZHJlc3NlLmltbW87Ni45O2dtYWlsLmNvbTs2LjENClN0w6lwaGFuZSBQbGF6YSBJbW1vOzExNDU7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzUwLjU7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzQzLjg7c3RlcGhhbmVwbGF6YWltbW9iaWxpZXIuY29tOzgwLjc7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsyLjc7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxLjI7YWRyZXNzZV9nZW5lcmlxdWU7Y29udGFjdEAgLyBpbmZvQDswLjk7c2l4aWVtZWF2ZW51ZS5jb207NC45O2dtYWlsLmNvbTsyLjgNCkV4cGVydGltbzs1NTM7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzY1LjE7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxNC41O2dtYWlsLmNvbTs0OC42O2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7MTAuNTtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzMuMztwcmVub21fc2V1bDtwcsOpbm9tIHNldWw7Mi45O2V4cGVydGltby5jb207MjAuMztvdXRsb29rLmZyOzMuNg0KRGFucyB1bmUgYWdlbmNlOzQzMjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7NDcuNTtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzE3LjE7Z21haWwuY29tOzM1LjQ7cHJlbm9tX3NldWw7cHLDqW5vbSBzZXVsOzExLjg7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTs3LjQ7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzYuOTtob3RtYWlsLmZyOzMuNzthZ2VuY2VuaWNhcmQuZnI7Mi44DQpEciBIb3VzZSBJbW1vOzQyODtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzM4LjE7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzI1LjU7ZHJob3VzZS1pbW1vLmNvbTs0My4wO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MjQuNTtwcmVub21fc2V1bDtwcsOpbm9tIHNldWw7NC40O3ByZW5vbV91bmRlcnNjb3JlX25vbTtwcsOpbm9tX25vbTsxLjk7ZHJob3VzZS5pbW1vOzIyLjA7Z21haWwuY29tOzEwLjMNCldlIEludmVzdDszNTQ7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs1NC4yO25vbV9wb2ludF9wcmVub207bm9tLnByw6lub207MjYuNjt3ZWludmVzdC5mcjs4My42O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs5LjM7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTs2LjU7cHJlbm9tX3NldWw7cHLDqW5vbSBzZXVsOzEuNztibC1hZ2VudHMuZnI7My40O2dtYWlsLmNvbTsyLjUNCkF4bzszNTA7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzU4LjM7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzM4Ljk7YXhvLmltbW87MzkuNDtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzIuOTs7Ozs7OztheG8tYWN0aWZzLmZyOzM1LjQ7Z21haWwuY29tOzE2LjYNCkxsb3lkICYgRGF2aXM7Mjg3O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NTUuNDthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7NDEuODtsbG95ZC1kYXZpcy5jb207OTEuNjtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzIuODs7Ozs7OztnbWFpbC5jb207OC40OzsNCkxpYmVya2V5czsyNzY7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs3OS4wO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsyMS4wO2xpYmVya2V5cy5jb207OTQuMjs7Ozs7Ozs7OztnbWFpbC5jb207NC4zO2NhcGlmcmFuY2UuZnI7MS40DQpBYnJpY3VsdGV1cnM7MjYwO3ByZW5vbV9zZXVsO3Byw6lub20gc2V1bDs4MS41O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsxOC41O2FicmljdWx0ZXVycy5jb207OTUuNDs7Ozs7Ozs7OztnbWFpbC5jb207My4xO2xlc2FicmljdWx0ZXVycy5jb207MS41DQpNZWlsbGV1cnNCaWVuczsyNDk7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzQ1Ljg7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzQxLjQ7bWVpbGxldXJzYmllbnMuY29tOzU2LjI7bm9tX3BvaW50X3ByZW5vbTtub20ucHLDqW5vbTszLjI7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTszLjI7cHJlbm9tX25vbV9jb25jYXQ7cHLDqW5vbStub20gY29sbMOpczszLjI7Z21haWwuY29tOzM0LjE7aG90bWFpbC5mcjszLjINCldlZWxvZGdlOzIzMTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7ODIuMztpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7My45O3dlLWxvZ2UuY29tOzc3LjE7YWRyZXNzZV9nZW5lcmlxdWU7Y29udGFjdEAgLyBpbmZvQDszLjU7bm9tX3BvaW50X3ByZW5vbTtub20ucHLDqW5vbTszLjU7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTszLjU7d2VlbG9kZ2UuZnI7Ni45O2dtYWlsLmNvbTs0LjMNClJlbWF4OzIwOTtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzcyLjc7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzEzLjQ7cmVtYXguZnI7NzMuNztpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7Ny43O3ByZW5vbV9ub21fY29uY2F0O3Byw6lub20rbm9tIGNvbGzDqXM7Mi40O2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7Mi40O2dtYWlsLmNvbTsxMi40O2ltbW9mcm9udGllcmUuY29tOzcuNw0KTm9vdmltbzsyMDU7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzc0LjY7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzEyLjc7bm9vdmltby5mcjs5MS4yO2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207NC45O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207My45O3ByZW5vbV9ub21fY29uY2F0O3Byw6lub20rbm9tIGNvbGzDqXM7My45O2RyaG91c2UuaW1tbzs0Ljk7Z21haWwuY29tOzMuOQ0KVGVhbWZpOzE4NjtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzgxLjc7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzE4LjM7dGVhbWZpLmZyOzkxLjk7Ozs7Ozs7Ozs7Z21haWwuY29tOzguMTs7DQpLZXltZXg7MTgwO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NzcuODthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MjAuMDtrZXltZXguZnI7NzEuMTtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzIuMjs7Ozs7OztrZXltZXhpbW1vLmZyOzE3Ljg7Z21haWwuY29tOzQuNA0KRW5kaWUgRnJhbmNlOzE3ODtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzU1LjE7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzM2LjA7ZW5kaWUuZnI7NjkuNztub21fcG9pbnRfcHJlbm9tO25vbS5wcsOpbm9tOzkuMDs7Ozs7OztnbWFpbC5jb207MTkuMTtvdXRsb29rLmZyOzQuNQ0KV2UgSW52ZXN0IEZyYW5jZTsxNzY7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs5MC45O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs5LjE7d2VpbnZlc3QuZnI7OTMuODs7Ozs7Ozs7OztpYWRmcmFuY2UuZnI7NC41O25vdXZlbGxlLWRlbWV1cmUuY29tOzEuNw0KSW1tb0ZvcmZhaXQ7MTYwO2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207ODUuMDthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTUuMDtpbW1vZm9yZmFpdC5mcjs5NS4wOzs7Ozs7Ozs7O29yYW5nZS5mcjs1LjA7Ow0KUGlldHJhcG9saXM7MTU4O2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207NzcuMjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTcuNztwaWV0cmFwb2xpcy5mcjs5My4wO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NS4xOzs7Ozs7O2dtYWlsLmNvbTs1LjE7cGlldHJhb3BsaXMuZnI7MS45DQpCTCBBZ2VudHMgSW1tb2JpbGllcnM7MTUwO2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207NjMuMzthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MjAuNztibC1hZ2VudHMuZnI7NzguNztwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzguNztwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzcuMzs7OztnbWFpbC5jb207MTAuNzt3ZWludmVzdC5mcjs1LjMNClN3aXhpbTsxNDY7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTs1NC4xO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs0My44O3N3aXhpbS5jb207NzYuNztwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzIuMTs7Ozs7OztnbWFpbC5jb207MjEuMjt5YWhvby5mcjsyLjENCkltbW8gUmVzZWF1OzE0NTtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzY3LjY7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzIxLjQ7aW1tby1yZXNlYXUuY29tOzcwLjM7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxMS4wOzs7Ozs7O2dtYWlsLmNvbTs5LjA7aWFkZnJhbmNlLmZyOzYuOQ0KU2l4acOobWUgQXZlbnVlOzEzNztpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7ODYuMTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTEuNztzaXhpZW1lYXZlbnVlLmNvbTs3Ni42O2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207Mi4yOzs7Ozs7O3N0ZXBoYW5lcGxhemFpbW1vYmlsaWVyLmNvbTsxNy41O3NpeGllbWVhdmVudWVpbW1vYmlsaWVyLmNvbTszLjYNCkNhc2F2bzsxMjk7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs4NC41O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsxNS41O2Nhc2F2by5jb207NzUuMjs7Ozs7Ozs7Oztwcm9wcmlvby5mcjsxMi40O2dtYWlsLmNvbTs2LjINCkFydGh1cmltbW8uY29tOzEwNjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7NTEuOTtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzMxLjE7YWdlbmNlLWFydGh1cmltbW8uY29tOzI4LjM7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxMi4zO2luaXRpYWxlX3BsdXNfbm9tO2luaXRpYWxlTm9tIChzYW5zIHPDqXBhcmF0ZXVyKTs0Ljc7Ozs7Z21haWwuY29tOzI2LjQ7YXJ0aHVyaW1tby5jb207MTcuMA0KU2V4dGFudDs5ODtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzg3Ljg7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzEyLjI7c2V4dGFudGZyYW5jZS5mcjs4MS42Ozs7Ozs7Ozs7O2hvdG1haWwuY29tOzguMjtzZXh0YW50LmZyOzguMg0KTEdNIEltbW9iaWxpZXI7ODQ7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs1Ny4xO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTszMy4zO2xnbS1pbW1vYmlsaWVyLmZyOzU3LjE7cHJlbm9tX3NldWw7cHLDqW5vbSBzZXVsOzkuNTs7Ozs7OztnbWFpbC5jb207MzMuMzthdXJvcmFob3J0aS5mcjs5LjUNCkltbW9yZXNlYXU7NzY7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTs3Ni4zO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsyMy43O2ltbW8tcmVzZWF1LmNvbTs4Ni44Ozs7Ozs7Ozs7O2hvdG1haWwuZnI7MTMuMjs7DQpBZ2VudE1hbmRhdGFpcmUuZnI7NTc7cHJlbm9tX25vbV9jb25jYXQ7cHLDqW5vbStub20gY29sbMOpczs3MS45O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsxNC4wO2FnZW50bWFuZGF0YWlyZS5mcjs4Ni4wO2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7MTQuMDs7Ozs7OztnbWFpbC5jb207MTQuMDs7DQpFY290cmFuc2FjOzU2O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTAwLjA7Ozs7ZWNvdHJhbnNhYy5mcjsxMDAuMDs7Ozs7Ozs7Ozs7OzsNCkh1bWFuOzUyO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs3OC44O2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207MjEuMjtodW1hbi1pbW1vYmlsaWVyLmZyOzQyLjM7Ozs7Ozs7Ozs7aG90bWFpbC5mcjsyNS4wO2hvdG1haWwuY29tOzE1LjQNCllvdWxpdmUgaW1tb2JpbGllcjs1MDthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7NTIuMDtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzQ4LjA7eW91bGl2ZS1pbW1vYmlsaWVyLmZyOzY0LjA7Ozs7Ozs7Ozs7Y2FwaWZyYW5jZS5mcjsxNi4wO291dGxvb2suZnI7MTYuMA0KQWdlbmNlIGltbW87NDg7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzMzLjM7cHJlbm9tX3NldWw7cHLDqW5vbSBzZXVsOzMzLjM7Z21haWwuY29tOzI3LjE7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxNi43O2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207MTYuNzs7OztpY2xvdWQuY29tOzE2Ljc7YWdlbmNlLmltbW87MTYuNw0KUsOpc2VhdSBIQjs0ODtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzUyLjE7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzQxLjc7cmVzZWF1aGIuZnI7NTIuMTtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzYuMjs7Ozs7OztnbWFpbC5jb207NDcuOTs7DQpBcm1vciBjb25zZWlsIGltbW9iaWxpZXI7NDE7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTs3My4yO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTkuNTthcm1vci1jb25zZWlsLWltbW9iaWxpZXIuY29tOzg3Ljg7YWRyZXNzZV9nZW5lcmlxdWU7Y29udGFjdEAgLyBpbmZvQDs3LjM7Ozs7Ozs7Ymx1ZW9jdG9wdXMuZnI7MTIuMjs7DQpDw7R0w6kgUGFydGljdWxpZXJzOzQxO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs2NS45O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MjIuMDtjb3RlcGFydGljdWxpZXJzLmNvbTs0Ni4zO2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7MTIuMjs7Ozs7OztnbWFpbC5jb207MzQuMTtwcm9wYXJ0aWN1bGllcnMuZnI7MTIuMg0KQzJpOzQwO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs2MC4wO25vbV9zZXVsO25vbSBzZXVsOzIwLjA7c2ZyLmZyOzIwLjA7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsyMC4wOzs7Ozs7O3lhaG9vLmZyOzIwLjA7Z3JvdXBlLWMyaS5jb207MjAuMA0KTGVkaWwgaW1tbzszNztwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzEwMC4wOzs7O2xlZGlsLmltbW87NzguNDs7Ozs7Ozs7OztnbWFpbC5jb207MjEuNjs7DQpUaGUgRG9vciBNYW47Mzc7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs3OC40O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsyMS42O3RkbS5pbW1vOzEwMC4wOzs7Ozs7Ozs7Ozs7Ow0KVG93ZXIgaW1tb2JpbGllcjszNztwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzc4LjQ7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzIxLjY7Z21haWwuY29tOzY0Ljk7Ozs7Ozs7Ozs7dG93ZXItaW1tb2JpbGllci5mcjszNS4xOzsNCkJvbmFwYXJ0ZTszNDtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzg1LjM7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzE0Ljc7Ym9uYXBhcnRlLWFydGRldml2cmUuY29tOzg1LjM7Ozs7Ozs7Ozs7Z21haWwuY29tOzE0Ljc7Ow0KRm9uY2lhOzMzO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NjAuNjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MzkuNDtnbWFpbC5jb207NDguNTs7Ozs7Ozs7Oztmb25jaWEuY29tOzM2LjQ7aG90bWFpbC5mcjsxNS4yDQpGcmFuY2UgUHJvcHJpbzszMjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7NTYuMjtpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7MzQuNDtmcmFuY2Vwcm9wcmlvLmNvbTs2OC44O2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7OS40Ozs7Ozs7O3phZi1pbW1vYmlsaWVyLmNvbTszMS4yOzsNCkxlcyBBZ2VudHMgZGUgbCdJbW1vYmlsaWVyOzMwO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs4My4zO3ByZW5vbV9ub21fY29uY2F0O3Byw6lub20rbm9tIGNvbGzDqXM7MTYuNztnbWFpbC5jb207NDYuNzs7Ozs7Ozs7OztsZXNhZ2VudHNkZWxpbW1vYmlsaWVyLmNvbTs0My4zO21henppbW1vLmNvbTsxMC4wDQpEb21pdW0gR3JvdXBlOzI5O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NzIuNDthZHJlc3NlX2dlbmVyaXF1ZTtjb250YWN0QCAvIGluZm9AOzI3LjY7ZG9taXVtLWltbW9iaWxpZXIuY29tOzEwMC4wOzs7Ozs7Ozs7Ozs7Ow0KTmVvcy1JbW1vOzI4O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NTcuMTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7NDIuOTtuZW9zLWltbW8uY29tOzU3LjE7Ozs7Ozs7Ozs7Z21haWwuY29tOzI4LjY7aG90bWFpbC5jb207MTQuMw0KSW1vY29uc2VpbDsyNjtkZXV4X2luaXRpYWxlc19ub207MmluaXRpYWxlcy5ub207MzAuODtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzMwLjg7aW1vY29uc2VpbC5jb207NjEuNTtwcmVub21fc2V1bDtwcsOpbm9tIHNldWw7MzAuODthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7Ny43Ozs7O2ZyaWVuZGx5LWltbW8uZnI7MzAuODtnbWFpbC5jb207Ny43DQpMYSBCb3V0aXF1ZSBkdSBQYXRyaW1vaW5lOzI2O2luaXRpYWxlX3BsdXNfbm9tO2luaXRpYWxlTm9tIChzYW5zIHPDqXBhcmF0ZXVyKTs3Ni45O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsyMy4xO2xhYm91dGlxdWVkdXBhdHJpbW9pbmUuZnI7ODguNTs7Ozs7Ozs7Oztob3RtYWlsLmZyOzExLjU7Ow0KSW1tbyBkZSBGcmFuY2U7MjQ7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzQ1Ljg7cHJlbm9tX3NldWw7cHLDqW5vbSBzZXVsOzMzLjM7amNnaW1tby5jb207MzMuMztwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzIwLjg7Ozs7Ozs7aW1tb2RlZnJhbmNlLWNpZnYuZnI7MzMuMztpbW1vZnJhbmNlYWluLmNvbTsyMC44DQpDaXR5bGlmZTsyNDtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzc1LjA7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzI1LjA7Y2l0eWxpZmUuZnI7ODcuNTs7Ozs7Ozs7OztuZXVmLmZyOzEyLjU7Ow0KV2lua2V5OzI0O2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207NjYuNztwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzMzLjM7d2lua2V5LmZyOzY2Ljc7Ozs7Ozs7Ozs7Z21haWwuY29tOzMzLjM7Ow0KQ29sZHdlbGwgQmFua2VyOzIzO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NzguMzthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MjEuNztjb2xkd2VsbGJhbmtlci5mcjs3OC4zOzs7Ozs7Ozs7O2dtYWlsLmNvbTsyMS43OzsNClBpZXJyZSBEZSBMdW5lIEltbW9iaWxpZXI7MjM7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzg3LjA7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxMy4wO3BkbGkuZnI7ODcuMDs7Ozs7Ozs7OztvcmFuZ2UuZnI7MTMuMDs7DQpPcnp5IEltbW9iaWxpZXI7MjM7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTs3My45O2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7MTMuMDtvcnp5LmZyOzEwMC4wO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsxMy4wOzs7Ozs7Ozs7Ow0KTmFvcyBJbW1vYmlsaWVyOzIxO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NjEuOTtub21fcG9pbnRfcHJlbm9tO25vbS5wcsOpbm9tOzM4LjE7bmFvc2ltbW9iaWxpZXIuY29tOzYxLjk7Ozs7Ozs7Ozs7Z21haWwuY29tOzM4LjE7Ow0KTCdhZ2VudCBpbW1vYmlsaWVyOzIxO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTszOC4xO25vbV9wb2ludF9wcmVub207bm9tLnByw6lub207MzguMTtnbWFpbC5jb207NzYuMjtpbml0aWFsZV9wbHVzX25vbTtpbml0aWFsZU5vbSAoc2FucyBzw6lwYXJhdGV1cik7MjMuODs7Ozs7OztteWNhc2EtaW1tb2JpbGllci5jb207MjMuODs7DQpTb2xpZCBJbW1vOzIwO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NjAuMDtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzQwLjA7c29saWQtaW1tby5jb207MTAwLjA7Ozs7Ozs7Ozs7Ozs7DQpNYSBtYWlzb24gaWTDqWFsZTsyMDtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzEwMC4wOzs7O21hbWFpc29uaWRlYWxlLmltbW87ODAuMDs7Ozs7Ozs7OztsYW1haXNvbmlkZWFsZS5pbW1vOzIwLjA7Ow0KQWxiZXJ0IEltbW87MjA7YWRyZXNzZV9nZW5lcmlxdWU7Y29udGFjdEAgLyBpbmZvQDs1NS4wO3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MzAuMDthbGJlcnQtaW1tby5mcjs4NS4wO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsxNS4wOzs7Ozs7O2dtYWlsLmNvbTsxNS4wOzsNCkhvbWtpOzE5O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207NDIuMTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MzYuODtob21raS1pbW1vYmlsaWVyLmNvbTs3OC45O2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7MjEuMTs7Ozs7OztnbWFpbC5jb207MjEuMTs7DQpHbG9iYWwgSW1tb2JpbGllcjsxNjthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7NTAuMDtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzUwLjA7Z21haWwuY29tOzUwLjA7Ozs7Ozs7Ozs7ZnJlZS5mcjs1MC4wOzsNCkltbW9qb3k7MTY7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzEwMC4wOzs7O2dtYWlsLmNvbTs1MC4wOzs7Ozs7Ozs7O2ltbW9qb3kuY29tOzUwLjA7Ow0KQWtvbWk7MTY7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzUwLjA7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTs1MC4wO2Frb21pLmZyOzUwLjA7Ozs7Ozs7Ozs7Z21haWwuY29tOzUwLjA7Ow0KQ2FzYWRpY2k7MTY7aW5pdGlhbGVfcGx1c19ub207aW5pdGlhbGVOb20gKHNhbnMgc8OpcGFyYXRldXIpOzUwLjA7YWRyZXNzZV9nZW5lcmlxdWU7Y29udGFjdEAgLyBpbmZvQDs1MC4wO2Nhc2FkaWNpLmZyOzUwLjA7Ozs7Ozs7Ozs7Y2hyaXN0aWFuZXNzZS5mcjs1MC4wOzsNCkxpbGlob21lOzE2O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs1MC4wO3ByZW5vbV9ub21fY29uY2F0O3Byw6lub20rbm9tIGNvbGzDqXM7NTAuMDtjYXJtZW4taW1tb2JpbGllci5jb207NTAuMDs7Ozs7Ozs7OztnbWFpbC5jb207NTAuMDs7DQpMZWdnZXR0IEltbW9iaWxpZXI7MTY7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxMDAuMDs7OztsZWdnZXR0LmZyOzUwLjA7Ozs7Ozs7Ozs7aG90bWFpbC5jb207NTAuMDs7DQpDYWJpbmV0IFF1ZXNuZWU7MTQ7cHJlbm9tX3NldWw7cHLDqW5vbSBzZXVsOzc4LjY7YWRyZXNzZV9nZW5lcmlxdWU7Y29udGFjdEAgLyBpbmZvQDsyMS40O2NhYmluZXRxdWVzbmVlLmNvbTsxMDAuMDs7Ozs7Ozs7Ozs7OzsNCkJhcm5lczsxMTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7OTAuOTtpbml0aWFsZV9wb2ludF9ub207aW5pdGlhbGUubm9tOzkuMTtiYXJuZXMtaW50ZXJuYXRpb25hbC5jb207NTQuNTs7Ozs7Ozs7OztnbWFpbC5jb207NDUuNTs7DQpHcmVlbnBhcnRuZXJzOzExO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTs1NC41O3ByZW5vbV9zZXVsO3Byw6lub20gc2V1bDs0NS41O2dyZWVucGFydG5lcnMuaW1tbzsxMDAuMDs7Ozs7Ozs7Ozs7OzsNClNxdWFyZSBIYWJpdGF0OzEwO2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsxMDAuMDs7OztzcXVhcmVoYWJpdGF0LmZyOzUwLjA7Ozs7Ozs7Ozs7cHJvbW92ZW50ZS5jb207NTAuMDs7DQozJS5jb207MTA7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzUwLjA7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTs1MC4wO2dtYWlsLmNvbTsxMDAuMDs7Ozs7Ozs7Ozs7OzsNCkFHSTkyOzg7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzEwMC4wOzs7O291dGxvb2suZnI7MTAwLjA7Ozs7Ozs7Ozs7Ozs7DQpBIGxhIGx1Y2FybmU7ODthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTAwLjA7Ozs7Z21haWwuY29tOzEwMC4wOzs7Ozs7Ozs7Ozs7Ow0KTGlmZWhvbWU7ODthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTAwLjA7Ozs7Z21haWwuY29tOzEwMC4wOzs7Ozs7Ozs7Ozs7Ow0KTWVpbGxldXIgQ29uc2VpbDs4O25vbV9wb2ludF9wcmVub207bm9tLnByw6lub207MTAwLjA7Ozs7bGl2ZS5mcjsxMDAuMDs7Ozs7Ozs7Ozs7OzsNCkxhdmFsbGFyZCBJbW1vOzg7cHJlbm9tX3NldWw7cHLDqW5vbSBzZXVsOzYyLjU7YWRyZXNzZV9nZW5lcmlxdWU7Y29udGFjdEAgLyBpbmZvQDszNy41O2xhdmFsbGFyZC1pbW1vYmlsaWVyLmNvbTsxMDAuMDs7Ozs7Ozs7Ozs7OzsNCkwnaW1tb2JpbGllciBIdW1haW47ODtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzEwMC4wOzs7O2xpbW1vYmlsaWVyaHVtYWluLmNvbTsxMDAuMDs7Ozs7Ozs7Ozs7OzsNCkwnQXJ0IDIgVmVuZHJlOzg7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxMDAuMDs7OztsYXJ0MnZlbmRyZWltbW9iaWxpZXIuY29tOzEwMC4wOzs7Ozs7Ozs7Ozs7Ow0KTGVzIHByb2Zlc3Npb25uZWxzIGRlIGwnaW1tb2JpbGllcjs4O2luaXRpYWxlX3BvaW50X25vbTtpbml0aWFsZS5ub207MTAwLjA7Ozs7bGVzLXByb2Zlc3Npb25uZWxzLmltbW87MTAwLjA7Ozs7Ozs7Ozs7Ozs7DQpFdGhpa2tpbW1vOzg7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxMDAuMDs7OztldGhpa2staW1tby5mcjsxMDAuMDs7Ozs7Ozs7Ozs7OzsNCkRvbWluaTs4O2luaXRpYWxlX3BsdXNfbm9tO2luaXRpYWxlTm9tIChzYW5zIHPDqXBhcmF0ZXVyKTsxMDAuMDs7OztnbWFpbC5jb207MTAwLjA7Ozs7Ozs7Ozs7Ozs7DQpBbGxvd2E7ODthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTAwLjA7Ozs7Z21haWwuY29tOzEwMC4wOzs7Ozs7Ozs7Ozs7Ow0KQWR2aWNpbTs4O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTAwLjA7Ozs7YWR2aWNpbS5jb207MTAwLjA7Ozs7Ozs7Ozs7Ozs7DQpBViBUcmFuc2FjdGlvbnM7ODtwcmVub21fc2V1bDtwcsOpbm9tIHNldWw7MTAwLjA7Ozs7cHJlc3RpZ2VpbW1vYmlsaWVyLm5ldDsxMDAuMDs7Ozs7Ozs7Ozs7OzsNCkNhcm1lbjs4O2FsaWFzX3B1cjthbGlhcyAvIHBlcnNvIChpbXByw6l2aXNpYmxlKTsxMDAuMDs7Ozt5YWhvby5mcjsxMDAuMDs7Ozs7Ozs7Ozs7OzsNCkFCIEltbW9iaWxpZXI7ODtwcmVub21fbm9tX2NvbmNhdDtwcsOpbm9tK25vbSBjb2xsw6lzOzEwMC4wOzs7O2dtYWlsLmNvbTs2Mi41Ozs7Ozs7Ozs7O2ltbW9iaWxpZXJhYi5mcjszNy41OzsNCkNpZi1pbW1vOzg7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxMDAuMDs7OztjaWYtaW1tby5jb207MTAwLjA7Ozs7Ozs7Ozs7Ozs7DQpIVCZWZW5kcmUuY29tOzg7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxMDAuMDs7OztodGV0dmVuZHJlLmNvbTsxMDAuMDs7Ozs7Ozs7Ozs7OzsNClN3ZXZlbiBJbW1vOzg7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxMDAuMDs7Oztzd2V2ZW4taW1tby5mcjsxMDAuMDs7Ozs7Ozs7Ozs7OzsNClNtYXJ0IFByb3ByaW87ODtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzEwMC4wOzs7O3NtYXJ0cHJvcHJpby5jb207MTAwLjA7Ozs7Ozs7Ozs7Ozs7DQpPesOpbyBJbW1vOzg7cHJlbm9tX3BvaW50X25vbTtwcsOpbm9tLm5vbTsxMDAuMDs7OztsaXZlLmZyOzEwMC4wOzs7Ozs7Ozs7Ozs7Ow0KUHJvdmltbzs4O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTAwLjA7Ozs7cHJvdmltby5mcjsxMDAuMDs7Ozs7Ozs7Ozs7OzsNCldlIExvZ2U7ODthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTAwLjA7Ozs7Z21haWwuY29tOzEwMC4wOzs7Ozs7Ozs7Ozs7Ow0KTm90aWEgSW1tb2JpbGllcjs4O2FkcmVzc2VfZ2VuZXJpcXVlO2NvbnRhY3RAIC8gaW5mb0A7MTAwLjA7Ozs7bm90aWFpbW1vYmlsaWVyLmZyOzEwMC4wOzs7Ozs7Ozs7Ozs7Ow0KSHVudGVycyBTZXJ2aWNlOzY7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzEwMC4wOzs7O2hvdG1haWwuZnI7MTAwLjA7Ozs7Ozs7Ozs7Ozs7DQpBbWVzcyBJbW1vOzU7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxMDAuMDs7OzthbWVzcy1pbW1vLmZyOzEwMC4wOzs7Ozs7Ozs7Ozs7Ow0KRGV2Y29tOzU7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxMDAuMDs7OztkZXZjb20ucHJvOzEwMC4wOzs7Ozs7Ozs7Ozs7Ow0KSG9tZSBQYXNzaW9uIENvbmNlcHQ7NTthbGlhc19wdXI7YWxpYXMgLyBwZXJzbyAoaW1wcsOpdmlzaWJsZSk7MTAwLjA7Ozs7Z21haWwuY29tOzEwMC4wOzs7Ozs7Ozs7Ozs7Ow0KQ2ltbTs1O3ByZW5vbV9wb2ludF9ub207cHLDqW5vbS5ub207MTAwLjA7Ozs7Y2ltbS5jb207MTAwLjA7Ozs7Ozs7Ozs7Ozs7DQpDw6lzYXIgJiBCcnV0dXM7NTtwcmVub21fcG9pbnRfbm9tO3Byw6lub20ubm9tOzEwMC4wOzs7O2Nlc2FyZXRicnV0dXMuY29tOzEwMC4wOzs7Ozs7Ozs7Ozs7Ow0KUmFkaWFuIEltbW9iaWxpZXI7NTtwcmVub21fc2V1bDtwcsOpbm9tIHNldWw7MTAwLjA7Ozs7cmFkaWFuLWltbW9iaWxpZXIuZnI7MTAwLjA7Ozs7Ozs7Ozs7Ozs7DQpPcGVyYSBpbW1vYmlsaWVyOzU7aW5pdGlhbGVfcG9pbnRfbm9tO2luaXRpYWxlLm5vbTsxMDAuMDs7OztjYWJpbmV0LW9wZXJhLWltbW9iaWxpZXIuZnI7MTAwLjA7Ozs7Ozs7Ozs7Ozs7DQpjb25jZXB0IGltbW87NTtub21fc2V1bDtub20gc2V1bDsxMDAuMDs7Oztjb25jZXB0aW1tb2xpbGxlLmNvbTsxMDAuMDs7Ozs7Ozs7Ozs7OzsNCklta2l6OzM7YWxpYXNfcHVyO2FsaWFzIC8gcGVyc28gKGltcHLDqXZpc2libGUpOzEwMC4wOzs7O2lta2l6LmNvbTsxMDAuMDs7Ozs7Ozs7Ozs7OzsNCg=="

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
        return {"status": "invalid_format",
                "label": "Adresse mal formée — ne pas utiliser",
                "detail": "Le format de l'adresse est incorrect (ex. caractère manquant).",
                "icon": "🔴"}

    domain = email.split("@")[1]
    domain_info = get_domain_type(domain)
    dtype = domain_info["type"]
    mx    = domain_info["mx"]

    if dtype == "no_mx":
        return {"status": "no_mx",
                "label": "Domaine inexistant — adresse invalide",
                "detail": f"Le domaine @{domain} n'existe pas ou n'est plus actif. Inutile d'envoyer un email à cette adresse.",
                "icon": "🔴"}

    if dtype == "catchall":
        return {"status": "catchall",
                "label": "Impossible à vérifier — réseau accepte tout",
                "detail": f"Le serveur de {domain} accepte tous les emails sans vérifier si la boite existe vraiment. "
                          f"On ne peut pas confirmer que cette adresse est active — mais le format généré est statistiquement le plus probable.",
                "icon": "🟡"}

    if dtype == "blocked":
        return {"status": "blocked",
                "label": "Vérification bloquée — adresse probablement valide",
                "detail": f"Le serveur de {domain} refuse les vérifications automatiques (pratique courante chez Gmail, Outlook…). "
                          f"Le domaine existe bien, mais on ne peut pas confirmer la boite spécifique.",
                "icon": "🟡"}

    # strict → on teste la boite
    result = check_mailbox(email, mx)
    if result == "exists":
        return {"status": "exists",
                "label": "Adresse confirmée — boite active",
                "detail": "Le serveur a confirmé que cette boite mail existe et peut recevoir des emails.",
                "icon": "🟢"}
    if result == "rejected":
        return {"status": "rejected",
                "label": "Adresse invalide — boite inexistante",
                "detail": f"Le serveur de {domain} a rejeté cette adresse. La boite mail n'existe pas — essayez un autre format.",
                "icon": "🔴"}
    return {"status": "inconclusive",
            "label": "Résultat incertain — adresse à tester manuellement",
            "detail": f"Le serveur de {domain} n'a pas donné de réponse claire. "
                      f"Essayez d'envoyer un email de test ou de vérifier sur LinkedIn.",
            "icon": "🟡"}


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
st.caption(
    "Génères les adresses email les plus probables d'un agent selon son réseau.  "
    "— Fait par [Andrey](https://www.linkedin.com/in/bondaryev-andrey-944611203/)"
)

df = load_data()
networks = df["network"].tolist()

col_main, col_right = st.columns([3, 1])

with col_main:

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
                .query("`Proba (%)` >= 3")
                .reset_index(drop=True)
            )
            results_df.index = results_df.index + 1
            st.session_state["results_df"] = results_df

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

            # Deliverability check — bouton affiché hors du bloc generate
            st.divider()

    # Bouton vérifier — hors du if generate pour survivre au re-run Streamlit
    if "results_df" in st.session_state:
        if st.button("Verifier la delivrabilite des emails generes", use_container_width=True):

            yellow_emails = []
            for _, r in st.session_state["results_df"].iterrows():
                with st.spinner(f"Verification de {r['Email']}..."):
                    result = verify_email(r["Email"])
                col_email_v, col_status = st.columns([4, 3])
                with col_email_v:
                    st.code(r["Email"], language=None)
                with col_status:
                    st.markdown(f"{result['icon']} **{result['label']}**")
                    st.caption(result['detail'])
                if result['icon'] == '🟡':
                    yellow_emails.append(r['Email'])

            st.session_state["yellow_emails"] = yellow_emails

            # CSV download
            st.download_button(
                label="⬇️ Télécharger en CSV",
                data=st.session_state["results_df"].to_csv(index=False, sep=";").encode("utf-8-sig"),
                file_name=f"emails_{normalize(prenom)}_{normalize(nom)}_{selected_network.lower().replace(' ', '_')}.csv",
                mime="text/csv",
            )

with col_right:
    if "results_df" in st.session_state:
        st.info(
            "**Comment fonctionne la vérification ?**\n\n"
            "On teste d'abord si le domaine existe et s'il accepte les emails. "
            "Si le résultat est incertain 🟡, des liens s'affichent pour aller plus loin.\n\n"
            "**🔍 Hunter.io** s'ouvre directement avec l'email pré-rempli — un clic suffit.\n\n"
            "**Zerobounce, Neverbounce, Kickbox** : cliquer copie l'email dans le "
            "presse-papier — collez (Ctrl+V) dans le champ du site."
        )

    if "yellow_emails" in st.session_state and st.session_state["yellow_emails"]:
        st.markdown("---")
        st.markdown("**🔍 Double-vérification externe**")
        for _email in st.session_state["yellow_emails"]:
            _ejs = _email.replace("'", "\\'")
            _hunter = f"https://hunter.io/email-verifier/{_email}"
            _zb = "https://www.zerobounce.net/email-verifier"
            _nb = "https://www.neverbounce.com/email-verifier"
            _kb = "https://kickbox.com/email-verifier/"
            st.caption(f"📧 `{_email}`")
            _html = (
                '<style>'
                '.vl a{font-size:13px;text-decoration:none;display:block;margin:3px 0;}'
                '.vl a:hover{text-decoration:underline;}'
                '.vh{color:#1a7f37;font-weight:bold;}'
                '.vo{color:#4A90D9;}'
                '</style>'
                '<script>'
                'function fc(t){var a=document.createElement("textarea");a.value=t;'
                'a.style.position="fixed";a.style.opacity="0";'
                'document.body.appendChild(a);a.focus();a.select();'
                'document.execCommand("copy");document.body.removeChild(a);}'
                f'function oc(u){{try{{navigator.clipboard.writeText("{_ejs}").catch(()=>fc("{_ejs}"));}}'
                f'catch(e){{fc("{_ejs}");}}window.open(u,"_blank");}}'
                '</script>'
                '<div class="vl">'
                f'<a class="vh" href="{_hunter}" target="_blank">🔍 Hunter.io — auto</a>'
                f'<a class="vo" href="#" onclick="oc(\'{_zb}\');return false;">📋 Zerobounce</a>'
                f'<a class="vo" href="#" onclick="oc(\'{_nb}\');return false;">📋 Neverbounce</a>'
                f'<a class="vo" href="#" onclick="oc(\'{_kb}\');return false;">📋 Kickbox</a>'
                '</div>'
            )
            components.html(_html, height=95)
