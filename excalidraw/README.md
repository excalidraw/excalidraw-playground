# excalidraw.py

> Python library to generate `.excalidraw` files.

```python
import excalidraw

scene = excalidraw.Excalidraw()
scene.add_rectangle(0, 0, 100, 100)
scene.add_ellipse(120, 0, 100, 100)

scene.save_as("hello")
scene.save_as_lib("hello")
```
