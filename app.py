import streamlit as st
import pandas as pd
import unicodedata
import re
import base64
import io

st.set_page_config(
    page_title="Email Predictor — RealAdvisors",
    page_icon="📧",
    layout="centered",
)

_D = "77u/bmV0d29yaztuYl9lbWFpbHNfY2xhc3Nlcztlc3RpbWF0aW9uXzFfbW90aWY7ZXN0aW1hdGlvbl8xX2NsZTtlc3RpbWF0aW9uXzFfcHJvYmFfcGN0O2VzdGltYXRpb25fMl9tb3RpZjtlc3RpbWF0aW9uXzJfY2xlO2VzdGltYXRpb25fMl9wcm9iYV9wY3Q7ZXN0aW1hdGlvbl8zX21vdGlmO2VzdGltYXRpb25fM19jbGU7ZXN0aW1hdGlvbl8zX3Byb2JhX3BjdDtkb21haW5lXzE7ZG9tYWluZV8xX3Byb2JhX3BjdDtkb21haW5lXzI7ZG9tYWluZV8yX3Byb2JhX3BjdDtkb21haW5lXzM7ZG9tYWluZV8zX3Byb2JhX3BjdA0KSWFkOzQ3OTc0O3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207NzAuMDthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsyOS4zO3Byw6lub20rbm9tIGNvbGzDqXMgKHNhbnMgLiBuaSBfKTtwcmVub21fbm9tX2NvbmNhdDswLjM7aWFkZnJhbmNlLmZyOzk0Ljg7Z21haWwuY29tOzIuMDtic2tpbW1vYmlsaWVyLmNvbTswLjkNClNhZnRpOzIxNDI3O3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207NTguNzthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTszNi45O3Byw6lub20rbm9tIGNvbGzDqXMgKHNhbnMgLiBuaSBfKTtwcmVub21fbm9tX2NvbmNhdDsxLjM7c2FmdGkuZnI7NzguNDtnbWFpbC5jb207Ni44O2NhcGlmcmFuY2UuZnI7MS4wDQpQcm9wcmnDqXTDqXMgcHJpdsOpZXM7MTA4MzM7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7OTcuOTtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzEuMTtwcsOpbm9tK25vbSBjb2xsw6lzIChzYW5zIC4gbmkgXyk7cHJlbm9tX25vbV9jb25jYXQ7MC40O3Byb3ByaWV0ZXMtcHJpdmVlcy5jb207OTUuNTtnbWFpbC5jb207MS44O29yYW5nZS5mcjswLjQNCkVmZmljaXR5OzgzOTE7aW5pdGlhbGUgKyBub207aW5pdGlhbGVfcGx1c19ub207NzcuMDthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsxOS4xO3Byw6lub20rbm9tIGNvbGzDqXMgKHNhbnMgLiBuaSBfKTtwcmVub21fbm9tX2NvbmNhdDsyLjY7ZWZmaWNpdHkuY29tOzkzLjY7Z21haWwuY29tOzMuMDt5YWhvby5mcjswLjQNCkNhcGlGcmFuY2U7Nzk4NTtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzY4LjQ7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7MzAuMztwcsOpbm9tK25vbSBjb2xsw6lzIChzYW5zIC4gbmkgXyk7cHJlbm9tX25vbV9jb25jYXQ7MC43O2NhcGlmcmFuY2UuZnI7OTEuMztnbWFpbC5jb207My4xO3lhaG9vLmZyOzAuNg0KS2VsbGVyIFdpbGxpYW1zOzYzMDU7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTs2Ny41O2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzI4LjQ7aW5pdGlhbGUgKyBub207aW5pdGlhbGVfcGx1c19ub207MS41O2t3ZnJhbmNlLmNvbTs3OC40O2dtYWlsLmNvbTs3LjY7Y2VzYXJldGJydXR1cy5jb207Mi4yDQpCc2sgaW1tb2JpbGllcjs0NzEwO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzYxLjU7aW5pdGlhbGUgKyBub207aW5pdGlhbGVfcGx1c19ub207MzMuMztwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzMuNTtic2tpbW1vYmlsaWVyLmNvbTs4Ni43O2dtYWlsLmNvbTs2LjM7aWFkZnJhbmNlLmZyOzEuMw0KT3B0aW1ob21lOzQ2OTA7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NTAuNDtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzQ4Ljg7cHLDqW5vbStub20gY29sbMOpcyAoc2FucyAuIG5pIF8pO3ByZW5vbV9ub21fY29uY2F0OzAuNjtvcHRpbWhvbWUuY29tOzkyLjU7Z21haWwuY29tOzMuNztvcmFuZ2UuZnI7MC43DQpNZWdhZ2VuY2U7NDE1MDthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTs2Ni43O3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207MzIuMDtwcsOpbm9tK25vbSBjb2xsw6lzIChzYW5zIC4gbmkgXyk7cHJlbm9tX25vbV9jb25jYXQ7MS4wO21lZ2FnZW5jZS5jb207OTAuODtnbWFpbC5jb207NS4xO2hvdG1haWwuZnI7MC41DQpBdXRyZTsyMjU0O2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzYwLjY7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTsyNC44O2luaXRpYWxlICsgbm9tO2luaXRpYWxlX3BsdXNfbm9tOzYuMztnbWFpbC5jb207MzAuMDtic2tpbW1vYmlsaWVyLmNvbTs4LjE7aWFkZnJhbmNlLmZyOzYuNw0KTGVzIFBvcnRlcyBDbMOpczsxODU4O3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207NTIuNjthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTszNi4yO2NvbnRhY3RAIC8gaW5mb0AgLyDigKY7YWRyZXNzZV9nZW5lcmlxdWU7Ni44O2ltbW9iaWxpZXIuZW1haWw7NzUuOTtnbWFpbC5jb207Ni4yO21hYXAtaW1tb2JpbGllci5mcjsxLjANCkxhIEZvdXJtaTsxNzk4O3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207NzAuMjthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsyOC44O3Byw6lub20rbm9tIGNvbGzDqXMgKHNhbnMgLiBuaSBfKTtwcmVub21fbm9tX2NvbmNhdDswLjc7bGFmb3VybWktaW1tby5jb207ODIuOTtsZmltbW8uZnI7OC42O2dtYWlsLmNvbTszLjcNCjNHIEltbW87MTcxODtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzQyLjg7aW5pdGlhbGUgKyBub207aW5pdGlhbGVfcGx1c19ub207MzIuNjthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsyMy43OzNnaW1tb2JpbGllci5jb207OTUuMjtnbWFpbC5jb207Mi4yO2pjLWltbW9iaWxpZXIuZnI7MC4zDQpFeHAgRnJhbmNlOzE2MDc7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTs2Ny4wO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzI5LjA7cHLDqW5vbSBzZXVsO3ByZW5vbV9zZXVsOzIuNztleHBmcmFuY2UuZnI7ODcuNztsdXh1cnlieWJsdWUuY29tOzQuNztnbWFpbC5jb207NC4wDQpJa2FtaTs4NDI7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7OTkuNTtjb250YWN0QCAvIGluZm9AIC8g4oCmO2FkcmVzc2VfZ2VuZXJpcXVlOzAuNTs7OzAuMDtpa2FtaS5mcjs5Ni4wO2dtYWlsLmNvbTsyLjQ7b3JwaS5jb207MC40DQpFeHBlcnRpbW87MTk0O2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzY5LjE7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTsxMC4zO2NvbnRhY3RAIC8gaW5mb0AgLyDigKY7YWRyZXNzZV9nZW5lcmlxdWU7OS4zO2dtYWlsLmNvbTs1MC4wO2V4cGVydGltby5jb207MTkuNjtvdXRsb29rLmZyOzMuNg0KRHIgSG91c2UgSW1tbzsxNTE7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NzUuNTtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzE2LjY7cHLDqW5vbSBzZXVsO3ByZW5vbV9zZXVsOzQuMDtkcmhvdXNlLWltbW8uY29tOzQ0LjQ7ZHJob3VzZS5pbW1vOzIwLjU7Z21haWwuY29tOzExLjMNCkRhbnMgdW5lIGFnZW5jZTsxMzc7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NjIuODtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzE3LjU7aW5pdGlhbGUgKyBub207aW5pdGlhbGVfcGx1c19ub207OC4wO2dtYWlsLmNvbTszMy42O2hvdG1haWwuZnI7NC40O2FnZW5jZW5pY2FyZC5mcjsyLjkNCkxsb3lkICYgRGF2aXM7MTAwO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzYyLjA7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTszOC4wOzs7MC4wO2xsb3lkLWRhdmlzLmNvbTs5MS4wO2dtYWlsLmNvbTs5LjA7Ow0KTGliZXJrZXlzOzk0O3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207NTkuNjthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTs0MC40Ozs7MC4wO2xpYmVya2V5cy5jb207OTMuNjtnbWFpbC5jb207NS4zO2NhcGlmcmFuY2UuZnI7MS4xDQpBYnJpY3VsdGV1cnM7OTE7cHLDqW5vbSBzZXVsO3ByZW5vbV9zZXVsOzU3LjE7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NDIuOTs7OzAuMDthYnJpY3VsdGV1cnMuY29tOzk1LjY7Z21haWwuY29tOzMuMztsZXNhYnJpY3VsdGV1cnMuY29tOzEuMQ0KV2VlbG9kZ2U7ODc7aW5pdGlhbGUgKyBub207aW5pdGlhbGVfcGx1c19ub207NTguNjthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsyNy42O2NvbnRhY3RAIC8gaW5mb0AgLyDigKY7YWRyZXNzZV9nZW5lcmlxdWU7My40O3dlLWxvZ2UuY29tOzc1Ljk7d2VlbG9kZ2UuZnI7OC4wO2dtYWlsLmNvbTs0LjYNCk1laWxsZXVyc0JpZW5zOzg2O2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzQ2LjU7aW5pdGlhbGUgKyBub207aW5pdGlhbGVfcGx1c19ub207NDMuMDtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzcuMDttZWlsbGV1cnNiaWVucy5jb207NjAuNTtnbWFpbC5jb207MzIuNjtob3RtYWlsLmZyOzMuNQ0KTm9vdmltbzs3NDtpbml0aWFsZSArIG5vbTtpbml0aWFsZV9wbHVzX25vbTs3MC4zO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzI1Ljc7cHLDqW5vbStub20gY29sbMOpcyAoc2FucyAuIG5pIF8pO3ByZW5vbV9ub21fY29uY2F0OzQuMTtub292aW1vLmZyOzkwLjU7ZHJob3VzZS5pbW1vOzUuNDtnbWFpbC5jb207NC4xDQpDZW50dXJ5IDIxOzY4O2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzY0Ljc7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTszMC45O3Byw6lub20rbm9tIGNvbGzDqXMgKHNhbnMgLiBuaSBfKTtwcmVub21fbm9tX2NvbmNhdDs0LjQ7Y2VudHVyeTIxLmZyOzU0LjQ7Z21haWwuY29tOzI5LjQ7bGl2ZS5mcjs0LjQNCkVuZGllIEZyYW5jZTs2NDtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzUwLjA7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NTAuMDs7OzAuMDtlbmRpZS5mcjs3MC4zO2dtYWlsLmNvbTsxOC44O291dGxvb2suZnI7NC43DQpXZSBJbnZlc3QgRnJhbmNlOzYzO3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207ODUuNzthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsxNC4zOzs7MC4wO3dlaW52ZXN0LmZyOzk1LjI7aWFkZnJhbmNlLmZyOzQuODs7DQpJbW1vRm9yZmFpdDs2MDthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsxMDAuMDs7OzAuMDs7OzAuMDtpbW1vZm9yZmFpdC5mcjs5NS4wO29yYW5nZS5mcjs1LjA7Ow0KQkwgQWdlbnRzIEltbW9iaWxpZXJzOzUxO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzgyLjQ7cHLDqW5vbStub20gY29sbMOpcyAoc2FucyAuIG5pIF8pO3ByZW5vbV9ub21fY29uY2F0OzExLjg7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTs1Ljk7YmwtYWdlbnRzLmZyOzc4LjQ7Z21haWwuY29tOzExLjg7d2VpbnZlc3QuZnI7NS45DQpLZXltZXg7NTE7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTs1OC44O2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzM5LjI7cHLDqW5vbStub20gY29sbMOpcyAoc2FucyAuIG5pIF8pO3ByZW5vbV9ub21fY29uY2F0OzIuMDtrZXltZXguZnI7NjYuNztrZXltZXhpbW1vLmZyOzE5LjY7Z21haWwuY29tOzUuOQ0KUmVtYXg7NTE7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTs3MC42O2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzE5LjY7aW5pdGlhbGUgKyBub207aW5pdGlhbGVfcGx1c19ub207OS44O3JlbWF4LmZyOzc4LjQ7Z21haWwuY29tOzExLjg7aW1tb2Zyb250aWVyZS5jb207OS44DQpBeG87NDk7aW5pdGlhbGUgKyBub207aW5pdGlhbGVfcGx1c19ub207NjMuMzthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTszMC42O3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207Ni4xO2F4by5pbW1vOzQwLjg7YXhvLWFjdGlmcy5mcjsyNi41O2dtYWlsLmNvbTsxMi4yDQpJbW1vIFJlc2VhdTs0NzthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTs4Ny4yO3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207MTIuODs7OzAuMDtpbW1vLXJlc2VhdS5jb207NzIuMztpYWRmcmFuY2UuZnI7Ni40O2dtYWlsLmNvbTs2LjQNCkNhc2F2bzs0NjtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzUyLjI7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NDcuODs7OzAuMDtjYXNhdm8uY29tOzczLjk7cHJvcHJpb28uZnI7MTMuMDtnbWFpbC5jb207Ni41DQpTZXh0YW50OzM2O3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207NzIuMjthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsyNy44Ozs7MC4wO3NleHRhbnRmcmFuY2UuZnI7ODAuNjtob3RtYWlsLmNvbTs4LjM7c2V4dGFudC5mcjs4LjMNCkxHTSBJbW1vYmlsaWVyOzI5O3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207NDQuODthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTszNC41O3Byw6lub20gc2V1bDtwcmVub21fc2V1bDsxMC4zO2xnbS1pbW1vYmlsaWVyLmZyOzU1LjI7Z21haWwuY29tOzM0LjU7YXVyb3JhaG9ydGkuZnI7MTAuMw0KSW1tb3Jlc2VhdTsyNTthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsxMDAuMDs7OzAuMDs7OzAuMDtpbW1vLXJlc2VhdS5jb207ODQuMDtob3RtYWlsLmZyOzE2LjA7Ow0KT3JwaTsyMTthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTs0Mi45O2luaXRpYWxlICsgbm9tO2luaXRpYWxlX3BsdXNfbm9tOzI4LjY7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTsyOC42O29ycGkuY29tOzcxLjQ7b3JhbmdlLmZyOzE0LjM7Z21haWwuY29tOzE0LjMNCkVjb3RyYW5zYWM7MjA7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTsxMDAuMDs7OzAuMDs7OzAuMDtlY290cmFuc2FjLmZyOzEwMC4wOzs7Ow0KTGFmb3LDqnQ7MjA7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NzUuMDtpbml0aWFsZSArIG5vbTtpbml0aWFsZV9wbHVzX25vbTsyMC4wO3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207NS4wO2xhZm9yZXQuY29tOzgwLjA7Y2VnZXRlbC5uZXQ7MTUuMDtpYWRmcmFuY2UuZnI7NS4wDQpXZSBJbnZlc3Q7MjA7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NTUuMDtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzMwLjA7cHLDqW5vbStub20gY29sbMOpcyAoc2FucyAuIG5pIF8pO3ByZW5vbV9ub21fY29uY2F0OzE1LjA7d2VpbnZlc3QuZnI7NDUuMDtibC1hZ2VudHMuZnI7MjAuMDtpYWRmcmFuY2UuZnI7MTUuMA0KQWdlbnRNYW5kYXRhaXJlLmZyOzE5O2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzQ3LjQ7cHLDqW5vbStub20gY29sbMOpcyAoc2FucyAuIG5pIF8pO3ByZW5vbV9ub21fY29uY2F0OzM2Ljg7Y29udGFjdEAgLyBpbmZvQCAvIOKApjthZHJlc3NlX2dlbmVyaXF1ZTsxNS44O2FnZW50bWFuZGF0YWlyZS5mcjs4NC4yO2dtYWlsLmNvbTsxNS44OzsNCllvdWxpdmUgaW1tb2JpbGllcjsxOTthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTs1Mi42O3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207NDcuNDs7OzAuMDt5b3VsaXZlLWltbW9iaWxpZXIuZnI7NjMuMjtjYXBpZnJhbmNlLmZyOzE1Ljg7b3V0bG9vay5mcjsxNS44DQpFcmE7MTc7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTsxMDAuMDs7OzAuMDs7OzAuMDtlcmFpbW1vLmZyOzEwMC4wOzs7Ow0KUsOpc2VhdSBIQjsxNjthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTs2Mi41O3Byw6lub20rbm9tIGNvbGzDqXMgKHNhbnMgLiBuaSBfKTtwcmVub21fbm9tX2NvbmNhdDsxOC44O3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207MTguODtnbWFpbC5jb207NTYuMjtyZXNlYXVoYi5mcjs0My44OzsNCkMyaTsxNTthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTs4MC4wO25vbSBzZXVsO25vbV9zZXVsOzIwLjA7OzswLjA7c2ZyLmZyOzIwLjA7eWFob28uZnI7MjAuMDtncm91cGUtYzJpLmNvbTsyMC4wDQpTd2l4aW07MTQ7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7MTAwLjA7OzswLjA7OzswLjA7Z21haWwuY29tOzUwLjA7c3dpeGltLmNvbTs1MC4wOzsNCk5lc3Rlbm47MTM7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7OTIuMztjb250YWN0QCAvIGluZm9AIC8g4oCmO2FkcmVzc2VfZ2VuZXJpcXVlOzcuNzs7OzAuMDtuZXN0ZW5uLmNvbTsxMDAuMDs7OzsNCkxlZGlsIGltbW87MTI7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTsxMDAuMDs7OzAuMDs7OzAuMDtsZWRpbC5pbW1vOzc1LjA7Z21haWwuY29tOzI1LjA7Ow0KU3TDqXBoYW5lIFBsYXphIEltbW87MTI7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NTAuMDtpbml0aWFsZSArIG5vbTtpbml0aWFsZV9wbHVzX25vbTs1MC4wOzs7MC4wO3N0ZXBoYW5lcGxhemFpbW1vYmlsaWVyLmNvbTs3NS4wO2dtYWlsLmNvbTsyNS4wOzsNClRlYW1maTsxMjtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzc1LjA7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7MjUuMDs7OzAuMDt0ZWFtZmkuZnI7NzUuMDtnbWFpbC5jb207MjUuMDs7DQpUaGUgRG9vciBNYW47MTI7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTs3NS4wO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzI1LjA7OzswLjA7dGRtLmltbW87MTAwLjA7Ozs7DQpUb3dlciBpbW1vYmlsaWVyOzEyO3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207NzUuMDthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsyNS4wOzs7MC4wO2dtYWlsLmNvbTs3NS4wO3Rvd2VyLWltbW9iaWxpZXIuZnI7MjUuMDs7DQpGb25jaWE7MTA7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTs3MC4wO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzMwLjA7OzswLjA7Z21haWwuY29tOzYwLjA7Zm9uY2lhLmNvbTs0MC4wOzsNCkltb2NvbnNlaWw7MTA7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NzAuMDtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzMwLjA7OzswLjA7aW1vY29uc2VpbC5jb207NjAuMDtmcmllbmRseS1pbW1vLmZyOzMwLjA7Z21haWwuY29tOzEwLjANCkFnZW5jZSBpbW1vOzk7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NjYuNztwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzMzLjM7OzswLjA7aWNsb3VkLmNvbTszMy4zO2FnZW5jZS5pbW1vOzMzLjM7Z21haWwuY29tOzMzLjMNCkJvbmFwYXJ0ZTs5O2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzEwMC4wOzs7MC4wOzs7MC4wO2JvbmFwYXJ0ZS1hcnRkZXZpdnJlLmNvbTsxMDAuMDs7OzsNCldpbmtleTs5O2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzY2Ljc7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTszMy4zOzs7MC4wO3dpbmtleS5mcjs2Ni43O2dtYWlsLmNvbTszMy4zOzsNCk5lb3MtSW1tbzs4O3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207NzUuMDthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsyNS4wOzs7MC4wO25lb3MtaW1tby5jb207NjIuNTtnbWFpbC5jb207MjUuMDtob3RtYWlsLmNvbTsxMi41DQpBa29taTs2O2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzEwMC4wOzs7MC4wOzs7MC4wO2Frb21pLmZyOzUwLjA7Z21haWwuY29tOzUwLjA7Ow0KQ2FzYWRpY2k7Njtpbml0aWFsZSArIG5vbTtpbml0aWFsZV9wbHVzX25vbTs1MC4wO2NvbnRhY3RAIC8gaW5mb0AgLyDigKY7YWRyZXNzZV9nZW5lcmlxdWU7NTAuMDs7OzAuMDtjYXNhZGljaS5mcjs1MC4wO2NocmlzdGlhbmVzc2UuZnI7NTAuMDs7DQpGcmFuY2UgUHJvcHJpbzs2O2luaXRpYWxlICsgbm9tO2luaXRpYWxlX3BsdXNfbm9tOzUwLjA7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NTAuMDs7OzAuMDtmcmFuY2Vwcm9wcmlvLmNvbTsxMDAuMDs7OzsNCkdsb2JhbCBJbW1vYmlsaWVyOzY7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NTAuMDtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzUwLjA7OzswLjA7Z21haWwuY29tOzUwLjA7ZnJlZS5mcjs1MC4wOzsNCkh1bWFuOzY7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7MTAwLjA7OzswLjA7OzswLjA7aG90bWFpbC5jb207NTAuMDtob3RtYWlsLmZyOzUwLjA7Ow0KSW1tb2pveTs2O2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzEwMC4wOzs7MC4wOzs7MC4wO2dtYWlsLmNvbTs1MC4wO2ltbW9qb3kuY29tOzUwLjA7Ow0KTCdhZ2VudCBpbW1vYmlsaWVyOzY7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NTAuMDtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzUwLjA7OzswLjA7Z21haWwuY29tOzEwMC4wOzs7Ow0KTGVnZ2V0dCBJbW1vYmlsaWVyOzY7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTs1MC4wO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzUwLjA7OzswLjA7bGVnZ2V0dC5mcjs1MC4wO2hvdG1haWwuY29tOzUwLjA7Ow0KTGlsaWhvbWU7NjthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTs1MC4wO3Byw6lub20rbm9tIGNvbGzDqXMgKHNhbnMgLiBuaSBfKTtwcmVub21fbm9tX2NvbmNhdDs1MC4wOzs7MC4wO2Nhcm1lbi1pbW1vYmlsaWVyLmNvbTs1MC4wO2dtYWlsLmNvbTs1MC4wOzsNCk1hIG1haXNvbiBpZMOpYWxlOzY7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7MTAwLjA7OzswLjA7OzswLjA7bWFtYWlzb25pZGVhbGUuaW1tbzs4My4zO2xhbWFpc29uaWRlYWxlLmltbW87MTYuNzs7DQpOYW9zIEltbW9iaWxpZXI7NjtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzEwMC4wOzs7MC4wOzs7MC4wO25hb3NpbW1vYmlsaWVyLmNvbTs1MC4wO2dtYWlsLmNvbTs1MC4wOzsNClBpZXRyYXBvbGlzOzY7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7NTAuMDtwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzUwLjA7OzswLjA7cGlldHJhcG9saXMuZnI7NTAuMDtnbWFpbC5jb207NTAuMDs7DQpTb2xpZCBJbW1vOzY7cHLDqW5vbStub20gY29sbMOpcyAoc2FucyAuIG5pIF8pO3ByZW5vbV9ub21fY29uY2F0OzUwLjA7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTszMy4zO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzE2Ljc7c29saWQtaW1tby5jb207MTAwLjA7Ozs7DQpIb21raTs0O3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207NzUuMDtjb250YWN0QCAvIGluZm9AIC8g4oCmO2FkcmVzc2VfZ2VuZXJpcXVlOzI1LjA7OzswLjA7aG9ta2ktaW1tb2JpbGllci5jb207NzUuMDtnbWFpbC5jb207MjUuMDs7DQpBIGxhIGx1Y2FybmU7MzthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsxMDAuMDs7OzAuMDs7OzAuMDtnbWFpbC5jb207MTAwLjA7Ozs7DQpBR0k5MjszO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzEwMC4wOzs7MC4wOzs7MC4wO291dGxvb2suZnI7MTAwLjA7Ozs7DQpBViBUcmFuc2FjdGlvbnM7MztwcsOpbm9tIHNldWw7cHJlbm9tX3NldWw7MTAwLjA7OzswLjA7OzswLjA7cHJlc3RpZ2VpbW1vYmlsaWVyLm5ldDsxMDAuMDs7OzsNCkFkdmljaW07MztwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzEwMC4wOzs7MC4wOzs7MC4wO2FkdmljaW0uY29tOzEwMC4wOzs7Ow0KQWxsb3dhOzM7cHLDqW5vbStub20gY29sbMOpcyAoc2FucyAuIG5pIF8pO3ByZW5vbV9ub21fY29uY2F0OzEwMC4wOzs7MC4wOzs7MC4wO2dtYWlsLmNvbTsxMDAuMDs7OzsNCkNhcm1lbjszO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzEwMC4wOzs7MC4wOzs7MC4wO3lhaG9vLmZyOzEwMC4wOzs7Ow0KQ2lmLWltbW87MzthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsxMDAuMDs7OzAuMDs7OzAuMDtjaWYtaW1tby5jb207MTAwLjA7Ozs7DQpEb21pbmk7Mztpbml0aWFsZSArIG5vbTtpbml0aWFsZV9wbHVzX25vbTsxMDAuMDs7OzAuMDs7OzAuMDtnbWFpbC5jb207MTAwLjA7Ozs7DQpFdGhpa2tpbW1vOzM7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTsxMDAuMDs7OzAuMDs7OzAuMDtldGhpa2staW1tby5mcjsxMDAuMDs7OzsNCkhUJlZlbmRyZS5jb207MzthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsxMDAuMDs7OzAuMDs7OzAuMDtodGV0dmVuZHJlLmNvbTsxMDAuMDs7OzsNCklta2l6OzM7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7MTAwLjA7OzswLjA7OzswLjA7aW1raXouY29tOzEwMC4wOzs7Ow0KSW1tbyBkZSBGcmFuY2U7MztwcsOpbm9tIHNldWw7cHJlbm9tX3NldWw7MTAwLjA7OzswLjA7OzswLjA7amNnaW1tby5jb207MTAwLjA7Ozs7DQpMJ0FkcmVzc2U7MztwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzEwMC4wOzs7MC4wOzs7MC4wO2xhZHJlc3NlLmNvbTsxMDAuMDs7OzsNCkwnQXJ0IDIgVmVuZHJlOzM7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7MTAwLjA7OzswLjA7OzswLjA7bGFydDJ2ZW5kcmVpbW1vYmlsaWVyLmNvbTsxMDAuMDs7OzsNCkwnaW1tb2JpbGllciBIdW1haW47MzthdXRyZSAoYWxpYXMsIHBlcnNvLCBmYXV0ZSwg4oCmKTthdXRyZTsxMDAuMDs7OzAuMDs7OzAuMDtsaW1tb2JpbGllcmh1bWFpbi5jb207MTAwLjA7Ozs7DQpMZXMgcHJvZmVzc2lvbm5lbHMgZGUgbCdpbW1vYmlsaWVyOzM7YXV0cmUgKGFsaWFzLCBwZXJzbywgZmF1dGUsIOKApik7YXV0cmU7MTAwLjA7OzswLjA7OzswLjA7bGVzLXByb2Zlc3Npb25uZWxzLmltbW87MTAwLjA7Ozs7DQpMaWZlaG9tZTszO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzEwMC4wOzs7MC4wOzs7MC4wO2dtYWlsLmNvbTsxMDAuMDs7OzsNCk1laWxsZXVyIENvbnNlaWw7MztwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzEwMC4wOzs7MC4wOzs7MC4wO2xpdmUuZnI7MTAwLjA7Ozs7DQpOb3RpYSBJbW1vYmlsaWVyOzM7Y29udGFjdEAgLyBpbmZvQCAvIOKApjthZHJlc3NlX2dlbmVyaXF1ZTsxMDAuMDs7OzAuMDs7OzAuMDtub3RpYWltbW9iaWxpZXIuZnI7MTAwLjA7Ozs7DQpPesOpbyBJbW1vOzM7cHLDqW5vbS5ub207cHJlbm9tX3BvaW50X25vbTsxMDAuMDs7OzAuMDs7OzAuMDtsaXZlLmZyOzEwMC4wOzs7Ow0KUHJvdmltbzszO3Byw6lub20ubm9tO3ByZW5vbV9wb2ludF9ub207MTAwLjA7OzswLjA7OzswLjA7cHJvdmltby5mcjsxMDAuMDs7OzsNClNtYXJ0IFByb3ByaW87MztwcsOpbm9tLm5vbTtwcmVub21fcG9pbnRfbm9tOzEwMC4wOzs7MC4wOzs7MC4wO3NtYXJ0cHJvcHJpby5jb207MTAwLjA7Ozs7DQpTd2V2ZW4gSW1tbzszO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzEwMC4wOzs7MC4wOzs7MC4wO3N3ZXZlbi1pbW1vLmZyOzEwMC4wOzs7Ow0KV2UgTG9nZTszO2F1dHJlIChhbGlhcywgcGVyc28sIGZhdXRlLCDigKYpO2F1dHJlOzEwMC4wOzs7MC4wOzs7MC4wO2dtYWlsLmNvbTsxMDAuMDs7OzsNCg=="

# ── Data ──────────────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    raw = base64.b64decode(_D)
    df = pd.read_csv(io.BytesIO(raw), sep=";", dtype=str)
    for col in df.columns:
        if "proba_pct" in col:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    return df

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
    "prenom_point_nom":  "prénom.nom",
    "initiale_plus_nom": "initiale + nom",
    "prenom_nom_concat": "prénom+nom collés",
    "prenom_seul":       "prénom seul",
    "nom_seul":          "nom seul",
    "adresse_generique": "contact@ / info@",
    "autre":             "alias / perso (imprévisible)",
}

def generate_local(motif: str, prenom: str, nom: str) -> list[str]:
    """Return a list of candidate local parts for a given motif."""
    p = normalize(prenom)
    n = normalize(nom)
    if motif == "prenom_point_nom":
        return [f"{p}.{n}"] if p and n else []
    if motif == "initiale_plus_nom":
        return [f"{p[0]}.{n}"] if p and n else []
    if motif == "prenom_nom_concat":
        return [f"{p}{n}"] if p and n else []
    if motif == "prenom_seul":
        return [p] if p else []
    if motif == "nom_seul":
        return [n] if n else []
    if motif == "adresse_generique":
        return ["contact", "info"]
    return []  # "autre" — unpredictable

# ── Which inputs are needed for a given set of motifs ─────────────────────────

def needs_inputs(motifs: list[str]) -> tuple[bool, bool]:
    """Return (needs_prenom, needs_nom)."""
    needs_p = any(m in {"prenom_point_nom", "initiale_plus_nom", "prenom_nom_concat", "prenom_seul"} for m in motifs)
    needs_n = any(m in {"prenom_point_nom", "initiale_plus_nom", "prenom_nom_concat", "nom_seul"} for m in motifs)
    return needs_p, needs_n

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
for i in [1, 2, 3]:
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
autre_pct = sum(m["proba"] for m in motifs_data if m["cle"] == "autre")
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
            if m["cle"] == "autre":
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

        if cle == "autre":
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

        # CSV download
        st.download_button(
            label="⬇️ Télécharger en CSV",
            data=results_df.to_csv(index=False, sep=";").encode("utf-8-sig"),
            file_name=f"emails_{normalize(prenom)}_{normalize(nom)}_{selected_network.lower().replace(' ', '_')}.csv",
            mime="text/csv",
        )
