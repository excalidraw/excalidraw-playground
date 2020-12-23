import excalidraw

scene = excalidraw.Excalidraw()
scene.add_chart("chart.csv", 64, 480)
scene.save_as("chart")
